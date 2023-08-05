# Copyright 2015-2017 The MathWorks, Inc.

from setuptools import setup
from distutils.command.clean import clean
from distutils.command.install import install

class InstallRuntime(install):
    # Calls the default run command, then deletes the build area 
    # (equivalent to "setup clean --all").
    def run(self):
        install.run(self)
        c = clean(self.distribution)
        c.all = True
        c.finalize_options()
        c.run()

if __name__ == '__main__':

    setup(
        name="rpi_test",
        version="1.0.0",
        description='A module to call RPI MATLAB primitives from Python3.6',
        author='Keyi Liu',

        platforms=['Linux', 'Windows', 'MacOS'],
        packages=[
            'rpi_test'
        ],
        package_data={'rpi_featureSelection_matlab_tools': ['*.ctf']},
        # Executes the custom code above in order to delete the build area.
        cmdclass={'install': InstallRuntime}
    )


