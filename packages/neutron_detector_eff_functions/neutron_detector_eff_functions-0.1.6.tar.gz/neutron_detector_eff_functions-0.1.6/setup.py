from distutils.core import setup

setup(
    name='neutron_detector_eff_functions',
    packages=['neutron_detector_eff_functions'],
    version='0.1.6',
    description='A library to calculate Neutron detector theoretical efficiency',
    author='acarmona',
    author_email='acarmona@opendeusto.es',
    url='https://github.com/alvcarmona/neutronDetectorEffFunctions',  # URL to the github repo
    download_url='https://github.com/alvcarmona/neutronDetectorEffFunctions/archive/0.1.6.tar.gz',
    keywords=['science'],
    install_requires=[
        'numpy',
        'matplotlib',
        'scipy',
        'pylab',
    ],
    classifiers=[],
    include_package_data=True
)
