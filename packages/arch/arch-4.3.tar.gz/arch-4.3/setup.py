from __future__ import print_function

import glob
import os
import re
import subprocess
import sys
from distutils.errors import CCompilerError, DistutilsExecError, DistutilsPlatformError
from distutils.version import StrictVersion

import pkg_resources
import versioneer
from Cython.Build import cythonize
from setuptools import Command, Extension, find_packages, setup
from setuptools.dist import Distribution

CYTHON_COVERAGE = os.environ.get('ARCH_CYTHON_COVERAGE', '0') in ('true', '1', 'True')
if CYTHON_COVERAGE:
    print('Building with coverage for cython modules, ARCH_CYTHON_COVERAGE=' +
          os.environ['ARCH_CYTHON_COVERAGE'])

try:
    from Cython.Distutils.build_ext import build_ext as _build_ext
    
    CYTHON_INSTALLED = True
except ImportError:
    CYTHON_INSTALLED = False
    if CYTHON_COVERAGE:
        raise ImportError('cython is required for cython coverage. Unset '
                          'ARCH_CYTHON_COVERAGE')
    
    
    class _build_ext(object):
        pass

FAILED_COMPILER_ERROR = """
******************************************************************************
*                               WARNING                                      *
******************************************************************************

Unable to build binary modules for arch.  While these are not required to run 
any code in the package, it is strongly recommended to either compile the 
extension modules or to use numba. 

******************************************************************************
*                               WARNING                                      *
******************************************************************************
"""

cmdclass = versioneer.get_cmdclass()


# prevent setup.py from crashing by calling import numpy before
# numpy is installed
class build_ext(_build_ext):
    def build_extensions(self):
        numpy_incl = pkg_resources.resource_filename('numpy', 'core/include')
        
        for ext in self.extensions:
            if (hasattr(ext, 'include_dirs') and
                        numpy_incl not in ext.include_dirs):
                ext.include_dirs.append(numpy_incl)
        _build_ext.build_extensions(self)


SETUP_REQUIREMENTS = {'numpy': '1.10'}
REQUIREMENTS = {'Cython': '0.24',
                'matplotlib': '1.5',
                'scipy': '0.16',
                'pandas': '0.18',
                'statsmodels': '0.8'}

ALL_REQUIREMENTS = SETUP_REQUIREMENTS.copy()
ALL_REQUIREMENTS.update(REQUIREMENTS)

cmdclass['build_ext'] = build_ext


class BinaryDistribution(Distribution):
    def is_pure(self):
        return False


class CleanCommand(Command):
    user_options = []
    
    def run(self):
        raise NotImplementedError('Use git clean -xfd instead')
    
    def initialize_options(self):
        pass
    
    def finalize_options(self):
        pass


cmdclass['clean'] = CleanCommand


def strip_rc(version):
    return re.sub(r"rc\d+$", "", version)


# Polite checks for numpy, scipy and pandas.  These should not be upgraded,
# and if found and below the required version, refuse to install
missing_package = '{package} is installed, but the version installed' \
                  ', {existing_ver}, is less than the required version ' \
                  'of {required_version}. This package must be manually ' \
                  'updated.  If this isn\'t possible, consider installing ' \
                  'in an empty virtual environment.'

PACKAGE_CHECKS = ['numpy', 'scipy', 'pandas']
for key in PACKAGE_CHECKS:
    version = None
    satisfies_req = True
    existing_version = 'Too Old to Detect'
    if key == 'numpy':
        try:
            import numpy
            
            try:
                from numpy.version import short_version as version
            except ImportError:
                satisfies_req = False
        except ImportError:
            pass
    
    elif key == 'scipy':
        try:
            import scipy
            
            try:
                from scipy.version import short_version as version
            except ImportError:
                satisfies_req = False
        except ImportError:
            pass
    
    elif key == 'pandas':
        try:
            import pandas
            if not hasattr(pandas, '__version__'):
                raise AttributeError
        except AttributeError:
            try:
                from pandas.version import short_version as version
            except ImportError:
                satisfies_req = False
    else:
        raise NotImplementedError('Unknown package')
    
    if version:
        existing_version = StrictVersion(strip_rc(version))
        satisfies_req = existing_version >= ALL_REQUIREMENTS[key]
    if not satisfies_req:
        requirement = ALL_REQUIREMENTS[key]
        message = missing_package.format(package=key,
                                         existing_ver=existing_version,
                                         required_version=requirement)
        raise EnvironmentError(message)

cwd = os.getcwd()

# Convert markdown to rst for submission
long_description = ''
try:
    cmd = 'pandoc --from=markdown --to=rst --output=README.rst README.md'
    proc = subprocess.Popen(cmd, shell=True)
    proc.wait()
    long_description = open(os.path.join(cwd, "README.rst")).read()
except IOError as e:
    import warnings
    
    warnings.warn('Unable to convert README.md.  Most likely because pandoc '
                  'is not installed')

