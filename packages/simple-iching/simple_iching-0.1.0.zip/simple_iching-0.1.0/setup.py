from setuptools import setup

setup(
	name='simple_iching',
	packages=['simple_iching'],
	version="0.1.0",
	description="A simple I Ching package",
	url="https://github.com/dmallubhotla/iching",
	package_data={
		"simple_iching": ["*.csv"],
	},
	entry_points={
		"console_scripts": [
			"iching=simple_iching.iching:main"
		]
	}
)
