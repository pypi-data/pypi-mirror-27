from setuptools import setup
pkg = "generic_escape"
ver = '1.1.3'

with open(pkg+'/version.py', 'wt') as h:
    h.write('__version__ = "{}"\n'.format(ver))

setup(name             = pkg,
      version          = ver,
      description      = "A simple library for escaping and unescaping strings",
      author           = "Eduard Christian Dumitrescu",
      license          = "LGPLv3",
      url              = "https://hydra.ecd.space/f/generic_escape/",
      packages         = [pkg],
      install_requires = [],
      classifiers      = ["Programming Language :: Python :: 3 :: Only"])
