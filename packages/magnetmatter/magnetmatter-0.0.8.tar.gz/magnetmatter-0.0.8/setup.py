from distutils.core import setup
import os

setup(
    name='magnetmatter',
    version='0.0.8',
    packages=['magnetmatter',os.path.join('magnetmatter','modules')],
    license='MIT',
    author='Pelle Garbus',
    author_email='garbus@inano.au.dk',
    description='Material science neutron and X-Ray diffraction FullProf data visualization',
    long_description=open('README.txt').read(),
    install_requires=["numpy","pandas","matplotlib"],
    url = 'https://github.com/pgarbus/magnetmatter',
)
