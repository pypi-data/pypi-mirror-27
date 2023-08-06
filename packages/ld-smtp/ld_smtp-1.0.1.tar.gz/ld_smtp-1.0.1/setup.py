from distutils.core import setup
from pip.req import parse_requirements


setup (
    name            = 'ld_smtp',
    version         = '1.0.1',
    py_modules      = ['SMTPModule'],
    url             = 'https://github.com/4linux/ld_smtp',
    install_requires= ['Jinja2','PyYAML'],
    author          = 'Mariana Albano',
    author_email    = 'mariana.albano@4linux.com.br',
    description     = 'Este modulo ira realizar o envio de e-mail utilizando o smtplib.'
)