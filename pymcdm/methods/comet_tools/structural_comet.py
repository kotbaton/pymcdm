# Copyright (c) 2023 Andrii Shekhovtsov

import numpy as np

from ..comet import COMET
from ..mcda_method import MCDA_method
from ...io import TableDesc,  Table, MCDA_results


class Submodel:
    """ Create object of the COMET submodel. This class is mostly for internal
        use in the StructuralCOMET class or for creating StructuralCOMET
        object.

        Parameters
        ----------
            structure : tuple or int
                Structure of the submodel. Refer to the single criteria by
                names (str) or by indexes (int). If structure is more complex
                use defined names or nested structures. See example use of
                StructuralCOMET for more information.

            cvalues : list or None
                Cvalues for output of this submodel. Pass None if it is a final
                model to be evaluated.

            expert_function : Callable or None
                Expert function to evaluate characteristic objects in
                the submodel. See COMET documentation for more information.
                None is reserved for internal use in StructuralCOMET class.

            name : str or None
                Name (alias) of the Submodel. If name is not None Submodel
                could be referred by it in another Submodel in one
                StructuralCOMET model.
    """

    def __init__(self,
                 structure,
                 cvalues,  # Could be None if it is final submodel
                 expert_function,  # Could be None if structure is int
                 name,  # If we do not provide name we should put in some generic one
                 ):
        self.cvalues = cvalues
        self.structure = structure

        if name is None:
            self.name = str(structure)
        else:
            self.name = name

        if not isinstance(self.structure, int) and expert_function is None:
            raise ValueError('expert_function argument must be a function if '
                             'structure is not a single criterion!')

        self.expert_function = expert_function

        self.model = None

    def __str__(self):
        return f"""
COMET Submodel "{self.name}"
Structure: {self.structure}
Output cvalues: {self.cvalues}
"""

    def build(self, submodels):
        if isinstance(self.structure, int):
            raise ValueError('Cannot build submodel for one criterion.')

        self.model = COMET(
                cvalues=[submodels[sm].cvalues for sm in self.structure],
                expert_function=self.expert_function
                )

    def __call__(self, matrix, results):
        if isinstance(self.structure, int):
            return matrix[:, self.structure]

        if self.model:
            return self.model(np.array([results[struct]
                                        for struct in self.structure]).T)

        raise ValueError('Model is not build!')


class StructuralCOMET(MCDA_method):
    """ Create Structural COMET model with defined structure [#struct1]_.

        Parameters
        ----------
            submodels : list of Submodel objects
                List of the submodels which defines structure of the model.
                See example for more details.

            cvalues : list of lists
                Characteristic values for criteria.

            criteria_names : list or None
                Names of the criteria

        References
        ----------
        .. [#struct1] Shekhovtsov, A., Kołodziejczyk, J., & Sałabun, W. (2020). Fuzzy model identification using monolithic and structured approaches in decision problems with partially incomplete data. Symmetry, 12(9), 1541.

        Examples
        --------
        See examples/comet_tool_examples.ipynb for example with explanation.
    """
    def __init__(self,
                 submodels,
                 cvalues,
                 criteria_names=None):
        if criteria_names is not None and len(cvalues) != len(criteria_names):
            raise ValueError('Length of cvalues and cvalues_names should be equal')

        self.cvalues = cvalues
        # This dict will be used to map name
        # to structure and other way around
        self._name_struct_mapper = {}
        # Build every submodel, even for each criterion alone
        self._submodels = {}
        for struct, (n, c) in enumerate(zip(criteria_names, cvalues)):
            self._name_struct_mapper[n] = struct
            self._name_struct_mapper[struct] = n
            self._submodels[struct] = Submodel(name=n,
                                               structure=struct,
                                               cvalues=c,
                                               expert_function=None)

        for submodel in submodels:
            clear_structure = self.all_to_structures(submodel.structure)

            self._name_struct_mapper[submodel.name] = clear_structure
            self._name_struct_mapper[clear_structure] = submodel.name
            submodel.structure = clear_structure

            submodel.build(self._submodels)
            self._submodels[clear_structure] = submodel

            # Submodel without cvaluese is considered final
            if submodel.cvalues is None:
                self._final_submodel_struct = submodel.structure

    def __call__(self, matrix,
                 weights=None,
                 types=None,
                 validation=False,
                 verbose=False):
        """Rank alternatives from decision matrix `matrix`.

            Parameters
            ----------
                matrix : ndarray
                    Decision matrix / alternatives data.
                    Alternatives are in rows and Criteria are in columns.

                weights : None
                    Not used in the StructuralCOMET method.

                types : None
                    Not used in the StructuralCOMET method.

                validation : bool
                    Not used in the StructuralCOMET method.

                verbose : bool
                    If explained_call is True, then results of all submodels will be returned.
        """
        results = {}
        for struct, submodel in self._submodels.items():
            results[struct] = submodel(matrix, results)

        if not verbose:
            return results[self._final_submodel_struct]

        return MCDA_results(
            method=self,
            matrix=matrix,
            results=[TableDesc(caption=(name := self._name_struct_mapper[struct]),
                               label=name, symbol=name, rows='A', cols=None).create_table(res)
                     for struct, res in results.items() if not isinstance(struct, int)]
        )

    def _method(self, matrix, weights, types):
        pass

    def __getitem__(self, structure):
        return self._submodels[self.all_to_structures(structure)]

    def __len__(self):
        return len(self._submodels)

    def all_to_structures(self, structure):
        if isinstance(structure, str):
            return self._name_struct_mapper[structure]

        return tuple((
            self._name_struct_mapper[s] if isinstance(s, str) else s
            for s in structure
            ))

    def all_to_names(self, structure):
        if isinstance(structure, int):
            return self._name_struct_mapper[structure]

        return tuple((
            s if isinstance(s, str) else self._name_struct_mapper[s]
            for s in structure
            ))
