from setuptools import setup

setup(
	name='rpi_featureSelection_python_tools',  # This is the name of your PyPI-package. 
	version= '2.0.1',  # Update the version number for new releases
	author= 'Keyi Liu',
	entry_points = {
		'd3m.primitive': [
			'STMBFeatureSelector.STMBFeatureSelector = rpi_featureSelection_python_tools.STMBFeatureSelector:STMBFeatureSelector',
			'STMBPlusFeatureSelector.STMBPlusFeatureSelector = rpi_featureSelection_python_tools.STMBPlusFeatureSelector:STMBPlusFeatureSelector',
			'JMIFeatureSelector.JMIFeatureSelector = rpi_featureSelection_python_tools.JMIFeatureSelector:JMIFeatureSelector'
		],
	},
	packages=['rpi_featureSelection_python_tools']
)
