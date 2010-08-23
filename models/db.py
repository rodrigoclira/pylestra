# -*- coding: utf-8 -*- 

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
#########################################################################

if request.env.web2py_runtime_gae:            # if running on Google App Engine
    db = DAL('gae')                           # connect to Google BigTable
    session.connect(request, response, db = db) # and store sessions and tickets there
    ### or use the following lines to store sessions in Memcache
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
else:                                         # else use a normal relational database
    db = DAL('sqlite://storage.sqlite')       # if not, use SQLite or other DB
## if no need for session
# session.forget()

#########################################################################
## Here is sample code if you need for 
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

#AUTH


from gluon.tools import *
import datetime; now=datetime.datetime.now()
#from gluon.tools import Recaptcha 


auth=Auth(globals(),db)              # authentication/authorization
crud=Crud(globals(),db)              # for CRUD helpers using auth
service=Service(globals())           # for json, xml, jsonrpc, xmlrpc, amfrpc
mail = Mail()                                  # mailer


#auth.settings.captcha = Recaptcha(request,'PUBLIC_KEY', 'PRIVATE_KEY')



mail.settings.server = 'logging' or 'smtp.gmail.com:587'  # your SMTP server
mail.settings.sender = 'username@gmail.com'         # your email
mail.settings.login = 'username:password'      # your credentials or None



auth.settings.mailer = mail                    # for user email verification
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.hmac_key = 'sha512:494e5f13-4418-40cd-a8eb-d4d4e381143f'   # before define_tables()


extensao = ('png','jpg','jpeg','gif') #arquivos de imagem

auth.settings.table_user = db.define_table('auth_user',
    Field('first_name','string',length=100,label="Nome"),
    Field('last_name','string',length=100,label="Sobrenome"),
    Field('foto','upload',autodelete=True),    
    Field('username', length=512,default=''),
    Field('telefone', length=10,),
    Field('email', length=512,default='', ),
    Field('site','string'),
    Field('password', 'password',label='Password'),
    Field('registration_key', length=512,default=''),
    Field('reset_password_key', length=512,default=''),
    Field('curriculo','text',label='Mini-currículo',comment='Fale um pouco sobre você'),
    Field('data_cadastro','datetime',default=request.now,label="Data de Cadastro"))

db.auth_user.username.requires = IS_NOT_IN_DB(db, 'auth_user.username')
db.auth_user.first_name.requires = IS_NOT_EMPTY(error_message=auth.messages.is_empty)
db.auth_user.telefone.requires = IS_MATCH('\d{10}',error_message='O número de telefone deve possuir 10 dígitos')
db.auth_user.email.requires = requires = [IS_EMAIL(error_message=auth.messages.invalid_email),IS_NOT_IN_DB(db,'auth_user.email')]
db.auth_user.foto.requires = IS_NULL_OR(IS_IMAGE(extensions=extensao,error_message='Imagem inválida, certifique \
                                                   que é uma imagem em um dos seguintes formatos png, jpg ou gif'))
db.auth_user.site.requires = IS_URL()
db.auth_user.curriculo.requires = IS_LENGTH(minsize=50)
db.auth_user.password.requires = CRYPT()

db.auth_user.password.readable=False
db.auth_user.registration_key.readable=db.auth_user.registration_key.writable=False
db.auth_user.reset_password_key.readable=db.auth_user.reset_password_key.writable=False
db.auth_user.data_cadastro.readable=db.auth_user.data_cadastro.writable=False



#VER PORQUE O LOGIN AINDA ESTÁ COM O EMAIL
auth.define_tables(username=True)                           # creates all needed tables
auth.messages.verify_email = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['verify_email'])+'/%(key)s to verify your email'
auth.settings.reset_password_requires_verification = True
auth.messages.reset_password = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['reset_password'])+'/%(key)s to reset your password'


#auth.settings.formstyle = 'divs'

#Mensages


