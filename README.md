# PyMCDM

Python 3 library for solving multi-criteria decision-making (MCDM) problems.

Documentation is avaliable on [readthedocs](https://pymcdm.readthedocs.io/en/master/).

___

# Installation

You can download and install `pymcdm` library using pip:

```Bash 
pip install pymcdm
```

___

# Available methods

The library contains:

* MCDA methods:

|  Acronym            	|  Method Name                                                                   	|                Reference               	|
| :-------------------- | -------------------------------------------------------------------------------   | :--------------------------------------:	|
|  TOPSIS             	|  Technique for the Order of Prioritisation by Similarity to Ideal Solution     	|               [[1]](#c1)               	|
|  VIKOR              	|  VIseKriterijumska Optimizacija I Kompromisno Resenje                          	|               [[2]](#c2)               	|
|  COPRAS             	|  COmplex PRoportional ASsessment                                               	|               [[3]](#c3)               	|
|  PROMETHEE I & II   	|  Preference Ranking Organization METHod for Enrichment of Evaluations I & II   	|               [[4]](#c4)               	|
|  COMET              	|  Characteristic Objects Method                                                 	|               [[5]](#c5)               	|
|  SPOTIS             	|  Stable Preference Ordering Towards Ideal Solution                             	|               [[6]](#c6)               	|
|  ARAS               	|  Additive Ratio ASsessment                                                     	|          [[7]](#c7),[[8]](#c8)         	|
|  COCOSO             	|  COmbined COmpromise SOlution                                                  	|               [[9]](#c9)               	|
|  CODAS              	|  COmbinative Distance-based ASsessment                                         	|              [[10]](#c10)              	|
|  EDAS               	|  Evaluation based on Distance from Average Solution                            	|        [[11]](#c11),[[12]](#c12)       	|
|  MABAC              	|  Multi-Attributive Border Approximation area Comparison                        	|              [[13]](#c13)              	|
|  MAIRCA             	|  MultiAttributive Ideal-Real Comparative Analysis                              	| [[14]](#c14),[[15]](#c15),[[16]](#c16) 	|
|  MARCOS             	|  Measurement Alternatives and Ranking according to COmpromise Solution         	|        [[17]](#c17),[[18]](#c18)       	|
|  OCRA               	|  Operational Competitiveness Ratings                                           	|        [[19]](#c19),[[20]](#c20)       	|
|  MOORA              	|  Multi-Objective Optimization Method by Ratio Analysis                         	|        [[21]](#c21),[[22]](#c22)       	|
|  RIM               	|  Reference Ideal Method                                                           |               [[48]](#c48)               	|
|  ERVD               	|  Election Based on relative Value Distances                                       |               [[49]](#c49)               	|
|  PROBID               |  Preference Ranking On the Basis of Ideal-average Distance                        |               [[50]](#c50)               	|

* Weighting methods:

| Acronym   	| Method Name                                             	|                 Reference                	|
|-----------	|---------------------------------------------------------	|:----------------------------------------:	|
| -         	| Equal/Mean weights                                      	|               [[23]](#c23)               	|
| -         	| Entropy weights                                         	| [[23]](#c23),[[24]](#c24),[[25]](#c25) 	|
| STD       	| Standard Deviation weights                              	|        [[23]](#c23),[[26]](#c26)        	|
| MEREC     	| MEthod based on the Removal Effects of Criteria         	|               [[27]](#c27)               	|
| CRITIC    	| CRiteria Importance Through Intercriteria Correlation   	|        [[28]](#c28),[[29]](#c29)       	|
| CILOS     	| Criterion Impact LOS                                    	|               [[30]](#c30)               	|
| IDOCRIW   	| Integrated Determination of Objective CRIteria Weight   	|               [[30]](#c30)               	|
| -         	| Angular/Angle weights                                   	|               [[31]](#c31)               	|
| -         	| Gini Coeficient weights                                 	|               [[32]](#c32)               	|
| -         	| Statistical variance weights                            	|               [[33]](#c33)               	|

* Normalization methods:

| Method Name                          	|          Reference         	|
|--------------------------------------	|:--------------------------:	|
| Weitendorf’s Linear Normalization    	|        [[34]](#c34)        	|
| Maximum - Linear Normalization       	|        [[35]](#c35)        	|
| Sum-Based Linear Normalization       	|        [[36]](#c36)        	|
| Vector Normalization                 	|  [[36]](#c36),[[37]](#c37) 	|
| Logarithmic Normalization            	| [[36]](#c36),[[37]](#c37) 	|
| Linear Normalization (Max-Min)       	|  [[34]](#c34),[[38]](#c38) 	|
| Non-linear Normalization (Max-Min)   	|        [[39]](#c39)        	|
| Enhanced Accuracy Normalization      	|        [[40]](#c40)        	|
| Lai and Hwang Normalization           |        [[38]](#c38)           |
| Zavadskas and Turskis Normalization   |        [[38]](#c38)           |

* Correlation coefficients:

| Coefficient name                                   	|         Reference         	|
|----------------------------------------------------	|:-------------------------:	|
| Spearman's rank correlation coefficient            	| [[41]](#c41),[[42]](#c42) 	|
| Pearson correlation coefficient                    	|        [[43]](#c43)       	|
| Weighted Spearman’s rank correlation coefficient   	|        [[44]](#c44)       	|
| Rank Similarity Coefficient                        	|        [[45]](#c45)       	|
| Kendall rank correlation coefficient               	|        [[46]](#c46)       	|
| Goodman and Kruskal's gamma                        	|        [[47]](#c47)       	|


* Helpers
    * rankdata
    * rrankdata


___
# Usage example

Here's a small example of how use this library to solve MCDM problem.
For more examples with explanation see [examples](https://gitlab.com/shekhand/mcda/-/blob/master/examples/examples.ipynb).

```python
import numpy as np
from pymcdm.methods import TOPSIS
from pymcdm.helpers import rrankdata

# Define decision matrix (2 criteria, 4 alternative)
alts = np.array([
    [4, 4],
    [1, 5],
    [3, 2],
    [4, 2]
], dtype='float')

# Define weights and types
weights = np.array([0.5, 0.5])
types = np.array([1, -1])

# Create object of the method
topsis = TOPSIS()

# Determine preferences and ranking for alternatives
pref = topsis(alts, weights, types)
ranking = rrankdata(pref)

for r, p in zip(ranking, pref):
    print(r, p)
```

And the output of this example (numbers are rounded):

```bash
3 0.6126
4 0.0
2 0.7829
1 1.0
```
---
# References

<a name="c1">**[1]**</a> Hwang, C. L., & Yoon, K. (1981). Methods for multiple attribute decision making. In Multiple attribute decision making (pp. 58-191). Springer, Berlin, Heidelberg.

<a name="c2">**[2]**</a> Duckstein, L., & Opricovic, S. (1980). Multiobjective optimization in river basin development. Water resources research, 16(1), 14-20.

<a name="c3">**[3]**</a> Zavadskas, E. K., Kaklauskas, A., Peldschus, F., & Turskis, Z. (2007). Multi-attribute assessment of road design solutions by using the COPRAS method. The Baltic Journal of Road and Bridge Engineering, 2(4), 195-203.

<a name="c4">**[4]**</a> Brans, J. P., Vincke, P., & Mareschal, B. (1986). How to select and how to rank projects: The PROMETHEE method. European journal of operational research, 24(2), 228-238.

<a name="c5">**[5]**</a> Sałabun, W., Karczmarczyk, A., Wątróbski, J., & Jankowski, J. (2018, November). Handling data uncertainty in decision making with COMET. In 2018 IEEE Symposium Series on Computational Intelligence (SSCI) (pp. 1478-1484). IEEE.

<a name="c6">**[6]**</a> Dezert, J., Tchamova, A., Han, D., & Tacnet, J. M. (2020, July). The spotis rank reversal free method for multi-criteria decision-making support. In 2020 IEEE 23rd International Conference on Information Fusion (FUSION) (pp. 1-8). IEEE.

<a name="c7">**[7]**</a> Zavadskas, E. K., & Turskis, Z. (2010). A new additive ratio assessment (ARAS) method in multicriteria decision‐making. Technological and economic development of economy, 16(2), 159-172.

<a name="c8">**[8]**</a> Stanujkic, D., Djordjevic, B., & Karabasevic, D. (2015). Selection of candidates in the process of recruitment and selection of personnel based on the SWARA and ARAS methods. Quaestus, (7), 53.

<a name="c9">**[9]**</a> Yazdani, M., Zarate, P., Zavadskas, E. K., & Turskis, Z. (2019). A Combined Compromise Solution (CoCoSo) method for multi-criteria decision-making problems. Management Decision.

<a name="c10">**[10]**</a> Badi, I., Shetwan, A. G., & Abdulshahed, A. M. (2017, September). Supplier selection using COmbinative Distance-based ASsessment (CODAS) method for multi-criteria decision-making. In Proceedings of The 1st International Conference on Management, Engineering and Environment (ICMNEE) (pp. 395-407).

<a name="c11">**[11]**</a> Keshavarz Ghorabaee, M., Zavadskas, E. K., Olfat, L., & Turskis, Z. (2015). Multi-criteria inventory classification using a new method of evaluation based on distance from average solution (EDAS). Informatica, 26(3), 435-451.

<a name="c12">**[12]**</a> Yazdani, M., Torkayesh, A. E., Santibanez-Gonzalez, E. D., & Otaghsara, S. K. (2020). Evaluation of renewable energy resources using integrated Shannon Entropy—EDAS model. Sustainable Operations and Computers, 1, 35-42.

<a name="c13">**[13]**</a> Pamučar, D., & Ćirović, G. (2015). The selection of transport and handling resources in logistics centers using Multi-Attributive Border Approximation area Comparison (MABAC). Expert systems with applications, 42(6), 3016-3028.

<a name="c14">**[14]**</a> Gigović, L., Pamučar, D., Bajić, Z., & Milićević, M. (2016). The combination of expert judgment and GIS-MAIRCA analysis for the selection of sites for ammunition depots. Sustainability, 8(4), 372.

<a name="c15">**[15]**</a> Pamucar, D. S., Pejcic Tarle, S., & Parezanovic, T. (2018). New hybrid multi-criteria decision-making DEMATELMAIRCA model: sustainable selection of a location for the development of multimodal logistics centre. Economic research-Ekonomska istraživanja, 31(1), 1641-1665.

<a name="c16">**[16]**</a> Aksoy, E. (2021). An Analysis on Turkey's Merger and Acquisition Activities: MAIRCA Method. Gümüşhane Üniversitesi Sosyal Bilimler Enstitüsü Elektronik Dergisi, 12(1), 1-11.

<a name="c17">**[17]**</a> Stević, Ž., Pamučar, D., Puška, A., & Chatterjee, P. (2020). Sustainable supplier selection in healthcare industries using a new MCDM method: Measurement of alternatives and ranking according to COmpromise solution (MARCOS). Computers & Industrial Engineering, 140, 106231.

<a name="c18">**[18]**</a> Ulutaş, A., Karabasevic, D., Popovic, G., Stanujkic, D., Nguyen, P. T., & Karaköy, Ç. (2020). Development of a novel integrated CCSD-ITARA-MARCOS decision-making approach for stackers selection in a logistics system. Mathematics, 8(10), 1672.

<a name="c19">**[19]**</a> Parkan, C. (1994). Operational competitiveness ratings of production units. Managerial and Decision Economics, 15(3), 201-221.

<a name="c20">**[20]**</a> Işık, A. T., & Adalı, E. A. (2016). A new integrated decision making approach based on SWARA and OCRA methods for the hotel selection problem. International Journal of Advanced Operations Management, 8(2), 140-151.

<a name="c21">**[21]**</a> Brauers, W. K. (2003). Optimization methods for a stakeholder society: a revolution in economic thinking by multi-objective optimization (Vol. 73). Springer Science & Business Media.

<a name="c22">**[22]**</a> Hussain, S. A. I., & Mandal, U. K. (2016). Entropy based MCDM approach for Selection of material. In National Level Conference on Engineering Problems and Application of Mathematics (pp. 1-6).

<a name="c23">**[23]**</a> Sałabun, W., Wątróbski, J., & Shekhovtsov, A. (2020). Are mcda methods benchmarkable? a comparative study of topsis, vikor, copras, and promethee ii methods. Symmetry, 12(9), 1549.

<a name="c24">**[24]**</a> Lotfi, F. H., & Fallahnejad, R. (2010). Imprecise Shannon’s entropy and multi attribute decision making. Entropy, 12(1), 53-62.

<a name="c25">**[25]**</a> Li, X., Wang, K., Liu, L., Xin, J., Yang, H., & Gao, C. (2011). Application of the entropy weight and TOPSIS method in safety evaluation of coal mines. Procedia engineering, 26, 2085-2091.

<a name="c26">**[26]**</a> Wang, Y. M., & Luo, Y. (2010). Integration of correlations with standard deviations for determining attribute weights in multiple attribute decision making. Mathematical and Computer Modelling, 51(1-2), 1-12.

<a name="c27">**[27]**</a> Keshavarz-Ghorabaee, M., Amiri, M., Zavadskas, E. K., Turskis, Z., & Antucheviciene, J. (2021). Determination of Objective Weights Using a New Method Based on the Removal Effects of Criteria (MEREC). Symmetry, 13(4), 525.

<a name="c28">**[28]**</a> Diakoulaki, D., Mavrotas, G., & Papayannakis, L. (1995). Determining objective weights in multiple criteria problems: The critic method. Computers & Operations Research, 22(7), 763-770.

<a name="c29">**[29]**</a> Tuş, A., & Adalı, E. A. (2019). The new combination with CRITIC and WASPAS methods for the time and attendance software selection problem. Opsearch, 56(2), 528-538.

<a name="c30">**[30]**</a> Zavadskas, E. K., & Podvezko, V. (2016). Integrated determination of objective criteria weights in MCDM. International Journal of Information Technology & Decision Making, 15(02), 267-283.

<a name="c31">**[31]**</a> Shuai, D., Zongzhun, Z., Yongji, W., & Lei, L. (2012, May). A new angular method to determine the objective weights. In 2012 24th Chinese Control and Decision Conference (CCDC) (pp. 3889-3892). IEEE.

<a name="c32">**[32]**</a> Li, G., & Chi, G. (2009, December). A new determining objective weights method-gini coefficient weight. In 2009 First International Conference on Information Science and Engineering (pp. 3726-3729). IEEE.

<a name="c33">**[33]**</a> Rao, R. V., & Patel, B. K. (2010). A subjective and objective integrated multiple attribute decision making method for material selection. Materials & Design, 31(10), 4738-4747.

<a name="c34">**[34]**</a> Brauers, W. K., & Zavadskas, E. K. (2006). The MOORA method and its application to privatization in a transition economy. Control and cybernetics, 35, 445-469.

<a name="c35">**[35]**</a> Jahan, A., & Edwards, K. L. (2015). A state-of-the-art survey on the influence of normalization techniques in ranking: Improving the materials selection process in engineering design. Materials & Design (1980-2015), 65, 335-342.

<a name="c36">**[36]**</a> Gardziejczyk, W., & Zabicki, P. (2017). Normalization and variant assessment methods in selection of road alignment variants–case study. Journal of civil engineering and management, 23(4), 510-523.

<a name="c37">**[37]**</a> Zavadskas, E. K., & Turskis, Z. (2008). A new logarithmic normalization method in games theory. Informatica, 19(2), 303-314.

<a name="c38">**[38]**</a> Jahan, A., & Edwards, K. L. (2015). A state-of-the-art survey on the influence of normalization techniques in ranking: Improving the materials selection process in engineering design. Materials & Design (1980-2015), 65, 335-342.

<a name="c39">**[39]**</a> Peldschus, F., Vaigauskas, E., & Zavadskas, E. K. (1983). Technologische entscheidungen bei der berücksichtigung mehrerer Ziehle. Bauplanung Bautechnik, 37(4), 173-175.

<a name="c40">**[40]**</a> Zeng, Q. L., Li, D. D., & Yang, Y. B. (2013). VIKOR method with enhanced accuracy for multiple criteria decision making in healthcare management. Journal of medical systems, 37(2), 1-9.

<a name="c41">**[41]**</a> Binet, A., & Henri, V. (1898). La fatigue intellectuelle (Vol. 1). Schleicher frères.

<a name="c42">**[42]**</a> Spearman, C. (1910). Correlation calculated from faulty data. British Journal of Psychology, 1904‐1920, 3(3), 271-295.

<a name="c43">**[43]**</a> Pearson, K. (1895). VII. Note on regression and inheritance in the case of two parents. proceedings of the royal society of London, 58(347-352), 240-242.

<a name="c44">**[44]**</a> Dancelli, L., Manisera, M., & Vezzoli, M. (2013). On two classes of Weighted Rank Correlation measures deriving from the Spearman’s ρ. In Statistical Models for Data Analysis (pp. 107-114). Springer, Heidelberg.

<a name="c45">**[45]**</a> Sałabun, W., & Urbaniak, K. (2020, June). A new coefficient of rankings similarity in decision-making problems. In International Conference on Computational Science (pp. 632-645). Springer, Cham.

<a name="c46">**[46]**</a> Kendall, M. G. (1938). A new measure of rank correlation. Biometrika, 30(1/2), 81-93.

<a name="c47">**[47]**</a> Goodman, L. A., & Kruskal, W. H. (1979). Measures of association for cross classifications. Measures of association for cross classifications, 2-34.

<a name="c48">**[48]**</a> Cables, E., Lamata, M. T., & Verdegay, J. L. (2016). RIM-reference ideal method in multicriteria decision making. Information Sciences, 337, 1-10.

<a name="c49">**[49]**</a> Shyur, H. J., Yin, L., Shih, H. S., & Cheng, C. B. (2015). A multiple criteria decision making method based on relative value distances. Foundations of Computing and Decision Sciences, 40(4), 299-315.

<a name="c50">**[50]**</a> Wang, Z., Rangaiah, G. P., & Wang, X. (2021). Preference ranking on the basis of ideal-average distance method for multi-criteria decision-making. Industrial & Engineering Chemistry Research, 60(30), 11216-11230.
