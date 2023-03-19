import numpy as np

from ..methods import COMET

class Submodel:
    def __init__(self,
                 structure, # Should be a value
                 cvalues, # Could be None if it is final submodel
                 expert_function, # Could be None if structure is int
                 name, # If we do not provide name we should put in some generic one
                 ):
        self.cvalues = cvalues
        self.structure = structure

        if name is None:
            self.name = str(structure)
        else:
            self.name=name

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


class StructuralCOMET:
    def __init__(self,
                 submodels,
                 cvalues,
                 criteria_names=None):
        if criteria_names is not None and len(cvalues) != len(criteria_names):
            raise ValueError('Length of cvalues and cvalues_names should be equal')

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
                self._final_submodel_struct =  submodel.structure

    def __call__(self, matrix, return_all=False, use_names=True):
        results = {}
        for struct, submodel in self._submodels.items():
            results[struct] = submodel(matrix, results)

        if not return_all:
            return results[self._final_submodel_struct]

        if use_names:
            return {self._name_struct_mapper[struct]: res
                    for struct, res in results.items()}

        return results

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
