from distutils.core import setup

setup(
    name='magnetmatter',
    version='0.0.6',
    packages=['magnetmatter','magnetmatter\\modules'],
    license='MIT',
    author='Pelle Garbus',
    author_email='garbus@inano.au.dk',
    description='Material science neutron and X-Ray diffraction data visualization',
    long_description=open('README.md').read(),
    install_requires=["numpy","pandas","matplotlib"],
    url = 'https://github.com/pgarbus/magnetmatter',
)
