from setuptools import setup

setup(
    name='objdem',
    version='1.0.12',
    description='Generates an .obj file representing a digital elevation map from coordinate input',
    license="MIT",
    author='Kevin Forrest Connors',
    author_email='kevinforrestconnors@gmail.com',
    url="https://github.com/kevinforrestconnors/objdem",
    packages=['objdem'],
    install_requires=['numpy', 'scipy', 'utm']
)