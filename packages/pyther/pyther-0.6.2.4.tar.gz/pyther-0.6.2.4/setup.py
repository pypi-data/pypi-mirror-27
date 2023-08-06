
from distutils.core import setup
#from setuptools import setup, find_packages


def find_data_files(source, target, patterns):
    """
    Locates the specified data-files and returns the matches in a data_files
    compatible format. source is the root of the source data tree.

    Use '' or '.' for current directory. target is the root of the target
    data tree.

    Use '' or '.' for the distribution directory. patterns is a sequence of
    glob-patterns for the files you want to copy.
    """
    if glob.has_magic(source) or glob.has_magic(target):
        raise ValueError("Magic not allowed in src, target")
    ret = {}
    for pattern in patterns:
        pattern = os.path.join(source,pattern)
        for filename in glob.glob(pattern):
            if os.path.isfile(filename):
                targetpath = os.path.join(target,os.path.relpath(filename,source))
                path = os.path.dirname(targetpath)
                ret.setdefault(path,[]).append(filename)
    return sorted(ret.items())


setup(
	name = "pyther",
	packages = ["pyther"],
	version = "0.6.2.4",
	description = "A open source library for processing thermodynamics data",
	author = "pysg",
	author_email = "andres.pyther@gmail.com",
	url = "https://github.com/pysg/pyther",
	package_data = {'pyther': ['*.xls']},
	keyword = ["data analytics", "phases diagram", "thermodynamics"]

)

# python3 setup.py register -r pypi
# python3 setup.py register sdist upload -r pypi