# Convert examples notebook to rst for docs
try:
    from nbconvert.utils.exceptions import ConversionException
    from nbconvert.utils.pandoc import PandocMissing
except ImportError as e:
    ConversionException = PandocMissing = ValueError

try:
    import nbformat as nbformat
    from nbconvert import RSTExporter
    
    notebooks = glob.glob(os.path.join(cwd, 'examples', '*.ipynb'))
    for notebook in notebooks:
        try:
            with open(notebook, 'rt') as f:
                example_nb = f.read()
            
            rst_path = os.path.join(cwd, 'doc', 'source')
            path_parts = os.path.split(notebook)
            nb_filename = path_parts[-1]
            nb_filename = nb_filename.split('.')[0]
            source_dir = nb_filename.split('_')[0]
            rst_filename = os.path.join(cwd, 'doc', 'source',
                                        source_dir, nb_filename + '.rst')
            
            example_nb = nbformat.reader.reads(example_nb)
            rst_export = RSTExporter()
            (body, resources) = rst_export.from_notebook_node(example_nb)
            with open(rst_filename, 'wt') as rst:
                rst.write(body)
            
            for key in resources['outputs'].keys():
                if key.endswith('.png'):
                    resource_filename = os.path.join(cwd, 'doc', 'source',
                                                     source_dir, key)
                    with open(resource_filename, 'wb') as resource:
                        resource.write(resources['outputs'][key])
        
        except Exception:
            import warnings
            
            warnings.warn('Unable to convert {original} to {target}.  This '
                          'only affects documentation generation and not the '
                          'operation of the '
                          'module.'.format(original=notebook,
                                           target=rst_filename))
            print('The last error was:')
            import sys
            
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])

except Exception:
    import warnings
    
    warnings.warn('Unable to import required modules from the jupyter project.'
                  ' This only affects documentation generation and not the '
                  'operation of the module.')
    print('The last error was:')
    import sys
    
    print(sys.exc_info()[0])
    print(sys.exc_info()[1])


def run_setup(binary=True):
    if not binary:
        del REQUIREMENTS['Cython']
        extensions = []
    else:
        directives = {'linetrace': CYTHON_COVERAGE}
        macros = []
        if CYTHON_COVERAGE:
            macros.append(('CYTHON_TRACE', '1'))
        
        ext_modules = []
        ext_modules.append(Extension("arch.univariate.recursions",
                                     ["./arch/univariate/recursions.pyx"],
                                     define_macros=macros))
        ext_modules.append(Extension("arch.bootstrap._samplers",
                                     ["./arch/bootstrap/_samplers.pyx"],
                                     define_macros=macros))
        extensions = cythonize(ext_modules,
                               force=CYTHON_COVERAGE,
                               compiler_directives=directives)
    
    setup(name='arch',
          license='NCSA',
          version=versioneer.get_version(),
          description='ARCH for Python',
          long_description=long_description,
          author='Kevin Sheppard',
          author_email='kevin.sheppard@economics.ox.ac.uk',
          url='http://github.com/bashtage/arch',
          packages=find_packages(),
          ext_modules=extensions,
          package_dir={'arch': './arch'},
          cmdclass=cmdclass,
          keywords=['arch', 'ARCH', 'variance', 'econometrics', 'volatility',
                    'finance', 'GARCH', 'bootstrap', 'random walk', 'unit root',
                    'Dickey Fuller', 'time series', 'confidence intervals',
                    'multiple comparisons', 'Reality Check', 'SPA', 'StepM'],
          zip_safe=False,
          include_package_data=True,
          distclass=BinaryDistribution,
          classifiers=[
              'Development Status :: 5 - Production/Stable',
              'Intended Audience :: End Users/Desktop',
              'Intended Audience :: Financial and Insurance Industry',
              'Programming Language :: Python :: 2.7',
              'Programming Language :: Python :: 3.4',
              'Programming Language :: Python :: 3.5',
              'License :: OSI Approved',
              'Operating System :: MacOS :: MacOS X',
              'Operating System :: Microsoft :: Windows',
              'Operating System :: POSIX',
              'Programming Language :: Python',
              'Programming Language :: Cython',
              'Topic :: Scientific/Engineering',
          ],
          install_requires=[key + '>=' + REQUIREMENTS[key]
                            for key in REQUIREMENTS],
          setup_requires=[key + '>=' + SETUP_REQUIREMENTS[key]
                          for key in SETUP_REQUIREMENTS],
          )


try:
    build_binary = '--no-binary' not in sys.argv and CYTHON_INSTALLED
    if '--no-binary' in sys.argv:
        sys.argv.remove('--no-binary')
    
    run_setup(binary=build_binary)
except (CCompilerError, DistutilsExecError, DistutilsPlatformError, IOError, ValueError):
    run_setup(binary=False)
    import warnings
    
    warnings.warn(FAILED_COMPILER_ERROR, UserWarning)
