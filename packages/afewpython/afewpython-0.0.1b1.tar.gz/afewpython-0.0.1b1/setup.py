from setuptools import setup, find_packages

setup(
    name="afewpython",
    version="0.0.1.beta1",
    author="Zeus",
    license="MIT",
    package_dir={'':'src'},
    packages=find_packages(where='./src',exclude=['tests*']),
    url="https://afewusefulpython.readthedocs.io/en/latest/?",
    discription="It is a trial fun package created to understand git, gitlab and github with continuous integration and deployment.",
    install_requires=[]
)