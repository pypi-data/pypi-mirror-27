from setuptools import setup, find_packages
pkg = "jikan_sqlalchemy_utils"
ver = '0.0.4'
setup(
    name             = pkg,
    version          = ver,
    description      = "jikan sqlalchemy utilities",
    author           = "jikan@cock.li",
    author_email     = "jikan@cock.li",
    license          = "LGPLv3",
    url              = "https://hydra.bacontoast.org/f/jikan_sqlalchemy_utils/",
    packages         = find_packages(),
    install_requires = ['sqlalchemy>=1'],
    classifiers      = ["Programming Language :: Python :: 3 :: Only"])
