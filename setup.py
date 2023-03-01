import subprocess
import logging
from distutils.core import setup
import pathlib
from setuptools import find_packages

module_name = 'sshworm'
author = 'Nicolas DELGADO'
author_email =''
module_root_path = pathlib.Path('').absolute() / 'src'
description = 'sshworm: module that wraps python code with a single ssh tunnel (missing readme?)'

def _long_description():
        '''get long description from README.md'''
        try:
            with open('README.md') as rf:
                return rf.read()
        except IOError:
            return description

class SetupBoilerplateHelper:

    '''
    Get some meta-data from git instead of writing by hand
    '''

    def __init__(self):
        self._generated_file_name = '_generated_version.py'

    def _subprocess(self, command):
        '''Get python suprocess for launching OS independent shell commands'''
        return subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

    def _execute_command_and_get_text_or_fail(self, command):
        '''Get text from launching 'fast' commands. Fails if return code is not 0'''

        with self._subprocess(command) as subp:
            stdout, stderr = subp.communicate()
            logging.warning(subp.returncode)
            if subp.returncode != 0:
                raise EnvironmentError(
                    f'command failed in your shell: {command}\nError:{stderr.decode("utf-8").strip()}'
                )
            else:
                return stdout.decode('utf-8').strip()

    def _generate_version_file(self, version, module_root_path):
        '''Generates and saves to module root directory a python file with __version__ variable in it'''
        generated_version_file = module_root_path / self._generated_file_name

        print(f'creating or updating file: {generated_version_file} with version: {version}')

        with open(generated_version_file, mode='w') as version_file:
            version_file.write(f'__version__ = \'{version}\'\n')

    def version_from_git(self, default_version='NO_GIT_SO_UNKNOWN', module_root_path=None):
        '''executes `git describe` command and parses latest annotated tag as a module version'''
        command = ['git', 'describe', '--dirty']

        try:
            version_from_git = self._execute_command_and_get_text_or_fail(command)

            version = str(version_from_git[1:]) if (
                        version_from_git.startswith('v') or version_from_git.startswith('V')) else version_from_git

        except EnvironmentError as e:
            if default_version is None:
                raise e
            else:
                version = default_version

        if module_root_path is not None:
            self._generate_version_file(version, module_root_path)
        else:
            print(f'Warning: Not updating version inside generated file. module_root_path was not provided')

        return version

    def origin_url_from_git(self, default_url=None):
        '''Uses git remote command to extract the url from the first remote named "origin"'''
        command = ['git', 'remote', '-v']

        try:
            remote = self._execute_command_and_get_text_or_fail(command)
        except EnvironmentError as env_e:

            if default_url is None:
                raise env_e
            else:
                return default_url

        lines = remote.split('\n')
        for line in lines:
            if line.startswith('origin'):
                return line.split('\t')[1].split(' ')[0]

        raise ValueError(f'No origin remote in git repo.\n{remote}')

setup_boilerplate_helper = SetupBoilerplateHelper()

setup(
    name=module_name,
    version=setup_boilerplate_helper.version_from_git(module_root_path=module_root_path),
    # cmdclass=versioneer.get_cmdclass(),
    author=author,
    author_email=author_email,
    packages=find_packages(),
    scripts=[],
    url=setup_boilerplate_helper.origin_url_from_git(),
    include_package_data=True,
    # license='LICENSE.txt',
    description=description,
    long_description=_long_description(),

    install_requires=[],
    extras_require={
        'test': ['pytest', 'requests']
    }
)
