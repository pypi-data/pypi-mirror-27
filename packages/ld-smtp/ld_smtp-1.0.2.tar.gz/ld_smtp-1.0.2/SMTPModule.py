#!/usr/bin/python3
#-*- coding: utf-8 -*-

"""
Este módulo irá realizar o envio de e-mail utilizando o smtplib.
Maiores informações sobre o módulo: https://docs.python.org/3/library/smtplib.html
"""

from smtplib import SMTP
from email.mime.text import MIMEText
from yaml import load
from os import path
from jinja2 import Template

class Email(object):

    """
    Este método irá fazer a conexão com o servidor de e-mail, as informações de usuário, senha, servidor e porta são
    obtidas através do arquivo /config/config.yml
    A variável "me" identifica quem enviou o e-mail.
    """

    def __init__(self):
        with open(path.expanduser('~/config/config.yml'), 'r') as yml:
            config = load(yml).get('smtp')
        self.smtp = SMTP()
        self.smtp.connect(config['server'], config['port'])
        self.smtp.ehlo()

        if config['env'] == 'prod':
            self.smtp.starttls()
            self.smtp.login(config['user'], config['password'])
        
        self.me = config['user']


    """
    Este método fará o envio das mensagens, ele deve receber os seguintes parametros:
    msg.email: deve ser uma lista contendo todos os destinatários
    msg.mensagem: a mensagem a ser enviada
    msg.subject: o título do e-mail
    """

    def sendmail(self):
        try:
            mail = Template(self.mensagem)

            msg = MIMEText(mail.render(), 'html')

            msg.set_charset('utf-8')
            msg['From'] = self.me
            msg['To'] = ", ".join(self.email)
            msg['Subject'] = self.subject

            self.smtp.sendmail(self.me, self.email, msg.as_string())
        except Exception as e:
            raise Exception(e)