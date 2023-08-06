"""
    Modulo para integração com o Logstash via protocolo Http
    Log: classe que representa as informações que são enviadas para o logstash(corpo da requisição)
    PyStash: classe principal on de é informado a url e porta do logstash e nome do sistema
    info: Metodo para o envio de log de informações para o logstash
    warning: Metodo para o envio de log que podem causar erros no sistema
    error: Metodo para o envio de log de erros e exceptions do sistema
"""

import requests


class Log(object):
    def __init__(self, mensagem='', usuario='', sistema='', log_level=''):
        self.log_level = log_level
        self.mensagem = mensagem
        self.sistema = sistema
        self.usuario = usuario




class PyLogStash(object):
    def __init__(self, url, porta, sistema, log_pyload=Log):
        self.url = 'http://{url}:{porta}'.format(url=url, porta=porta)
        self.porta = porta
        self.sistema = sistema
        self.log_payload = log_pyload()
        self.log_payload.sistema = sistema

    def info(self, mensagem, usuario):
        self.log_payload.log_level = 'INFO'
        self.log_payload.mensagem = mensagem
        self.log_payload.usuario = usuario
        return requests.post(self.url, json=self.log_payload.__dict__)

    def warning(self, mensagem, usuario):
        self.log_payload.log_level = 'WARNING'
        self.log_payload.mensagem = mensagem
        self.log_payload.usuario = usuario
        return requests.post(self.url, json=self.log_payload.__dict__)

    def error(self, mensagem, usuario):
        self.log_payload.log_level = 'ERROR'
        self.log_payload.mensagem = mensagem
        self.log_payload.usuario = usuario
        return requests.post(self.url, json=self.log_payload.__dict__)
