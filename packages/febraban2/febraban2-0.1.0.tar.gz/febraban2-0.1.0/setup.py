from distutils.core import setup

version = "0.1.0"
setup(
    name='febraban2',
    packages=['febraban2'],
    version=version,
    description='A library to generate files that conform to the FEBRABAN formats',
    author='Hummingbird Product Studio',
    author_email='deromir.neves@hummingbird.com.br',
    url='https://github.com/HummingbirdStudio/febraban.git',
    download_url='https://github.com/HummingbirdStudio/febraban/archive/v%s.tar.gz' % version,
    keywords=['febraban', 'cnab', 'transfer', 'billing', 'bank']
)