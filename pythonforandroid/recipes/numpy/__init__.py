from pythonforandroid.recipe import CompiledComponentsPythonRecipe
from pythonforandroid.logger import shprint, info
from pythonforandroid.util import current_directory
from multiprocessing import cpu_count
from os.path import join
import glob
import sh


class NumpyRecipe(CompiledComponentsPythonRecipe):

    version = '1.18.1'
    url = 'https://pypi.python.org/packages/source/n/numpy/numpy-{version}.zip'
    site_packages_name = 'numpy'
    depends = ['setuptools', 'cython']
    install_in_hostpython = True
    call_hostpython_via_targetpython = False

    patches = [
        join('patches', 'hostnumpy-xlocale.patch'),
        join('patches', 'remove-default-paths.patch'),
        join('patches', 'add_libm_explicitly_to_build.patch'),
        join('patches', 'compiler_cxx_fix.patch'),
        ]

    call_hostpython_via_targetpython = False

    def get_recipe_env(self, arch=None, with_flags_in_cc=True):
        env = super().get_recipe_env(arch, with_flags_in_cc)
        
        env['LDFLAGS'] += ' -lm'
        
        return env

    def build_compiled_components(self, arch):
        self.setup_extra_args = ['-j', str(cpu_count())]
        super().build_compiled_components(arch)
        self.setup_extra_args = []

    def rebuild_compiled_components(self, arch, env):
        self.setup_extra_args = ['-j', str(cpu_count())]
        super().rebuild_compiled_components(arch, env)
        self.setup_extra_args = []


recipe = NumpyRecipe()
