# Version 1.2.1

* Add `comet_3d_esp_plot` visualization function
* Rename `comet_esp_plot` to `comet_2d_esp_plot`
* Improve `normalize_matrix` helper function
* Add `RAM` method and documentation for it
* Add `get_local_weights` function
* Fix bug with file writing in `manual_expert` and `triad_supported_expert`
* Improve behaviour of `StructuralCOMET` class
* Fix calculation on final stage of the `COPRAS` method and improve tests accordingly
* Fix bug with `zavadsks_turkish_normalization` function

# Version 1.2.0

## General changes

* Add CONTRIBUTING.md
* Add CHANGELOG.md
* Functions `correlation_matrix` and `normalize_matrix` are moved to helpers
* Add ESP to SPOTIS implementation

## New methods

* RIM
* ERVD
* PROBID
* WSM
* WPM
* WASPAS

## Visualization changes

* Fix visuals import bug
* Add `leave_one_out_rr` helper function
* Add `rankings_flow_correlation` visualization
* Add `correlation_plot` visualization
* Add `comet_tfns` visualization
* All visualization function now returns ax or ax, cax if used
* Add colors argument to `polar_plot`
* Improve `promethee_I_graph` visualization
* Refactor and improve `ranking_flows` function

## New similarity coefficients and other correlation related changes

* WSC, WSC2 - Weights similarity coefficients
* draWS - drastic distance between rankings
* Some of the correlation coefficients got aliases, such as rs, r, rw, ws

## COMET Tools module

* Refactor evaluation of the characteriscic objects in the COMET, now rate_function and expert_function are the same function
* Add bunch of Expert functions for the COMET: `MethodExpert`, `ManualExpert`, `FunctionExpert`, `CompromiseExpert`, `TriadSupportExpert`, `ESPExpert`
* Add triads consistency coefficient
* Add `StructuralCOMET` class which allows to build structural MCDA models in easy way
* Add example of the structural COMET usage
* Add examples for the most of the new Expert functions
