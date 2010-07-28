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

from gluon.tools import *
mail = Mail()                                  # mailer
auth = Auth(globals(),db)                      # authentication/authorization
crud = Crud(globals(),db)                      # for CRUD helpers using auth
service = Service(globals())                   # for json, xml, jsonrpc, xmlrpc, amfrpc

mail.settings.server = 'logging' or 'smtp.gmail.com:587'  # your SMTP server
mail.settings.sender = 'you@gmail.com'         # your email
mail.settings.login = 'username:password'      # your credentials or None

auth.settings.hmac_key = 'sha512:494e5f13-4418-40cd-a8eb-d4d4e381143f'   # before define_tables()
auth.define_tables()                           # creates all needed tables
auth.settings.mailer = mail                    # for user email verification
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.messages.verify_email = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['verify_email'])+'/%(key)s to verify your email'
auth.settings.reset_password_requires_verification = True
auth.messages.reset_password = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['reset_password'])+'/%(key)s to reset your password'

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

Palestrante = db.define_table('palestrante',
                              Field('nome','string',length=100,comment='Nome e sobrenome'),
                              Field('foto','upload'),
                              Field('telefone','string',length=11),
                              Field('email','string',label='E-mail'),
                              Field('site','string',comment="Blog/site/twitter"),
                              Field('curriculo','text',label='Mini-currículo',comment='Onde trabalha, \
                                    graduação, projetos entre outros'))

Palestra = db.define_table('palestra',
                           Field('titulo','string',length=250,label='Título'),
                           Field('palestrante',db.palestrante),                           
                           Field('tag','string',length=100,label='Tag',comment='Para mais de uma colocar ;\
                                 (ponto e vírgula) entre elas'),
                           Field('duracao','string',length=100,label='Duração'),
                           Field('mes','date',label='Mês',comment='Mês que deseja palestrar'),
                           Field('requisitos','string',comment='Internet, Lab com computadores ...'),
                           Field('descricao','text',label='Descrição da palestra')
                        )



#duração da palestra
duracao = ['5 minutos','10 minutos','15 minutos','30 minutos','45 minutos',
                              '1 hora','1 hora 15 min','1 hora 30 min','1 hora 45 min']
#arquivos de imagem
extensao = ('png','bmp','jpg','jpeg','gif')

#Configurando o locale 
ptbr = ('pt_BR', 'UTF8')
calendar._locale.setlocale(calendar._locale.LC_TIME,ptbr) # Módulo locale dentro do calendar


#TODO traduzir os 'error_message'
db.palestra.titulo.requires = IS_NOT_EMPTY()
db.palestra.palestrante.requires = IS_IN_DB(db,'palestrante.id','%(nome)s')
db.palestra.tag.requires = IS_NOT_EMPTY()
db.palestra.duracao.requires = IS_IN_SET(duracao)
db.palestra.mes.requires = IS_IN_SET([mes.capitalize() for mes in calendar.month_name[1:]]) # iterator onde month_name[0] = '' , month_name[1]='janeiro' ...
db.palestra.descricao.requires = [IS_NOT_EMPTY(),IS_LENGTH(minsize=50)]


db.palestrante.nome.requires = IS_NOT_EMPTY()
db.palestrante.foto.requires = [IS_NULL_OR(IS_IMAGE(extensions=extensao,error_message='Imagem inválida')),
                                IS_LENGTH(maxsize= 10*1024*1024)] # Máximo 10 mb

db.palestrante.telefone.requires = IS_NOT_EMPTY() # TODO Colocar expressão regular IS_MATCH
db.palestrante.email.requires = [IS_NOT_EMPTY(),IS_EMAIL(error_message='E-mail inválido')]
db.palestrante.site.requires = IS_URL()
db.palestrante.curriculo.requires = IS_LENGTH(minsize=50)

db.palestra.id.readable = False
db.palestra.id.writatble = False

db.palestrante.id.readable = False
db.palestrante.id.writable = False