from setuptools import setup

setup(
	name='hid_converge',
	version='2.0.1.1',
	author='HID',
	license='Thermofisher Scientific',
	packages=['authentication',
			'Queue','QueueModule'],
	install_requires=['xlsxwriter','requests','simplejson'],
	dependency_links=['https://pypi.python.org/pypi/XlsxWriter',
					'https://pypi.python.org/pypi/simplejson',
					'https://pypi.python.org/pypi/requests'],
	include_package_data=True,
	zip_safe=False
)
