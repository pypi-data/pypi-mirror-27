import os
import sys
if os.name == 'posix' and sys.version_info[0] < 3:
    import subprocess32 as s
else:
    import subprocess as s
import threading
import shutil
import fnmatch
import numpy as np
import datetime
import f90nml

from . import _installation
from . import InputFile, Output, ConcentrationOutput, RatesOutput, AdjointOutput, JacobianOutput, HessianOutput
try:
    import matplotlib
    from .plotter import ExperimentPlotter
except:
    pass
from . import FluxParser

work_path = _installation.validate()

examplesPath=os.path.join(os.environ['KPP_HOME'], "boxmox", "boxmox_examples")

class ExampleData:
    def __getitem__(self, name):
        if name in self.files.keys():
            return InputFile(self.files[name])
        else:
            raise Exception("Input file {:s} does not exist.".format(name))
    def __init__(self, path):
        self.path  = path
        self.files = { x.replace(".csv", ""): os.path.join(self.path, x) for x in os.listdir(self.path) if '.csv' in x }
        self.mech  = 'unknown'
        try:
            with open( os.path.join( self.path, 'mech_used' ) ) as f:
                self.mech = f.readline()
        except:
            pass

compiledMechsPath=os.path.join(os.environ['KPP_HOME'], "boxmox", "compiled_mechs")

compiledMechs = []
try:
    compiledMechs = [ x for x in os.listdir(compiledMechsPath) if (os.path.isdir( os.path.join(compiledMechsPath, x) )) and ("_adjoint" not in x) ]
except:
    print("No compile_mechs directory found")

_examples = { x: ExampleData(os.path.join(examplesPath, x)) for x in os.listdir(examplesPath) if os.path.isdir( os.path.join(examplesPath, x) ) }
examples  = { x: _examples[x] for x in _examples if _examples[x].mech in compiledMechs }

class Namelist:
    '''
    A BOXMOX (Fortran 90) namelist. Getting and setting of values
    works like a dictionary::

       print(nml['tstart'])
       nml['tstart'] = 12.0

    '''
    def __getitem__(self, item):
        if item.lower() in self._namelist['boxmox'].keys():
            return self._namelist['boxmox'][item.lower()]
        else:
            raise Exception('{:s} does not exist in Namelist.'.format(item))
    def __setitem__(self, item, value):
        if item.lower() in self._namelist['boxmox'].keys():
            try:
                self._namelist['boxmox'][item] = value
            except:
                raise Exception('Failed to set {:s} to {:s}'.format(item, str(value)))
        else:
            raise Exception('{:s} does not exist in Namelist'.format(item))
    def __str__(self):
        return ', '.join( [ ('{:s}: {:s}'.format(item, str(self._namelist['boxmox'][item]))) for item in self._namelist['boxmox'].keys() ] )
    def keys(self):
        return self._namelist['boxmox'].keys()
    def write(self, path):
        '''
        Write namelist to file.
        '''
        self._namelist.write(path, 'w')
    def read(self, path):
        '''
        Read namelist from file.
        '''
        self._namelist = f90nml.read(path)
    def __init__(self, path = None):
        self._namelist = None

        firstExample = examples[examples.keys()[0]]
        self.read(os.path.join(firstExample.path, "BOXMOX.nml"))
        if not path is None:
            if os.path.exists(path):
                self.read(path)

