try:
    from _site_specific import *
except:
    pass

import _installation

from data import InputFile, InputFileOrig, InputFile17, Output, ConcentrationOutput, RatesOutput, AdjointOutput, JacobianOutput, HessianOutput
from fluxes import FluxParser

work_path = _installation.validate()
if work_path is None:
    import warnings
    warnings.warn("BOXMOX unusable - experiment execution disabled.")
else:
    from experiment import Experiment, ExperimentFromExample, ExperimentFromExistingRun, Namelist, examples, compiledMechs

try:
    import matplotlib
    from plotter import ExperimentPlotter
except:
    import warnings
    warnings.warn('matplotlib not found - plotting disabled.')

import _console