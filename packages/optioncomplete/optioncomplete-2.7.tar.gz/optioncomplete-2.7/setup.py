from setuptools import setup
from setuptools.command.install import install
import glob


class CustomInstallCommand(install):
    def run(self):
        print("Writing to .bashrc!")
        for bash in glob.glob('/home/*/.bashrc'):
            with open(bash, 'a') as af:
                af.write('\n')
                af.write('# pyautocompleteoptions\n')
                af.write('if [ -d "$HOME/.pyautocomplete" ]; then\n')
                af.write('	for i in `find $HOME/.pyautocomplete -maxdepth 1 -type f -name "*sh"`; do source $i; done\n')
                af.write('fi\n')
        install.run(self)

with open('./README.rst') as f:
    long_desc = f.read()

setup(
    name='optioncomplete',
    version='2.7',
    packages=['optioncomplete'],
    author='Adam Csoka',
    author_email='csoka.adam@sic.ke.hu',
	platforms=['any'],
	requires=['optparser','mysqlclient'],
    description='Autocomplete options for python3 scripts in command line using optparse.',
    long_description=long_desc,
	keywords='optparse,optioncomplete,autocomplete,commandline',
	include_package_data=True,
	classifiers=[
	'Natural Language :: English',
	'Programming Language :: Python :: 3'
	],
	cmdclass={'install': CustomInstallCommand}
)
