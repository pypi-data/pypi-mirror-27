"""
Este modulo visa interagir com o Zimbra através da aplicação SOAP
XML de acordo com a URL : https://files.zimbra.com/docs/soap_api/8.7.11/api-reference/index.html
"""

import requests
from bs4 import BeautifulSoup
from os import path
from yaml import load

class ZimbraModule(object):

    """
    O arquivo /config/config.yml sera lido e as variaveis poderao ser acessadas a partir da variavel config.
    """
    
    with open(path.expanduser('~/config/config.yml'), 'r') as yml:
        config = load(yml).get('mail')

    """
    Este metodo gera o token de autenticacao de admin do zimbra.
    Ela utiliza o usuario e senha a partir do arquivo: /config/config.yml
    O seu retorno sera o token.
    Caso ocorra um erro, ele será informado.
    """
    
    def token(self):
        try:
            self.zimbra_user = self.config['user']
            self.zimbra_password = self.config['password']

            self.headers = { 'Content-Type': 'application/soap+xml' }

            self.xml = '<?xml version="1.0" ?> \
                        <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">\
                            <soap:Header>\
                                <context xmlns="urn:zimbraAdmin">\
                                    <format type="xml"/>\
                                </context>\
                            </soap:Header>\
                            <soap:Body>\
                                <AuthRequest xmlns="urn:zimbraAdmin">\
                                    <name>%s</name>\
                                    <password>%s</password>\
                                </AuthRequest>\
                            </soap:Body>\
                        </soap:Envelope>' % (self.zimbra_user, self.zimbra_password)

            self.url = 'https://%s:%s/service/admin/soap/server' %(self.config['server'], self.config['port'])


            auth = requests.post(self.url, data=self.xml, headers=self.headers)._content
            token = BeautifulSoup(auth, 'xml').find_all('authToken')[0].text
            return token
        except Exception as e:
            return "Ocorreu um erro ao gerar o token: %s" %e


    """
    Este metodo sera o template de XML utilizado para executar as funcionalidades.
    Ela deve receber o token de acesso e o XML referente a qual módulo será gerenciado (ambos como String).
    O seu retorno sera um XML completo para enviar na requisicao dos outros metodos.
    """

    def padrao(self, token, xml):
        xml_padrao = '<?xml version="1.0" ?> \
                <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">\
                    <soap:Header>\
                        <context xmlns="urn:zimbra">\
                            <format type="xml"/>\
                            <authToken>%s</authToken>\
                        </context>\
                    </soap:Header>\
                    <soap:Body>\
                       %s \
                    </soap:Body>\
                </soap:Envelope>' %(token, xml)
        return xml_padrao


    """
    Este metodo ira buscar o ID de um usuario.
    Ela deve receber como parametro o email (string).
    Seu retorno sera o ID do usuario.
    Caso ocorra um erro, ele será informado.
    """

    def get_account(self, account):
        try:
            self.headers = { 'Content-Type': 'application/soap+xml' }
            
            xml = '<GetAccountRequest  xmlns="urn:zimbraAdmin"> \
                       <account by="name">%s</account >\
                   </GetAccountRequest>'%account

            token = self.token()
            xml = self.padrao(token, xml)
            self.url = 'https://%s:%s/service/admin/soap/server'  %(self.config['server'], 
                                                                    self.config['port'])

            auth = requests.post(self.url, data=xml, headers=self.headers).text

            soup = BeautifulSoup(auth, 'xml')
            id = soup.find_all('account')[0].attrs['id']
            return id
        except Exception as e:
            return "Ocorreu um erro ao obter o ID do usuário: %s" %e


    """
    Este metodo sera responsavel por criar novos emails.
    Ele deve receber como parametro o e-mail e a senha (ambos como string).
    O seu retorno sera uma mensagem informando que a conta foi criada com sucesso.
    Caso ocorra um erro, ele será informado.
    """

    def create_account(self, email, password, domain):
        try:
            self.headers = { 'Content-Type': 'application/soap+xml' }
            xml = '<CreateAccountRequest name="%s" password="%s"  xmlns="urn:zimbraAdmin"> \
                       <domain by="name">%s</domain>\
                   </CreateAccountRequest>' %(email, password, domain)
            token = self.token()
            xml = self.padrao(token, xml)
            self.url = 'https://%s:%s/service/admin/soap/dl' %(self.config['server'], 
                                                               self.config['port'])

            auth = requests.post(self.url, data=xml, headers=self.headers)._content
            return "Conta criada com sucesso!"
        except Exception as e:
            return "Ocorreu um erro ao criar conta: %s" %e


    """
    Este metodo ira buscar o ID de uma lista de distribuicao.
    Ela deve receber como parametro o email desta lista (string).
    Seu retorno sera o ID da lista.
    Caso ocorra um erro, ele será informado.
    """

    def get_list_distribution(self, list):
        try:
            self.headers = { 'Content-Type': 'application/soap+xml' }
            xml = '<GetDistributionListRequest  xmlns="urn:zimbraAdmin"> \
                       <dl by="name">%s</dl>\
                   </GetDistributionListRequest>' %(list)

            token = self.token()
            xml = self.padrao(token, xml)
            self.url = 'https://%s:%s/service/admin/soap/dl' %(self.config['server'],
                                                               self.config['port'])


            auth = requests.post(self.url, data=xml, headers=self.headers).text
            soup = BeautifulSoup(auth, 'xml')
            id = soup.find_all('dl')[0].attrs['id']
            return id
        except Exception as e:
            return "Ocorreu um erro ao gerar ID da lista de distribuicao: %s" %e
        

    """
    Este metodo sera responsavel por adicionar usuarios em listas de distribuicao.
    Ele deve receber como parametro o id da lista (obtido pelo metodo get_list_distribution) e o email.
    O seu retorno sera uma mensagem informando que o usuario foi criada com sucesso.
    Caso ocorra um erro, ele será informado.
    """

    def add_member_dl(self, id, member):
        try:
            self.headers = { 'Content-Type': 'application/soap+xml' }
            xml = '<AddDistributionListMemberRequest id="%s"  xmlns="urn:zimbraAdmin"> \
                        <dlm>%s</dlm>\
                    </AddDistributionListMemberRequest>' %(id, member)
            token = self.token()
            xml = self.padrao(token, xml)
            self.url = 'https://%s:%s/service/admin/soap/dlm' %(self.config['server'],
                                                                self.config['port'])


            auth = requests.post(self.url, data=xml, headers=self.headers)._content
            return "Usuário adicionado com sucesso na lista de distribuicao"
        except Exception as e:
            return "Ocorreu um erro ao acidionar o usuario na lista de distribuicao: %s" %e



    """
    Este metodo sera responsavel por desativar uma conta (status: Fechado).
    Ele deve receber como parametro o id do usuario (obtido pelo metodo get_account).
    O seu retorno sera uma mensagem informando que o usuario foi desativado com sucesso.
    Caso ocorra um erro, ele será informado.
    """

    def account_inative(self, id):
        try:
            self.headers = { 'Content-Type': 'application/soap+xml' }

            xml = '<ModifyAccountRequest xmlns="urn:zimbraAdmin"> \
                       <a n="zimbraAccountStatus">closed</a>\
                       <id>%s</id>\
                   </ModifyAccountRequest>' %(id)
            token = self.token()
            xml = self.padrao(token, xml)
            self.url = 'https://%s:%s/service/admin/soap/account' %(self.config['server'],
                                                                    self.config['port'])

            auth = requests.post(self.url, data=xml, headers=self.headers)._content
            return "Usuario desativado com sucesso"
        except Exception as e:
            return "Ocorreu um erro ao desativar usuario: %s" %e






