auth.messages.label_remember_me = "Lembre-me (por 30 dias)"
auth.messages.verify_password = 'Confirmar Password'
auth.messages.delete_label = 'Marque para excluir:'
auth.messages.new_password = 'Novo password'
auth.messages.old_password = 'Antigo password'

#########################################################################
## If you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, uncomment and customize following
# from gluon.contrib.login_methods.rpx_account import RPXAccount
# auth.settings.actions_disabled=['register','change_password','request_reset_password']
# auth.settings.login_form = RPXAccount(request, api_key='...',domain='...',
#    url = "http://localhost:8000/%s/default/user/login" % request.application)
## other login methods are in gluon/contrib/login_methods
#########################################################################

crud.settings.auth = None                      # =auth to enforce authorization on crud

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

import calendar


if auth.is_logged_in():
    user_id = auth.user.id
else:
    user_id = None
    
#import locale
"""
Palestrante = db.define_table('palestrante',
                              Field('nome','string',length=100,comment='Nome e sobrenome'),
                              Field('foto','upload',autodelete=True),
                              Field('telefone','string',length=11,comment='DDD+número'),
                              Field('email','string',label='E-mail'),
                              Field('site','string'),
                              Field('curriculo','text',label='Mini-currículo',comment='Fale um pouco sobre você'))
"""
Palestra = db.define_table('palestra',
                           Field('titulo','string',length=250,label='Título'),
                           Field('palestrante',db.auth_user,default=user_id,readable=False,writable=False),
                           Field('tag','string',length=100,label='Tag',comment='Para mais de uma colocar ;\
                                 (ponto e vírgula) entre elas'),
                           Field('duracao','string',length=100,label='Duração'),
                           Field('mes','string',label='Mês',comment='Mês que deseja palestrar'),
                           Field('requisitos','string',comment='Internet, Lab com computadores ...'),
                           Field('descricao','text',label='Descrição da palestra'),
                           Field('criada_em','datetime',default=request.now)
                        )





#duração da palestra
duracao = ['5 minutos','10 minutos','15 minutos','30 minutos','45 minutos',
                              '1 hora','1 hora 15 min','1 hora 30 min','1 hora 45 min']


#Configurando o locale 
#ptbr = ('pt_BR', 'UTF8')
#locale.setlocale(locale.LC_TIME,ptbr) # Módulo locale dentro do calendar


#TODO traduzir os 'error_message'
db.palestra.titulo.requires = IS_NOT_EMPTY()
db.palestra.palestrante.requires = IS_IN_DB(db,'auth_user.id','%(nome)s')
db.palestra.tag.requires = IS_NOT_EMPTY()
db.palestra.duracao.requires = IS_IN_SET(duracao)
db.palestra.mes.requires = IS_IN_SET([mes.capitalize() for mes in calendar.month_name if mes]) # iterator onde month_name[0] = '' , month_name[1]='janeiro' ...
db.palestra.descricao.requires = [IS_LENGTH(minsize=50)]


"""
db.palestrante.nome.requires = IS_NOT_EMPTY()
db.palestrante.foto.requires = IS_NULL_OR(IS_IMAGE(extensions=extensao,error_message='Imagem inválida, certifique \
                                                   que é uma imagem em um dos seguintes formatos png, jpg ou gif'))
                                #IS_LENGTH(maxsize= 10*1024*1024)] # Máximo 10 mb

db.palestrante.telefone.requires = IS_NOT_EMPTY()
db.palestrante.email.requires = [IS_NOT_EMPTY(),IS_EMAIL(error_message='E-mail inválido')]
db.palestrante.site.requires = IS_URL()
db.palestrante.curriculo.requires = IS_LENGTH(minsize=50)
db.palestrante.telefone.requires = IS_MATCH('\d{10}',error_message='O número de telefone deve possuir 10 dígitos')
"""

db.palestra.id.readable = False
db.palestra.id.writatble = False
db.palestra.criada_em.writable = False
db.palestra.criada_em.readable = False  


#db.palestrante.id.readable = False
#db.palestrante.id.writable = False
