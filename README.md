<h1 align="center">
<img src="https://raw.githubusercontent.com/kotbaton/pymcdm/master/branding/logo_text.svg" width="300">
</h1><br>

[![github](https://img.shields.io/badge/github-repo-000.svg?logo=github&labelColor=gray&color=blue)](https://github.com/kotbaton/pymcdm)
[![Version](https://img.shields.io/pypi/v/pymcdm)](https://pypi.org/project/pymcdm/)
[![ReadTheDocs](https://img.shields.io/readthedocs/pymcdm)](https://pymcdm.readthedocs.io/en/latest/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://img.shields.io/badge/DOI-10.1016%2Fj.softx.2023.101368-000.svg?color=blue)](https://doi.org/10.1016/j.softx.2023.101368)

**Important:** Development process was moved from [GitLab](https://gitlab.com/shekhand/mcda) to [Github](https://github.com/kotbaton/pymcdm).

# PyMCDM

Python 3 library for solving multi-criteria decision-making (MCDM) problems.

Documentation is avaliable on [readthedocs](https://pymcdm.readthedocs.io/en/master/).

___

# Installation

You can download and install `pymcdm` library using pip:

```Bash
pip install pymcdm
```

You can run all tests with following command from the root of the project:

```Bash
python -m unittest -v
```

___

# Citing pymcdm

If usage of the pymcdm library lead to a scientific publication, please 
acknowledge this fact by citing "[_Kizielewicz, B., Shekhovtsov, A., 
& Sałabun, W. (2023). pymcdm—The universal library for solving multi-criteria 
decision-making problems. SoftwareX, 22, 101368._](https://doi.org/10.1016/j.softx.2023.101368)"

Or using BibTex:
```bibtex
@article{kizielewicz2023pymcdm,
  title={pymcdm—The universal library for solving multi-criteria decision-making problems},
  author={Kizielewicz, Bart{\l}omiej and Shekhovtsov, Andrii and Sa{\l}abun, Wojciech},
  journal={SoftwareX},
  volume={22},
  pages={101368},
  year={2023},
  publisher={Elsevier}
}
```

DOI: [https://doi.org/10.1016/j.softx.2023.101368](https://doi.org/10.1016/j.softx.2023.101368)

___

# Available methods

The library contains:

* MCDA methods:

| Acronym            	  | Method Name                                                                                          |               Reference                |
|:----------------------|------------------------------------------------------------------------------------------------------|:--------------------------------------:|
| TOPSIS             	  | Technique for the Order of Prioritisation by Similarity to Ideal Solution                            |               [[1]](#c1)               |
| VIKOR              	  | VIseKriterijumska Optimizacija I Kompromisno Resenje                                                 |               [[2]](#c2)               |
| COPRAS             	  | COmplex PRoportional ASsessment                                                                      |               [[3]](#c3)               |
| PROMETHEE I & II   	  | Preference Ranking Organization METHod for Enrichment of Evaluations I & II                          |               [[4]](#c4)               |
| COMET              	  | Characteristic Objects Method                                                                        |               [[5]](#c5)               |
| SPOTIS             	  | Stable Preference Ordering Towards Ideal Solution                                                    |               [[6]](#c6)               |
| ARAS               	  | Additive Ratio ASsessment                                                                            |         [[7]](#c7),[[8]](#c8)          |
| COCOSO             	  | COmbined COmpromise SOlution                                                                         |               [[9]](#c9)               |
| CODAS              	  | COmbinative Distance-based ASsessment                                                                |              [[10]](#c10)              |
| CRADIS             	  | Compromise Ranking of Alternatives from Distance to Ideal Solution                                   |             [[102]](#c102)             |
| EDAS               	  | Evaluation based on Distance from Average Solution                                                   |       [[11]](#c11),[[12]](#c12)        |
| MABAC              	  | Multi-Attributive Border Approximation area Comparison                                               |              [[13]](#c13)              |
| MAIRCA             	  | MultiAttributive Ideal-Real Comparative Analysis                                                     | [[14]](#c14),[[15]](#c15),[[16]](#c16) |
| MARCOS             	  | Measurement Alternatives and Ranking according to COmpromise Solution                                |       [[17]](#c17),[[18]](#c18)        |
| OCRA               	  | Operational Competitiveness Ratings                                                                  |       [[19]](#c19),[[20]](#c20)        |
| PIV                   | Proximity Indexed Value                                                                              |             [[114]](#c114)             |
| MOORA              	  | Multi-Objective Optimization Method by Ratio Analysis                                                |       [[21]](#c21),[[22]](#c22)        |
| MULTIMOORA         	  | MOORA plus the Full Multiplicative Form with the dominance theory                                    |       [[99]](#c99),[[100]](#c100)        |
| RIM                	  | Reference Ideal Method                                                                               |              [[47]](#c47)              |
| ERVD               	  | Election Based on relative Value Distances                                                           |              [[48]](#c48)              |
| GRA                	  | Grey Relational Analysis                                                                             |             [[103]](#c103)             |
| HELLWIG            	  | Hellwig's taxonomic measure of development (Euclidean or Mahalanobis distance)                       |     [[107]](#c107),[[108]](#c108)      |
| MIDIA              	  | Multi-criteria method Integrating Distances to Ideal and Anti-ideal points                           |             [[109]](#c109)             |
| DARP               	  | Distances to Aspiration Reference Points                                                             |             [[110]](#c110)             |
| RPM                	  | Reference Point Method (objective ranking)                                                           |     [[111]](#c111),[[112]](#c112)      |
| PROBID                | Preference Ranking On the Basis of Ideal-average Distance                                            |              [[49]](#c49)              |
| WSM                   | Weighted Sum Model                                                                                   |              [[50]](#c50)              |
| WPM                   | Weighted Product Model                                                                               |              [[50]](#c50)              |
| WASPAS                | Weighted Aggregated Sum Product ASSessment                                                           |              [[51]](#c51)              |
| RAM                	  | Root Assesment Method                                                                                |              [[60]](#c60)              |
| RAFSI                 | Ranking of Alternatives through Functional mapping of criterion sub-intervals into a Single Interval |              [[67]](#c67)              |
| LoPM                	 | Limits on Property Method                                                                            |              [[65]](#c65)              |
| LMAW                  | Logarithmic Methodology of Additive Weights                                                          |              [[68]](#c68)               | 
| AROMAN                | Alternative Ranking Order Method Accounting for Two-Step Normalization)                              |              [[70]](#c70)               |
| TODIM                 | TOmada de Decisão Interativa e Multicritério                                                         |       [[73]](#c73),[[74]](#c74),[[75]](#c75),[[76]](#c76)         |
| ELECTRE TRI           | ELimination Et Choix Traduisant la REalité TRI (sorting into ordered categories)                     |       [[96]](#c96),[[97]](#c97)      |

* MCDA Methods' extensions and variations:

| Acronym       	|    Reference         	    |
|:-----------------|:-------------------------:|
| Balanced SPOTIS	|   [[66]](#c66)       	    |
| R-TOPSIS        	|   [[77]](#c77)       	    |
| NR-TOPSIS\* | [[90]](#c90) |
| TOPSIS (García-Cascales & Lamata)\* | [[91]](#c91) |
| IE-TOPSIS (domain)\* | [[92]](#c92) |
| TOPSIS-RAD\* | [[93]](#c93) |
| BP-TOPSIS\* | [[113]](#c113) |
| TOPSIS-Sort-B, TOPSIS-Sort-C (sorting) | [[98]](#c98) |
| R-VIKOR | [[101]](#c101) |

\* Obtained with the parameters of R-TOPSIS (`RTOPSIS`), see its documentation. For IE-TOPSIS only the expansion of
the criteria domains is available; its PRC ranking index, which depends on the whole set of alternatives, is not
implemented.

* Weighting methods:

| Acronym | Method Name                                               |                Reference                 |
|:--------|:----------------------------------------------------------|:----------------------------------------:|
| -       | Equal/Mean weights                                        |               [[23]](#c23)               |
| -       | Entropy weights                                           | [[23]](#c23), [[24]](#c24), [[25]](#c25) |
| STD     | Standard Deviation weights                                |        [[23]](#c23), [[26]](#c26)        |
| MEREC   | MEthod based on the Removal Effects of Criteria           |               [[27]](#c27)               |
| CRITIC  | CRiteria Importance Through Intercriteria Correlation     |        [[28]](#c28), [[29]](#c29)        |
| CILOS   | Criterion Impact LOS                                      |               [[30]](#c30)               |
| IDOCRIW | Integrated Determination of Objective CRIteria Weight     |               [[30]](#c30)               |
| LOPCOW  | LOgarithmic Percentage Change-driven Objective Weighting  |               [[69]](#c69)               |
| PSI     | Preference Selection Index                                |              [[104]](#c104)              |
| -       | Angular/Angle weights                                     |               [[31]](#c31)               |
| -       | Gini Coeficient weights                                   |               [[32]](#c32)               |
| -       | Statistical variance weights                              |               [[33]](#c33)               |
| AHP     | Analytic Hierarchy Process                                |        [[63]](#c63), [[78]](#c78)        |
| RANCOM  | RANking COMparison                                        |               [[64]](#c64)               |
| SWARA   | Step-wise Weight Assessment Ratio Analysis                |               [[79]](#c79)               |
| PIPRECIA | PIvot Pairwise RElative Criteria Importance Assessment    |        [[80]](#c80), [[94]](#c94)        |
| FUCOM   | FUll COnsistency Method                                   |               [[81]](#c81)               |
| BWM     | Best-Worst Method                                         |        [[82]](#c82), [[95]](#c95)        |
| BCM     | Base-Criterion Method                                     |               [[83]](#c83)               |
| LBWA    | Level Based Weight Assessment                             |               [[84]](#c84)               |
| SIMOS   | Simos procedure (cards method)                            |               [[85]](#c85)               |
| SRF     | Simos-Roy-Figueira (revised Simos procedure)              |               [[85]](#c85)               |
| VIMM    | Vital-Immaterial-Mediocre Method                          |               [[86]](#c86)               |
| COBRAC  | COmparisons Between RAnked Criteria                       |               [[87]](#c87)               |
| ITARA   | Indifference Threshold-based Attribute RAtio Analysis     |               [[88]](#c88)               |
| OWCM    | Opinion Weight Criteria Method                            |               [[89]](#c89)               |
| ROC     | Rank Order Centroid                                       |              [[105]](#c105)              |
| RS      | Rank Sum                                                  |              [[106]](#c106)              |
| RR      | Rank Reciprocal                                           |              [[106]](#c106)              |
| RE      | Rank Exponent                                             |              [[106]](#c106)              |

* Normalization methods:

| Method Name                          	 |     Reference         	     |
|:---------------------------------------|:---------------------------:|
| Weitendorf’s Linear Normalization    	 |    [[34]](#c34)        	    |
| Maximum - Linear Normalization       	 |    [[35]](#c35)        	    |
| Sum-Based Linear Normalization       	 |    [[36]](#c36)        	    |
| Vector Normalization                 	 | [[36]](#c36),[[37]](#c37) 	 |
| Logarithmic Normalization            	 | [[36]](#c36),[[37]](#c37) 	 |
| Linear Normalization (Max-Min)       	 | [[34]](#c34),[[35]](#c35) 	 |
| Non-linear Normalization (Max-Min)   	 |    [[38]](#c38)        	    |
| Enhanced Accuracy Normalization      	 |    [[39]](#c39)        	    |
| Lai and Hwang Normalization            |        [[35]](#c35)         |
| Zavadskas and Turskis Normalization    |        [[35]](#c35)         |

* Correlation coefficients:

| Coefficient name                                   	 |     Reference         	     |
|------------------------------------------------------|:---------------------------:|
| Spearman's rank correlation coefficient            	 | [[40]](#c40),[[41]](#c41) 	 |
| Pearson correlation coefficient                    	 |    [[42]](#c42)       	     |
| Weighted Spearman’s rank correlation coefficient   	 |    [[43]](#c43)       	     |
| Rank Similarity Coefficient                        	 |    [[44]](#c44)       	     |
| Kendall rank correlation coefficient               	 |    [[45]](#c45)       	     |
| Goodman and Kruskal's gamma                        	 |    [[46]](#c46)       	     |
| Drastic Weighted Similarity (draWS)                  |    [[57]](#c57)       	     |
| Weights Similarity Coefficient (WSC)                 |    [[58]](#c58)       	     |
| Weights Similarity Coefficient 2 (WSC2)              |    [[58]](#c58)       	     |

* Distance metrics:

| Metric Name                    	 |  Reference           |
|-----------------------------------|:--------------------:|
| Kemeny distance              	 |    [[71]](#c71) 	    |
| Frobenius distance              	 |    [[72]](#c72) 	    |
| draWS distance              	     |    [[57]](#c57) 	    |

* Helpers

| Helpers submodule    | Description                                                                                                      |
|----------------------|------------------------------------------------------------------------------------------------------------------|
| `rankdata`           | Create ranking vector from the preference vector. Smaller preference values has higher positions in the ranking. |
| `rrankdata`          | Alias to the `rankdata` which reverse the sorting order.                                                         |
| `correlation_matrix` | Create the correlation matrix for given coefficient from several the several rankings.                           |
| `normalize_matrix`   | Normalize decision matrix column by column using given normalization and criteria types.                         |

* COMET Tools

| Class/Function       | Description                                                                                        |  Reference   |
|----------------------|----------------------------------------------------------------------------------------------------|:------------:|
| `MethodExpert`       | Class which allows to evaluate CO in COMET using any MCDA method.                                  | [[54]](#c54) |
| `ManualExpert`       | Class which allows to evaluate CO in COMET manually by pairwise comparisons.                       | [[55]](#c55) |
| `FunctionExpert`     | Class which allows to evaluate CO in COMET using any expert function.                              | [[56]](#c56) |
| `CompromiseExpert`   | Class which allows to evaluate CO in COMET using compromise between several different methods.     | [[61]](#c61) |
| `TriadSupportExpert` | Class which allows to evaluate CO in COMET manually but with triads support.                       | [[62]](#c62) |
| `ESPExpert`          | Class which allows to identify MEJ using expert-defined Expected Solution Points.                  | [[59]](#c59) |
| `triads_consistency` | Function to which evaluates consistency of the MEJ matrix.                                         | [[53]](#c53) |
| `Submodel`           | Class mostly for internal use in StructuralCOMET class.                                            | [[52]](#c52) |
| `StructuralCOMET`    | Class which allows to split a decision problem into submodels to be evaluated by the COMET method. | [[52]](#c52) |

___
# Usage example

Here's a small example of how use this library to solve MCDM problem.
For more examples with explanation see [examples](https://gitlab.com/shekhand/mcda/-/blob/master/examples/examples.ipynb).

```python
import numpy as np
from pymcdm.methods import TOPSIS
from pymcdm.helpers import rrankdata

# Define decision matrix (3 criteria, 4 alternative)
alts = np.array([
    [4, 4, 0.2],
    [1, 5, 0.5],
    [3, 2, 0.3],
    [4, 3, 0.5]
])

# Define criteria weights (should sum up to 1)
weights = np.array([0.3, 0.5, 0.2])

# Define criteria types (1 for profit, -1 for cost)
types = np.array([1, -1, 1])

# Create object of the method
# Note, that default normalization method for TOPSIS is minmax
topsis = TOPSIS()

# Determine preferences and ranking for alternatives
pref = topsis(alts, weights, types)
ranking = rrankdata(pref)

for r, p in zip(ranking, pref):
    print(r, p)
```

And the output of this example (numbers are rounded):

```bash
3.0 0.469
4.0 0.255
1.0 0.765
2.0 0.747
```

If you want to inspect computation process in details, you can add the following code to the above example:

```python
results = topsis(alts, weights, types, verbose=True)
print(results)
```

This will produce output that contains formatted decision matrix, intermediate results, preference values and ranking.

---
# References

<a name="c1">[1]</a> Hwang, C. L., & Yoon, K. (1981). Methods for multiple attribute decision making. In Multiple attribute decision making (pp. 58-191). Springer, Berlin, Heidelberg. https://doi.org/10.1007/978-3-642-48318-9_3

<a name="c2">[2]</a> Duckstein, L., & Opricovic, S. (1980). Multiobjective optimization in river basin development. Water resources research, 16(1), 14-20. https://doi.org/10.1029/WR016i001p00014

<a name="c3">[3]</a> Zavadskas, E. K., Kaklauskas, A., Peldschus, F., & Turskis, Z. (2007). Multi-attribute assessment of road design solutions by using the COPRAS method. The Baltic Journal of Road and Bridge Engineering, 2(4), 195-203.

<a name="c4">[4]</a> Brans, J. P., Vincke, P., & Mareschal, B. (1986). How to select and how to rank projects: The PROMETHEE method. European journal of operational research, 24(2), 228-238. https://doi.org/10.1016/0377-2217(86)90044-5

<a name="c5">[5]</a> Sałabun, W., Karczmarczyk, A., Wątróbski, J., & Jankowski, J. (2018, November). Handling data uncertainty in decision making with COMET. In 2018 IEEE Symposium Series on Computational Intelligence (SSCI) (pp. 1478-1484). IEEE. https://doi.org/10.1109/SSCI.2018.8628934

<a name="c6">[6]</a> Dezert, J., Tchamova, A., Han, D., & Tacnet, J. M. (2020, July). The spotis rank reversal free method for multi-criteria decision-making support. In 2020 IEEE 23rd International Conference on Information Fusion (FUSION) (pp. 1-8). IEEE. https://doi.org/10.23919/FUSION45008.2020.9190347

<a name="c7">[7]</a> Zavadskas, E. K., & Turskis, Z. (2010). A new additive ratio assessment (ARAS) method in multicriteria decision‐making. Technological and economic development of economy, 16(2), 159-172. https://doi.org/10.3846/tede.2010.10

<a name="c8">[8]</a> Stanujkic, D., Djordjevic, B., & Karabasevic, D. (2015). Selection of candidates in the process of recruitment and selection of personnel based on the SWARA and ARAS methods. Quaestus, (7), 53.

<a name="c9">[9]</a> Yazdani, M., Zarate, P., Zavadskas, E. K., & Turskis, Z. (2019). A Combined Compromise Solution (CoCoSo) method for multi-criteria decision-making problems. Management Decision. https://doi.org/10.1108/MD-05-2017-0458

<a name="c10">[10]</a> Badi, I., Shetwan, A. G., & Abdulshahed, A. M. (2017, September). Supplier selection using COmbinative Distance-based ASsessment (CODAS) method for multi-criteria decision-making. In Proceedings of The 1st International Conference on Management, Engineering and Environment (ICMNEE) (pp. 395-407).

<a name="c11">[11]</a> Keshavarz Ghorabaee, M., Zavadskas, E. K., Olfat, L., & Turskis, Z. (2015). Multi-criteria inventory classification using a new method of evaluation based on distance from average solution (EDAS). Informatica, 26(3), 435-451. https://doi.org/10.15388/Informatica.2015.57

<a name="c12">[12]</a> Yazdani, M., Torkayesh, A. E., Santibanez-Gonzalez, E. D., & Otaghsara, S. K. (2020). Evaluation of renewable energy resources using integrated Shannon Entropy—EDAS model. Sustainable Operations and Computers, 1, 35-42. https://doi.org/10.1016/j.susoc.2020.12.002

<a name="c13">[13]</a> Pamučar, D., & Ćirović, G. (2015). The selection of transport and handling resources in logistics centers using Multi-Attributive Border Approximation area Comparison (MABAC). Expert systems with applications, 42(6), 3016-3028. https://doi.org/10.1016/j.eswa.2014.11.057

<a name="c14">[14]</a> Gigović, L., Pamučar, D., Bajić, Z., & Milićević, M. (2016). The combination of expert judgment and GIS-MAIRCA analysis for the selection of sites for ammunition depots. Sustainability, 8(4), 372. https://doi.org/10.3390/su8040372

<a name="c15">[15]</a> Pamucar, D. S., Pejcic Tarle, S., & Parezanovic, T. (2018). New hybrid multi-criteria decision-making DEMATELMAIRCA model: sustainable selection of a location for the development of multimodal logistics centre. Economic research-Ekonomska istraživanja, 31(1), 1641-1665. https://doi.org/10.1080/1331677X.2018.1506706

<a name="c16">[16]</a> Aksoy, E. (2021). An Analysis on Turkey's Merger and Acquisition Activities: MAIRCA Method. Gümüşhane Üniversitesi Sosyal Bilimler Enstitüsü Elektronik Dergisi, 12(1), 1-11.

<a name="c17">[17]</a> Stević, Ž., Pamučar, D., Puška, A., & Chatterjee, P. (2020). Sustainable supplier selection in healthcare industries using a new MCDM method: Measurement of alternatives and ranking according to COmpromise solution (MARCOS). Computers & Industrial Engineering, 140, 106231. https://doi.org/10.1016/j.cie.2019.106231

<a name="c18">[18]</a> Ulutaş, A., Karabasevic, D., Popovic, G., Stanujkic, D., Nguyen, P. T., & Karaköy, Ç. (2020). Development of a novel integrated CCSD-ITARA-MARCOS decision-making approach for stackers selection in a logistics system. Mathematics, 8(10), 1672. https://doi.org/10.3390/math8101672

<a name="c19">[19]</a> Parkan, C. (1994). Operational competitiveness ratings of production units. Managerial and Decision Economics, 15(3), 201-221. https://doi.org/10.1002/mde.4090150303

<a name="c20">[20]</a> Işık, A. T., & Adalı, E. A. (2016). A new integrated decision making approach based on SWARA and OCRA methods for the hotel selection problem. International Journal of Advanced Operations Management, 8(2), 140-151. https://doi.org/10.1504/IJAOM.2016.079681

<a name="c21">[21]</a> Brauers, W. K. (2004). Optimization methods for a stakeholder society: a revolution in economic thinking by multi-objective optimization (Vol. 73). Springer Science & Business Media. https://doi.org/10.1007/978-1-4419-9178-2

<a name="c22">[22]</a> Hussain, S. A. I., & Mandal, U. K. (2016). Entropy based MCDM approach for Selection of material. In National Level Conference on Engineering Problems and Application of Mathematics (pp. 1-6).

<a name="c23">[23]</a> Sałabun, W., Wątróbski, J., & Shekhovtsov, A. (2020). Are mcda methods benchmarkable? a comparative study of topsis, vikor, copras, and promethee ii methods. Symmetry, 12(9), 1549. https://doi.org/10.3390/sym12091549

<a name="c24">[24]</a> Lotfi, F. H., & Fallahnejad, R. (2010). Imprecise Shannon’s entropy and multi attribute decision making. Entropy, 12(1), 53-62. https://doi.org/10.3390/e12010053

<a name="c25">[25]</a> Li, X., Wang, K., Liu, L., Xin, J., Yang, H., & Gao, C. (2011). Application of the entropy weight and TOPSIS method in safety evaluation of coal mines. Procedia engineering, 26, 2085-2091. https://doi.org/10.1016/j.proeng.2011.11.2410

<a name="c26">[26]</a> Wang, Y. M., & Luo, Y. (2010). Integration of correlations with standard deviations for determining attribute weights in multiple attribute decision making. Mathematical and Computer Modelling, 51(1-2), 1-12. https://doi.org/10.1016/j.mcm.2009.07.016

<a name="c27">[27]</a> Keshavarz-Ghorabaee, M., Amiri, M., Zavadskas, E. K., Turskis, Z., & Antucheviciene, J. (2021). Determination of Objective Weights Using a New Method Based on the Removal Effects of Criteria (MEREC). Symmetry, 13(4), 525. https://doi.org/10.3390/sym13040525

<a name="c28">[28]</a> Diakoulaki, D., Mavrotas, G., & Papayannakis, L. (1995). Determining objective weights in multiple criteria problems: The critic method. Computers & Operations Research, 22(7), 763-770. https://doi.org/10.1016/0305-0548(94)00059-H

<a name="c29">[29]</a> Tuş, A., & Adalı, E. A. (2019). The new combination with CRITIC and WASPAS methods for the time and attendance software selection problem. Opsearch, 56(2), 528-538. https://doi.org/10.1007/s12597-019-00371-6

<a name="c30">[30]</a> Zavadskas, E. K., & Podvezko, V. (2016). Integrated determination of objective criteria weights in MCDM. International Journal of Information Technology & Decision Making, 15(02), 267-283. https://doi.org/10.1142/S0219622016500036

<a name="c31">[31]</a> Shuai, D., Zongzhun, Z., Yongji, W., & Lei, L. (2012, May). A new angular method to determine the objective weights. In 2012 24th Chinese Control and Decision Conference (CCDC) (pp. 3889-3892). IEEE. https://doi.org/10.1109/CCDC.2012.6244621

<a name="c32">[32]</a> Li, G., & Chi, G. (2009, December). A new determining objective weights method-gini coefficient weight. In 2009 First International Conference on Information Science and Engineering (pp. 3726-3729). IEEE. https://doi.org/10.1109/ICISE.2009.84

<a name="c33">[33]</a> Rao, R. V., & Patel, B. K. (2010). A subjective and objective integrated multiple attribute decision making method for material selection. Materials & Design, 31(10), 4738-4747. https://doi.org/10.1016/j.matdes.2010.05.014

<a name="c34">[34]</a> Brauers, W. K., & Zavadskas, E. K. (2006). The MOORA method and its application to privatization in a transition economy. Control and cybernetics, 35, 445-469.

<a name="c35">[35]</a> Jahan, A., & Edwards, K. L. (2015). A state-of-the-art survey on the influence of normalization techniques in ranking: Improving the materials selection process in engineering design. Materials & Design (1980-2015), 65, 335-342. https://doi.org/10.1016/j.matdes.2014.09.022

<a name="c36">[36]</a> Gardziejczyk, W., & Zabicki, P. (2017). Normalization and variant assessment methods in selection of road alignment variants–case study. Journal of civil engineering and management, 23(4), 510-523. https://doi.org/10.3846/13923730.2016.1210223

<a name="c37">[37]</a> Zavadskas, E. K., & Turskis, Z. (2008). A new logarithmic normalization method in games theory. Informatica, 19(2), 303-314. https://doi.org/10.15388/Informatica.2008.215

<a name="c38">[38]</a> Peldschus, F., Vaigauskas, E., & Zavadskas, E. K. (1983). Technologische entscheidungen bei der berücksichtigung mehrerer Ziehle. Bauplanung Bautechnik, 37(4), 173-175.

<a name="c39">[39]</a> Zeng, Q. L., Li, D. D., & Yang, Y. B. (2013). VIKOR method with enhanced accuracy for multiple criteria decision making in healthcare management. Journal of medical systems, 37(2), 1-9. https://doi.org/10.1007/s10916-012-9908-1

<a name="c40">[40]</a> Binet, A., & Henri, V. (1898). La fatigue intellectuelle (Vol. 1). Schleicher frères.

<a name="c41">[41]</a> Spearman, C. (1910). Correlation calculated from faulty data. British Journal of Psychology, 1904‐1920, 3(3), 271-295. https://doi.org/10.1111/j.2044-8295.1910.tb00206.x

<a name="c42">[42]</a> Pearson, K. (1895). VII. Note on regression and inheritance in the case of two parents. proceedings of the royal society of London, 58(347-352), 240-242. https://doi.org/10.1098/rspl.1895.0041

<a name="c43">[43]</a> Dancelli, L., Manisera, M., & Vezzoli, M. (2013). On two classes of Weighted Rank Correlation measures deriving from the Spearman’s ρ. In Statistical Models for Data Analysis (pp. 107-114). Springer, Heidelberg. https://doi.org/10.1007/978-3-319-00032-9_13

<a name="c44">[44]</a> Sałabun, W., & Urbaniak, K. (2020, June). A new coefficient of rankings similarity in decision-making problems. In International Conference on Computational Science (pp. 632-645). Springer, Cham. https://doi.org/10.1007/978-3-030-50417-5_47

<a name="c45">[45]</a> Kendall, M. G. (1938). A new measure of rank correlation. Biometrika, 30(1/2), 81-93. https://doi.org/10.1093/biomet/30.1-2.81

<a name="c46">[46]</a> Goodman, L. A., & Kruskal, W. H. (1979). Measures of association for cross classifications. Measures of association for cross classifications, 2-34. https://doi.org/10.1007/978-1-4612-9995-0

<a name="c47">[47]</a> Cables, E., Lamata, M. T., & Verdegay, J. L. (2016). RIM-reference ideal method in multicriteria decision making. Information Sciences, 337, 1-10. https://doi.org/10.1016/j.ins.2015.12.011

<a name="c48">[48]</a> Shyur, H. J., Yin, L., Shih, H. S., & Cheng, C. B. (2015). A multiple criteria decision making method based on relative value distances. Foundations of Computing and Decision Sciences, 40(4), 299-315. https://doi.org/10.1515/fcds-2015-0017

<a name="c49">[49]</a> Wang, Z., Rangaiah, G. P., & Wang, X. (2021). Preference ranking on the basis of ideal-average distance method for multi-criteria decision-making. Industrial & Engineering Chemistry Research, 60(30), 11216-11230. https://doi.org/10.1021/acs.iecr.1c01413

<a name="c50">[50]</a> Fishburn, P. C., Murphy, A. H., & Isaacs, H. H. (1968). Sensitivity of decisions to probability estimation errors: A reexamination. Operations Research, 16(2), 254-267. https://doi.org/10.1287/opre.16.2.254

<a name="c51">[51]</a> Zavadskas, E. K., Turskis, Z., Antucheviciene, J., & Zakarevicius, A. (2012). Optimization of weighted aggregated sum product assessment. Elektronika ir elektrotechnika, 122(6), 3-6. https://doi.org/10.5755/j01.eee.122.6.1810

<a name="c52">[52]</a> Shekhovtsov, A., Kołodziejczyk, J., & Sałabun, W. (2020). Fuzzy model identification using monolithic and structured approaches in decision problems with partially incomplete data. Symmetry, 12(9), 1541. https://doi.org/10.3390/sym12091541

<a name="c53">[53]</a> Sałabun, W., Shekhovtsov, A., & Kizielewicz, B. (2021, June). A new consistency coefficient in the multi-criteria decision analysis domain. In Computational Science–ICCS 2021: 21st International Conference, Krakow, Poland, June 16–18, 2021, Proceedings, Part I (pp. 715-727). Cham: Springer International Publishing. https://doi.org/10.1007/978-3-030-77961-0_57

<a name="c54">[54]</a> Paradowski, B., Bączkiewicz, A., & Watrąbski, J. (2021). Towards proper consumer choices-MCDM based product selection. Procedia Computer Science, 192, 1347-1358. https://doi.org/10.1016/j.procs.2021.08.138

<a name="c55">[55]</a> Sałabun, W. (2015). The characteristic objects method: A new distance‐based approach to multicriteria decision‐making problems. Journal of Multi‐Criteria Decision Analysis, 22(1-2), 37-50. https://doi.org/10.1002/mcda.1525

<a name="c56">[56]</a> Sałabun, W., & Piegat, A. (2017). Comparative analysis of MCDM methods for the assessment of mortality in patients with acute coronary syndrome. Artificial Intelligence Review, 48, 557-571. https://doi.org/10.1007/s10462-016-9511-9

<a name="c57">[57]</a> Sałabun, W., & Shekhovtsov, A. (2023, September). An Innovative Drastic Metric for Ranking Similarity in Decision-Making Problems. In 2023 18th Conference on Computer Science and Intelligence Systems (FedCSIS) (pp. 731-738). IEEE. https://doi.org/10.15439/2023F6502

<a name="c58">[58]</a> Shekhovtsov, A. (2023). Evaluating the Performance of Subjective Weighting Methods for Multi-Criteria Decision-Making using a novel Weights Similarity Coefficient. Procedia Computer Science, 225, 4785-4794. https://doi.org/10.1016/j.procs.2023.10.478

<a name="c59">[59]</a> Shekhovtsov, A., Kizielewicz, B., & Sałabun, W. (2023). Advancing individual decision-making: An extension of the characteristic objects method using expected solution point. Information Sciences, 647, 119456. https://doi.org/10.1016/j.ins.2023.119456

<a name="c60">[60]</a> Sotoudeh-Anvari, A. (2023). Root Assessment Method (RAM): a novel multi-criteria decision making method and its applications in sustainability challenges. Journal of Cleaner Production, 423, 138695. https://doi.org/10.1016/j.jclepro.2023.138695

<a name="c61">[61]</a> Kizielewicz, B., Shekhovtsov, A., Więckowski, J., Wątróbski, J., & Sałabun, W. (2024). The Compromise-COMET method for identifying an adaptive multi-criteria decision model. IEEE Access, 12, 157083-157106. https://doi.org/10.1109/ACCESS.2024.3485798

<a name="c62">[62]</a> Shekhovtsov, A., & Sałabun, W. (2024). The New Algorithm for Effective Reducing the Number of Pairwise Comparisons in the Decision Support Methods. In M. Hernes & J. Wątróbski (Eds.), Emerging Challenges in Intelligent Management Information Systems (IMIS@ECAI 2023), Lecture Notes in Networks and Systems, 1079 (pp. 243-254). Springer, Cham. https://doi.org/10.1007/978-3-031-66761-9_20

<a name="c63">[63]</a> Saaty, T. L. (1980). The Analytic Hierarchy Process. McGraw-Hill, New York.

<a name="c64">[64]</a> Więckowski, J., Kizielewicz, B., Shekhovtsov, A., & Sałabun, W. (2023). RANCOM: A novel approach to identifying criteria relevance based on inaccuracy expert judgments. Engineering Applications of Artificial Intelligence, 122, 106114. https://doi.org/10.1016/j.engappai.2023.106114

<a name="c65">[65]</a> Farag, M. M. (2020). Materials and process selection for engineering design (4th ed.). CRC Press.

<a name="c66">[66]</a> Shekhovtsov, A., Dezert, J. and Sałabun, W. (2025). Enhancing Personalized Decision-Making with the Balanced SPOTIS Algorithm. In Proceedings of the 17th International Conference on Agents and Artificial Intelligence - Volume 3: ICAART; ISBN 978-989-758-737-5; ISSN 2184-433X, SciTePress, pages 264-271. DOI: 10.5220/0013119800003890 https://doi.org/10.5220/0013119800003890

<a name="c67">[67]</a> Žižović, M., Pamučar, D., Albijanić, M., Chatterjee, P., & Pribićević, I. (2020). Eliminating rank reversal problem using a new multi-attribute model—the RAFSI method. Mathematics, 8(6), 1015. https://doi.org/10.3390/math8061015

<a name="c68">[68]</a> Pamučar, D., Žižović, M., Biswas, S., & Božanić, D. (2021). A new logarithm methodology of additive weights (LMAW) for multi-criteria decision-making: Application in logistics. Facta universitatis, series: mechanical engineering, 19(3), 361-380. https://doi.org/10.22190/FUME210214031P

<a name="c69">[69]</a> Ecer, F., & Pamucar, D. (2022). A novel LOPCOW‐DOBI multi‐criteria sustainability performance assessment methodology: An application in developing country banking sector. Omega, 112, 102690. https://doi.org/10.1016/j.omega.2022.102690

<a name="c70">[70]</a> Bošković, S., Švadlenka, L., Jovčić, S., Dobrodolac, M., Simić, V., & Bacanin, N. (2023). An alternative ranking order method accounting for two-step normalization (AROMAN)—A case study of the electric vehicle selection problem. IEEE access, 11, 39496-39507. https://doi.org/10.1109/ACCESS.2023.3265818

<a name="c71">[71]</a> Kemeny, J. G., & Snell, J. L. (1962). Mathematical models in the social sciences. MIT Press.

<a name="c72">[72]</a> Dezert, J., Shekhovtsov, A., & Sałabun, W. (2024). A new distance between rankings. Heliyon, 10, e28265. https://doi.org/10.1016/j.heliyon.2024.e28265

<a name="c73">[73]</a> Dutta, V., & Haldar, S. (2025). Performance Comparison of TODIM and CPT-TODIM in Social Sustainability Assessment for G7 Countries. International Journal of Information Technology & Decision Making. https://doi.org/10.1142/S021962202550097X

<a name="c74">[74]</a> Gomes, L. F. A. M., & Lima, M. M. P. P. (1991). TODIM: Basics and application to multicriteria ranking of projects with environmental impacts. Foundations of Computing and Decision Sciences, 16(4), 113-127.

<a name="c75">[75]</a> Gomes, L. F. A. M., & Rangel, L. A. D. (2009). An application of the TODIM method to the multicriteria rental evaluation of residential properties. European Journal of Operational Research, 193(1), 204–211. https://doi.org/10.1016/j.ejor.2007.10.046

<a name="c76">[76]</a> Gomes, L. F. A. M., Machado, M. A. S., & Rangel, L. A. D. (2013). Behavioral multi-criteria decision analysis: the TODIM method with criteria interactions. Annals of Operations Research, 211(1), 531–548. https://doi.org/10.1007/s10479-013-1345-0

<a name="c77">[77]</a> de Farias Aires, R. F., & Ferreira, L. (2019). A new approach to avoid rank reversal cases in the TOPSIS method. Computers & Industrial Engineering, 132, 84-97. https://doi.org/10.1016/j.cie.2019.04.023

<a name="c78">[78]</a> Crawford, G., & Williams, C. (1985). A note on the analysis of subjective judgment matrices. Journal of Mathematical Psychology, 29(4), 387-405. https://doi.org/10.1016/0022-2496(85)90002-1

<a name="c79">[79]</a> Keršulienė, V., Zavadskas, E. K., & Turskis, Z. (2010). Selection of rational dispute resolution method by applying new step-wise weight assessment ratio analysis (SWARA). Journal of Business Economics and Management, 11(2), 243-258. https://doi.org/10.3846/jbem.2010.12

<a name="c80">[80]</a> Stanujkić, D., Zavadskas, E. K., Karabašević, D., Smarandache, F., & Turskis, Z. (2017). The use of the PIvot Pairwise RElative Criteria Importance Assessment method for determining the weights of criteria. Romanian Journal of Economic Forecasting, 20(4), 116-133.

<a name="c81">[81]</a> Pamučar, D., Stević, Ž., & Sremac, S. (2018). A new model for determining weight coefficients of criteria in MCDM models: Full Consistency Method (FUCOM). Symmetry, 10(9), 393. https://doi.org/10.3390/sym10090393

<a name="c82">[82]</a> Rezaei, J. (2015). Best-worst multi-criteria decision-making method. Omega, 53, 49-57. https://doi.org/10.1016/j.omega.2014.11.009

<a name="c83">[83]</a> Haseli, G., Sheikh, R., & Sana, S. S. (2020). Base-criterion on multi-criteria decision-making method and its applications. International Journal of Management Science and Engineering Management, 15(2), 79-88. https://doi.org/10.1080/17509653.2019.1633964

<a name="c84">[84]</a> Žižović, M., & Pamučar, D. (2019). New model for determining criteria weights: Level Based Weight Assessment (LBWA) model. Decision Making: Applications in Management and Engineering, 2(2), 126-137. https://doi.org/10.31181/dmame1902102z

<a name="c85">[85]</a> Figueira, J., & Roy, B. (2002). Determining the weights of criteria in the ELECTRE type methods with a revised Simos' procedure. European Journal of Operational Research, 139(2), 317-326. https://doi.org/10.1016/S0377-2217(01)00370-8

<a name="c86">[86]</a> Zakeri, S., Ecer, F., Konstantas, D., & Cheikhrouhou, N. (2023). The vital-immaterial-mediocre multi-criteria decision-making method. Kybernetes, 52(3), 937-963. https://doi.org/10.1108/K-05-2021-0403

<a name="c87">[87]</a> Pamucar, D., Simic, V., Gorcun, O. F., & Kucukonder, H. (2024). Selection of the best Big Data platform using COBRAC-ARTASI methodology with adaptive standardized intervals. Expert Systems with Applications, 239, 122312. https://doi.org/10.1016/j.eswa.2023.122312

<a name="c88">[88]</a> Hatefi, M. A. (2019). Indifference threshold-based attribute ratio analysis: A method for assigning the weights to the attributes in multiple attribute decision making. Applied Soft Computing, 74, 643-651. https://doi.org/10.1016/j.asoc.2018.10.050

<a name="c89">[89]</a> Ahmed Mandil, A. D., Salih, M. M., & Muhsen, Y. R. (2024). Opinion Weight Criteria Method (OWCM): A New Method for Weighting Criteria With Zero Inconsistency. IEEE Access, 12, 5605-5616. https://doi.org/10.1109/ACCESS.2024.3349472

<a name="c90">[90]</a> Yang, W. (2020). Ingenious solution for the rank reversal problem of TOPSIS method. Mathematical Problems in Engineering, 2020, 9676518. https://doi.org/10.1155/2020/9676518

<a name="c91">[91]</a> García-Cascales, M. S., & Lamata, M. T. (2012). On rank reversal and TOPSIS method. Mathematical and Computer Modelling, 56(5-6), 123-132. https://doi.org/10.1016/j.mcm.2011.12.022

<a name="c92">[92]</a> Yang, B., Zhao, J., & Zhao, H. (2022). A robust method for avoiding rank reversal in the TOPSIS. Computers & Industrial Engineering, 174, 108776. https://doi.org/10.1016/j.cie.2022.108776

<a name="c93">[93]</a> Costa, L. F., Costa, H. G., Lima, D., & Rodrigues, B. (2026). TOPSIS-RAD: Ranking According to Desires. arXiv preprint arXiv:2606.07253. https://doi.org/10.48550/arXiv.2606.07253

<a name="c94">[94]</a> Stanujkić, D., Karabašević, D., Popović, G., & Sava, C. (2021). Simplified pivot pairwise relative criteria importance assessment (PIPRECIA-S) method. Romanian Journal of Economic Forecasting, 24(4), 141-154.

<a name="c95">[95]</a> Rezaei, J. (2016). Best-worst multi-criteria decision-making method: Some properties and a linear model. Omega, 64, 126-130. https://doi.org/10.1016/j.omega.2015.12.001

<a name="c96">[96]</a> Mousseau, V., Słowiński, R., & Zielniewicz, P. (2000). A user-oriented implementation of the ELECTRE-TRI method integrating preference elicitation support. Computers & Operations Research, 27(7-8), 757-777. https://doi.org/10.1016/S0305-0548(99)00117-3

<a name="c97">[97]</a> Figueira, J. R., Mousseau, V., & Roy, B. (2016). ELECTRE methods. In S. Greco, M. Ehrgott, & J. R. Figueira (Eds.), Multiple Criteria Decision Analysis: State of the Art Surveys (pp. 155-185). Springer. https://doi.org/10.1007/978-1-4939-3094-4_5

<a name="c98">[98]</a> de Lima Silva, D. F., & de Almeida Filho, A. T. (2020). Sorting with TOPSIS through boundary and characteristic profiles. Computers & Industrial Engineering, 141, 106328. https://doi.org/10.1016/j.cie.2020.106328

<a name="c99">[99]</a> Brauers, W. K. M., & Zavadskas, E. K. (2010). Project management by MULTIMOORA as an instrument for transition economies. Technological and Economic Development of Economy, 16(1), 5-24. https://doi.org/10.3846/tede.2010.01

<a name="c100">[100]</a> Brauers, W. K. M., & Zavadskas, E. K. (2011). MULTIMOORA optimization used to decide on a bank loan to buy property. Technological and Economic Development of Economy, 17(1), 174-188. https://doi.org/10.3846/13928619.2011.560632

<a name="c101">[101]</a> Yang, W., & Wu, Y. (2020). A new improvement method to avoid rank reversal in VIKOR. IEEE Access, 8, 21261-21271. https://doi.org/10.1109/ACCESS.2020.2969681

<a name="c102">[102]</a> Puška, A., Stević, Ž., & Pamučar, D. (2022). Evaluation and selection of healthcare waste incinerators using extended sustainability criteria and multi-criteria analysis methods. Environment, Development and Sustainability, 24(9), 11195-11225. https://doi.org/10.1007/s10668-021-01902-2

<a name="c103">[103]</a> Kuo, Y., Yang, T., & Huang, G. W. (2008). The use of grey relational analysis in solving multiple attribute decision-making problems. Computers & Industrial Engineering, 55(1), 80-93. https://doi.org/10.1016/j.cie.2007.12.002

<a name="c104">[104]</a> Maniya, K., & Bhatt, M. G. (2010). A selection of material using a novel type decision-making method: Preference selection index method. Materials & Design, 31(4), 1785-1789. https://doi.org/10.1016/j.matdes.2009.11.020

<a name="c105">[105]</a> Barron, F. H., & Barrett, B. E. (1996). Decision quality using ranked attribute weights. Management Science, 42(11), 1515-1523. https://doi.org/10.1287/mnsc.42.11.1515

<a name="c106">[106]</a> Stillwell, W. G., Seaver, D. A., & Edwards, W. (1981). A comparison of weight approximation techniques in multiattribute utility decision making. Organizational Behavior and Human Performance, 28(1), 62-77. https://doi.org/10.1016/0030-5073(81)90015-5

<a name="c107">[107]</a> Hellwig, Z. (1968). Zastosowanie metody taksonomicznej do typologicznego podziału krajów ze względu na poziom ich rozwoju oraz zasoby i strukturę wykwalifikowanych kadr. Przegląd Statystyczny, 4, 307-326.

<a name="c108">[108]</a> Roszkowska, E. (2024). Modifying Hellwig's method for multi-criteria decision-making with Mahalanobis distance for addressing asymmetrical relationships. Symmetry, 16(1), 77. https://doi.org/10.3390/sym16010077

<a name="c109">[109]</a> Roszkowska, E., & Filipowicz-Chomko, M. (2024). A multi-criteria method integrating distances to ideal and anti-ideal points. Symmetry, 16(8), 1025. https://doi.org/10.3390/sym16081025

<a name="c110">[110]</a> Roszkowska, E., Filipowicz-Chomko, M., & Wachowicz, T. (2020). Using individual and common reference points to measure the performance of alternatives in multiple criteria evaluation. Operations Research and Decisions, 30(3), 77-96. https://doi.org/10.37190/ord200305

<a name="c111">[111]</a> Wierzbicki, A. P., Granat, J., & Makowski, M. (2007). Discrete decision problems with large number of criteria. IIASA Interim Report IR-07-025. International Institute for Applied Systems Analysis, Laxenburg. https://pure.iiasa.ac.at/8432/

<a name="c112">[112]</a> Wierzbicki, A. P. (2007). Reference point approaches and objective ranking. In Practical Approaches to Multi-Objective Optimization, Dagstuhl Seminar Proceedings 06501 (pp. 1-20). https://doi.org/10.4230/DagSemProc.06501.2

<a name="c113">[113]</a> Yang, W., Pang, X., Kong, D., & Shang, H. (2026). BP-TOPSIS: A Boxplot-Based Approach to Reducing Rank Reversal in the TOPSIS Method. International Journal of Information Technology & Decision Making, 25(10), 3509-3538. https://doi.org/10.1142/S0219622026500483

<a name="c114">[114]</a> Mufazzal, S., & Muzakkir, S. M. (2018). A new multi-criterion decision making (MCDM) method based on proximity indexed value for minimizing rank reversals. Computers & Industrial Engineering, 119, 427-438. https://doi.org/10.1016/j.cie.2018.03.045
