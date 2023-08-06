from distutils.core import setup
from pip.req import parse_requirements


setup (
    name            = 'ld_zimbra',
    version         = '1.0.3',
    py_modules      = ['ZimbraModule'],
    url             = 'https://github.com/4linux/ld_zimbra',
    install_requires= ['requests','PyYAML','beautifulsoup4'],
    author          = 'Mariana Albano',
    author_email    = 'mariana.albano@4linux.com.br',
    description     = 'Este modulo ira realizar o alterações no zimbra utilizando sua API SOAP.'
)
