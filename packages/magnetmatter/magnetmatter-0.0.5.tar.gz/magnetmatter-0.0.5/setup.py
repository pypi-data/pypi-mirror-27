from distutils.core import setup

setup(
    name='magnetmatter',
    version='0.0.5',
    packages=['magnetmatter','magnetmatter\\modules'],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    author='Pelle Garbus',
    author_email='garbus@inano.au.dk',
    long_description=open('README.txt').read(),
    install_requires=["numpy","pandas","matplotlib"],
)
