# Version X

## General changes

* Add CONTRIBUTING.md
* Add CHANGELOG.md
* Functions `correlation_matrix` and `normalize_matrix` are moved to helpers
* Add ESP to SPOTIS implementation

## New methods

* RIM
* ERVD
* PROBID

## New similarity coefficients and other correlation related changes

* WSC, WSC2 - Weights similarity coefficients
* draWS - drastic distance between rankings
* Some of the correlation coefficients got aliases, such as rs, r, rw, ws

## COMET Tools module

* Refactor evaluation of the characteriscic objects in the COMET, now rate_function and expert_function are the same function
* Add bunch of Expert functions for the COMET: `MethodExpert`, `ManualExpert`, `FunctionExpert`, `CompromiseExpert`, `TriadSupportExpert`
* Add triads consistency coefficient
* Add `StructuralCOMET` class which allows to build structural MCDA models in easy way
* Add example of the structural COMET usage
* Add examples for the most of the new Expert functions

