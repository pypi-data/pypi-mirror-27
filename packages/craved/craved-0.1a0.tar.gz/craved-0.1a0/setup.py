from setuptools import setup, find_packages

setup(
	name = "craved", #name of the package
	version = "0.1.alpha", #version 0.1
	packages = find_packages(), # automatically find packeges -- ['gap','sample']

	#Issue : numpy dependency for hdbscan built
	install_requires = ['matplotlib', 'seaborn', 'scipy', 'pandas', 'sklearn', 'h5py', 'cython', 'hdbscan', 'numpy', ],

	author = "R Mukesh",
	author_email = "reghu.mukesh@gmail.com",
	description = "Buddi-CRAVeD",
	long_description = "ClusteR Analysis and Validation for largE Datasets",
	license = "3-clause BSD",
	url = "https://github.com/elixir-code/craved",
)