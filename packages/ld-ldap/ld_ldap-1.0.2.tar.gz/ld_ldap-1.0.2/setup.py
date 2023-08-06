from distutils.core import setup
from pip.req import parse_requirements


setup (
    name            = 'ld_ldap',
    version         = '1.0.2',
    py_modules      = ['LdapModule'],
    url            = 'https://github.com/4linux/ld_ldap',
    install_requires= ['ldap3','PyYAML'],
    author          = 'Mariana Albano',
    author_email    = 'mariana.albano@4linux.com.br',
    description     = 'Este modulo ira realizar criacao e alteracao de usuarios utilizando o ldap3.'
)