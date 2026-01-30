# Release history

## Version 1.4.0

* New MCDM methods, with test and documentation:
  - LMAW (Logarithmic Methodology of Additive Weights).
  - RAFSI (Ranking of Alternatives through Functional mapping of criterion sub-intervals into a Single Interval).
  - Balanced SPOTIS (SPOTIS method's extension).
  - LOPCOW (LOgarithmic Percentage Change-driven Objective Weighting), weighting method.
* Add gray-code CO order support to COMET, with tests
* Add weighted ESP Expert for COMET evaluations.
* Add `param_sensitivity` helper for method parameter sweeps.
* Add new distance module for different metrics (Kemeny, Frobenius, draWS) with docs and tests.
* Fix zero-division issues in normalization functions.
* Small fixes in correlations, helpers and validators; various documentation updates.
* Update copyright year across the codebase.


## Version 1.3.1

* Add CSV and JSON export options to Table, MCDA_problem and MCDA_results classes.
* Add centering command to latex output of MCDA_problem, add "tab:" prefix to its label.
* Partially rewrite MCDA_results to be able to add new output format more easily.
* Change the validation of matrix and weights. Now if matrix contains dominant od dominated alternatives,
  or weights does not sum up to 1, UserWarning will be shown, instead of exception. To obey validation use
  validation=False argument in the method's call.

## Version 1.3.0

This is fairly big update, which include various improvements in code and modules structure, documentation,
implementations and so on. Two main points of the update are: `verbose` argument for MCDM methods,
which allows for easily inspect computation process for different methods, and addition of AHP and RANCOM pairwise
comparison-based subjective weighting methods.

Most of the code written for previous versions of `pymcdm` should work, however small fixes can be required.

### List of all changes:

#### New methods
- Added pairwise weighting method: RANCOM, and AHP, including examples and tests for them.
- Add RAM and LoPM methods, with documentation and tests for it.

#### New modules and changes in the structure
- Now such methods as PROMETHEE I/II and PROBID/SPROBID are implemented in separate classes.
- PROMETHEE I method is now implemented as `PROMETHEE_I` class in `pymcdm.methods.partial` module.
- Classes `RANCOM` and `AHP` are available under `pymcdm.weights.subjective`.
- New modules:
  - `pymcdm.io` - which includes classes that supports verbose output of the methods.
  - `pymcdm.validators` - which includes functions which are used for the validation of the input.
  - `pymcdm.methods.partial` - currently contains only `PROMETHEE_I` class, in future will include other partial
    ranking methods.
  - `pymcdm.weights.subjective` - module for subjective weighting method. Currently, contains AHP and RANCOM
    implementations.

#### Changes related to the usage of MCDM method
- Now, all additional arguments besides decision matrix, weights and types are provided in the constructor, not in 
  the call.
- Two new arguments to the call:
  - `verbose=True` - to return all intermediate results. See example in README for this. Results then can be represented
    as formatted string or as LaTeX code.
  - `validation=False` - to disable input data validation. Use it if you absolutely want to run the method on this data,
    but validation does not allow you to do it.

#### Other improvements
- Rewritten validation system across most methods for improved reliability. To skip validation add `validation=False`
  to the method call.
- Update for the documentation, including various fixes and improvements, as well as new examples. This includes changes
  in the subpage structure, API and User Guide improvements.
- Improved normalization handling in `normalize_matrix`. Now normalization type can be provided as `str`.
- Add new arguments to `ranking_bar()` function.
- Removed redundant files.

## Version 1.2.1

* Add examples for the `comet_tools` to the documentation
* Add `comet_3d_esp_plot` visualization function
* Add `RAM` method and documentation for it
* Add `get_local_weights` function
* Improve `normalize_matrix` helper function
* Improve behaviour of `StructuralCOMET` class
* Update references in README.md
* Rename `comet_esp_plot` to `comet_2d_esp_plot`
* Fix bug with file writing in `manual_expert` and `triad_supported_expert`
* Fix calculation on final stage of the `COPRAS` method and improve tests accordingly
* Fix bug with `zavadsks_turkish_normalization` function
* Clean up documentation folder
* Various fixes in the documentation and docstrings

## Version 1.2.0

### General changes

* Add CONTRIBUTING.md
* Add CHANGELOG.md
* Functions `correlation_matrix` and `normalize_matrix` are moved to helpers
* Add ESP to SPOTIS implementation

### New methods

* RIM
* ERVD
* PROBID
* WSM
* WPM
* WASPAS

### Visualization changes

* Fix visuals import bug
* Add `leave_one_out_rr` helper function
* Add `rankings_flow_correlation` visualization
* Add `correlation_plot` visualization
* Add `comet_tfns` visualization
* All visualization function now returns ax or ax, cax if used
* Add colors argument to `polar_plot`
* Improve `promethee_I_graph` visualization
* Refactor and improve `ranking_flows` function

### New similarity coefficients and other correlation related changes

* WSC, WSC2 - Weights similarity coefficients
* draWS - drastic distance between rankings
* Some of the correlation coefficients got aliases, such as rs, r, rw, ws

### COMET Tools module

* Refactor evaluation of the characteristic objects in the COMET, now rate_function and expert_function are the same function
* Add bunch of Expert functions for the COMET: `MethodExpert`, `ManualExpert`, `FunctionExpert`, `CompromiseExpert`, `TriadSupportExpert`, `ESPExpert`
* Add triads consistency coefficient
* Add `StructuralCOMET` class which allows to build structural MCDA models in easy way
* Add example of the structural COMET usage
* Add examples for the most of the new Expert functions
