from setuptools import setup

setup(
	name='hid_converge_batch',
	version='2.0.1.1',
	author='HID S/W',
	license='Thermofisher Scientific',
	packages=['ngs','service','utils'],
	install_requires=['hid_converge'],
	dependency_links=['https://pypi.python.org/pypi/hid_converge'],
	include_package_data=True,
	zip_safe=False
)
