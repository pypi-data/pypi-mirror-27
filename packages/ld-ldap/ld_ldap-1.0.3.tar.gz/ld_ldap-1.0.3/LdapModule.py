#!/usr/bin/python3
#-*- coding: utf-8 -*-


"""
Esta modulo ira interagir com o LDAP utilizando o modulo ldap3.
As configurações e parametros podem ser encontrados na documentação: http://ldap3.readthedocs.io/
"""

from ldap3 import Server, Connection, ALL, SUBTREE, MODIFY_REPLACE
from os import path
from yaml import load
from hashlib import md5
from base64 import b64encode
from unicodedata import normalize



class LdapModule(object):

    """
    Este método irá ler o arquivo config.yml (para atribuir usuário e senha) e conectar com o servidor LDAP.
    O seu retorno será o próprio método de conexão (a partir da variavel self.connection).
    Caso ocorra algum erro, será exibido na tela.
    """

    def __init__(self):
        with open(path.expanduser('~/config/config.yml'), 'r') as yml:
            self.config = load(yml).get('ldap')
        self.server = Server(self.config['server'], get_info=ALL)
        self.connection = Connection(self.server, user=self.config['user'], password=self.config['password'])
        if not self.connection.bind():
            print('error in bind', self.connection.result)


    """
    Este método é o responsável por adicionar novos usuários no LDAP.
    Ele deve receber como parametros obrigatórios nome e senha, e opcionais o ID do usuário.
    O próprio método faz as tratativas de usuário, login e cria um hash MD5 para senha.
    Seu retorno será uma mensagem informando se foi adicionado ou se ocorreu algum erro.
    """

    def add_user(self, nome, senha, id=1500):
        try:
            #define os padrões de login (nome.sobrenome) e apenas o sobrenome
            nome_lista = nome.split()
            login = normalize('NFKD', "%s.%s" %(nome_lista[0],nome_lista[-1])).encode('ASCII','ignore').decode('ASCII').lower()
            sobrenome = nome_lista[-1]

            #gera o hash md5 para senha
            m = md5()
            m.update(senha.encode('utf-8'))
            md5string=m.digest()
            senha = "{MD5}" + b64encode(md5string).decode()


            dominio = self.config['dominio']
            dc = self.config['dc']

            # adiciona o usuario no LDAP
            # este metodo precisa ser editado conforme a estrutura do LDAP
            self.connection.add('cn=%s,cn=USERS,%s'%(nome,dc),
                                ['inetOrgPerson','organizationalPerson','person','posixAccount','top'],
                                {'uid':'%s'%login, 
                                'uidNumber':id, 
                                'gidNumber':id,
                                'homeDirectory':'/home/%s'%login,
                                'givenName': '%s'%nome,
                                'sn':'%s'%sobrenome,
                                'mail': '%s@%s'%(login, dominio),
                                'userPassword':'%s'%senha})
            return 'Usuario adicionado com sucesso'
        except Exception as e:
            return ('Erro ao cadastrar %s' %e)

    """
    Este método é responsável por mover uma entrada para o grupo INACTIVE do LDAP.
    Ela deve receber como parametro o nome de quem será desativado.
    Seu retorno será uma mensagem informando se foi desativado ou se ocorreu algum erro.
    """    
    
    def inative_user(self, nome):
        try:
            dc = self.config['dc']
             # este metodo precisa ser editado conforme a estrutura do LDAP
            self.connection.modify_dn('cn=%s,cn=USERS,%s'%(nome,dc),
                                      'cn=%s'%nome,
                                       new_superior='cn=INACTIVE,%s'%dc)
            return ('Usuario movido ao grupo INACTIVE')
        except Exception as e:
            return ('Erro ao editar usuario: %s' %e)


