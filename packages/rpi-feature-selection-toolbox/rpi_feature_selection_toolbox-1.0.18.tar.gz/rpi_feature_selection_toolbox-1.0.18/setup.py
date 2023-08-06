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
        name="rpi_feature_selection_toolbox",
        version="1.0.18",
        description='A novel and robust Feature Selection toolbox for all types of classification problems',
        author='Keyi Liu, Zijun Cui, Qiang Ji',
        url='https://www.ecse.rpi.edu/~cvrl/',

        entry_points = {
        'd3m.primitives': [
            'rpi_feature_selection_toolbox.IPCMBplus_Selector = rpi_feature_selection_toolbox.feature_selector:IPCMBplus_Selector',
            'rpi_feature_selection_toolbox.JMIplus_Selector = rpi_feature_selection_toolbox.feature_selector:JMIplus_Selector',
            'rpi_feature_selection_toolbox.STMBplus_Selector = rpi_feature_selection_toolbox.feature_selector:STMBplus_Selector',
            'rpi_feature_selection_toolbox.aSTMBplus_Selector = rpi_feature_selection_toolbox.feature_selector:aSTMBplus_Selector',
            'rpi_feature_selection_toolbox.pSTMB_Selector = rpi_feature_selection_toolbox.feature_selector:pSTMB_Selector',
            'rpi_feature_selection_toolbox.sSTMBplus_Selector = rpi_feature_selection_toolbox.feature_selector:sSTMBplus_Selector',
            'rpi_feature_selection_toolbox.F_STMB_Selector = rpi_feature_selection_toolbox.feature_selector:F_STMB_Selector',
            'rpi_feature_selection_toolbox.F_aSTMB_Selector = rpi_feature_selection_toolbox.feature_selector:F_aSTMB_Selector',
            'rpi_feature_selection_toolbox.F_sSTMB_Selector = rpi_feature_selection_toolbox.feature_selector:F_sSTMB_Selector',
            'rpi_feature_selection_toolbox.JMIp_Selector = rpi_feature_selection_toolbox.feature_selector:JMIp_Selector',
            ],
        },

        platforms=['Linux', 'Windows', 'MacOS'],
        packages=[
            'rpi_feature_selection_toolbox'
        ],
        package_data={'rpi_feature_selection_toolbox': ['*.ctf']},
        # Executes the custom code above in order to delete the build area.
        cmdclass={'install': InstallRuntime}
    )


