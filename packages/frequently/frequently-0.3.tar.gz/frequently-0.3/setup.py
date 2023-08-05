from setuptools import setup,find_packages

install_requires=['clmenu','pyaml']
version='0.3'

with open("README.md","r") as f:
	long_desc=f.read()


setup(
	name='frequently',
	description="Quickly run scripts from other directories or open frequently visited websites",
	long_description=long_desc,
	version=version,
	author="Jordan Patterson",
	author_email="jordan.patterson2398@gmail.com",
	url="https://github.com/jordan-patterson/frequently",
	license='MIT',
	scripts=['freq'],
	packages=["freq"],
	package_data={'logo':'logo.txt'},
	install_requires=install_requires
	)