class Experiment:
    '''
    A new BOXMOX experiment using a certain mechanism.
    '''
    removeOnDel = True

    def __init__(self, mechanism):
        import uuid

        #: Unique ID
        self.name = str(uuid.uuid4())
        #: Chemical mechanism used
        self.mechanism = mechanism

        #: Absolute file system path of the experiment
        self.path = os.path.join(work_path, self.name)

        #: Input files
        self.input       = {}
        #: Output files
        self.output      = {}

        self.plotter     = None
        self.fluxes      = None

        #: Log file of the last run
        self.log         = None

        self.pid         = None
        self.thread      = None

        self.__new()

        #: Namelist
        self.namelist = Namelist(os.path.join(self.path, 'BOXMOX.nml'))

        self.version  = self._determineVersion(self.path)

    def _determineVersion(self, path):
        version     = 1.0
        versionFile = os.path.join(path, 'VERSION')
        if os.path.exists(versionFile):
            try:
                with open(versionFile, 'rb') as f:
                    line = f.readline().rstrip()
                    line = ".".join(line.split(".")[0:min(2, len(line.split(".")))])
                    # for development only:
                    if line == "__BOXMOX_VERSION__":
                        line = 1.7
                    version = float(line)
            except:
                version = 1.0
                pass
        return version

    def _populateInput(self):
        inputFileNames = [f for f in os.listdir(self.path) if f.endswith('.csv')]
        self.input = { x.replace('.csv', '') : InputFile(os.path.join(self.path, x)) for x in inputFileNames }

    def __new(self):
        try:
            s.call(["new_BOXMOX_experiment", self.mechanism, self.path])

            self._populateInput()
        except s.CalledProcessError as e:
            raise Exception("Creating new experiment failed: " + str(e.output))

    def addInputFromFile(self, name, fname, overwrite=False):
        '''
        Add input from file
        '''
        if name in self.input.keys() and not overwrite:
            raise Exception("Input file {:s} already exists.".format(name))
        self.input[name] = InputFile(fname)

    def addInput(self, name, inp, overwrite=False):
        '''
        Add input from InputFile object
        '''
        if name in self.input.keys() and not overwrite:
            raise Exception("Input file {:s} already exists.".format(name))
        self.input[name] = inp

    def _get_mechanism(self):
        mech = None

        # see if we have an executable
        exes = [ x for x in os.listdir(self.path) if '.exe' in x ]
        if len(exes) == 1:
            mech = exes[0].replace('.exe', '')

        # if not, use an output file
        if mech is None:
            outs = [ x for x in os.listdir(self.path) if x.endswith('.conc') ]
            if len(outs) == 1:
                mech = outs[0].replace('.conc', '')

        if mech is None:
            import warnings
            warnings.warn('Could not determine mechanism in BOXMOX experiment path: ' + self.path)

        return mech

    @property
    def running(self):
        '''
        Check if simulation is running (if started with asynchronous=True).
        '''
        if self.thread is None:
            return False
        else:
            return self.thread.isAlive()

    def _run(self, dumbOutput=False):
        try:
            self.pid = s.Popen("./" + self.mechanism + ".exe", stdout=s.PIPE, bufsize=1)
            self.pid.wait()
            self._pp_run(dumbOutput=dumbOutput)
        except Exception as e:
            failDir = self.path + "_failed_at_{:s}".format(datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d%H%M%S"))
            self.archive( failDir )
            raise Exception('BOXMOX integration failed: {:s}'.format(str(e)))
        return

    def run(self, dumbOutput=False, asynchronous=False):
        '''
        Run BOXMOX experiment

        :param bool dumbOutput: Only load references to output files, instead of loading data? (faster, but not usable for analysis)
        :param bool asynchronous: Run asynchronous?
        '''
        self.namelist.write(os.path.join(self.path, 'BOXMOX.nml'))

        for type in self.input:
            with open( os.path.join(self.path, type + '.csv'), 'wb') as f:
                self.input[type].write(f, version=self.version)

        pwd = os.getcwd()
        os.chdir(self.path)

        if asynchronous:
            self.thread = threading.Thread(target=self._run, args=(dumbOutput,))
            self.thread.start()
            os.chdir(pwd)
            return
        else:
            self._run(dumbOutput=dumbOutput)
            os.chdir(pwd)

    def _pp_run(self, dumbOutput=False):
        try:
            self.log = []
            for line in iter(self.pid.stdout.readline, b''):
                self.log.append(line.replace('\n',''))
        except:
            pass

        if dumbOutput:
            self._populateDumbOutput()
        else:
            self._populateOutput()

    outputTypes = {  'Concentrations': { 'ending': '.conc',     'class': ConcentrationOutput },
                     'Rates':          { 'ending': '.rates',    'class': RatesOutput },
                     'Jacobian':       { 'ending': '.jacobian', 'class': JacobianOutput },
                     'Hessian':        { 'ending': '.hessian',  'class': HessianOutput },
                     'Adjoint':        { 'ending': '.adjoint',  'class': AdjointOutput } }

    def _populateDumbOutput(self, filename="*"):
        for tname in self.outputTypes:
            otype = self.outputTypes[tname]

            fnames = [ x for x in os.listdir(self.path) if x.endswith(otype['ending']) and fnmatch.fnmatch(x, filename+otype['ending']) ]
            if len(fnames) > 0:
                if len(fnames) > 1:
                    raise Exception('Multiple output files found in path {:s} for type {:s}: {:s}'.format(self.path, tname, ', '.join(fnames)))
                self.output[tname] = Output(os.path.join(self.path, fnames[0]))

    def _populateOutput(self, filename="*"):
        for tname in self.outputTypes:
            otype = self.outputTypes[tname]

            fnames = [ x for x in os.listdir(self.path) if x.endswith(otype['ending']) and fnmatch.fnmatch(x, filename+otype['ending']) ]
            if len(fnames) > 0:
                if len(fnames) > 1:
                    raise Exception('Multiple output files found in path {:s} for type {:s}: {:s}'.format(self.path, tname, ', '.join(fnames)))
                self.output[tname] = otype['class'](os.path.join(self.path, fnames[0]))

        if 'Concentrations' in self.output.keys() and 'Rates' in self.output.keys():
            self.fluxes  = FluxParser(self.output)
        if 'Concentrations' in self.output.keys():
            try:
                self.plotter = ExperimentPlotter(self.output, self.fluxes)
            except:
                pass

    def plot(self, specs, **kwargs):
        '''
        Shortcut to plotter.concentrations for quick timeline plotting
        '''
        if not self.plotter is None:
            self.plotter.concentrations(specs, **kwargs)
        else:
            import warnings
            warnings.warn('Plotter not useable - is matplotlib installed?')

    def archive(self, archive_path):
        '''
        Save BOXMOX experiment to archive path
        '''
        try:
            shutil.copytree(self.path, archive_path)
        except Exception as e:
            raise Exception('Archiving experiment at {:s} to {:s} did not work: {:s}'.format(self.path, archive_path, str(e)))

    def __del__(self):
        def deldidntwork(fun, path, excinfo):
            raise IOError('Could not remove experiment path {:s}: {:s}'.format(path, excinfo))
        if self.removeOnDel:
            shutil.rmtree(self.path, onerror=deldidntwork)

class ExperimentFromExample(Experiment):
    '''
    A BOXMOX experiment based on an example from the BOXMOX installation.
    '''
    def __init__(self, example):
        import uuid

        self.name = str(uuid.uuid4())
        self.example = example

        self.path = os.path.join(work_path, self.name)

        self.log         = None

        self.pid         = None
        self.thread      = None

        self.input       = {}
        self.output      = {}

        self.plotter     = None
        self.fluxes      = None

        self.__new()

        self.namelist = Namelist(os.path.join(self.path, 'BOXMOX.nml'))
        self.mechanism = self._get_mechanism()

        self.version  = self._determineVersion(self.path)

    def __new(self):
        try:
            s.check_output(["new_BOXMOX_experiment_from_example", "-f", self.example, self.path], stderr=s.STDOUT)
            self._populateInput()
        except s.CalledProcessError as e:
            raise Exception("Creating new experiment failed: " + str(e.output))

class ExperimentFromExistingRun(Experiment):
    '''
    A BOXMOX experiment using an existing experiment.
    '''
    removeOnDel = False

    def __init__(self, path, filename="*"):
        '''
        :param str path: path to the existing run
        :param str filename: file name to look for (e.g., for MOZART_4.conc, MOZART_4.rates ...,
                            filename would be "MOZART_4")
        '''
        import uuid

        self.name = str(uuid.uuid4())

        self.path = os.path.abspath(path)

        self.log         = None

        self.pid         = None
        self.thread      = None

        self.input       = {}
        self.output      = {}

        self.plotter     = None
        self.fluxes      = None

        self.namelist = Namelist(os.path.join(self.path, 'BOXMOX.nml'))
        self.mechanism = self._get_mechanism()

        self.version  = self._determineVersion(self.path)

        self._populateInput()
        self._populateOutput(filename=filename)




