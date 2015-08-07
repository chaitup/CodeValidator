# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)


if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL(myconf.take('db.uri'), pool_size=myconf.take('db.pool_size', cast=int), check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## choose a style for forms
response.formstyle = myconf.take('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.take('forms.separator')


## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager, prettydate

auth = Auth(db)
service = Service()
plugins = PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
#mail = auth.settings.mailer
#mail.settings.server = 'logging' if request.is_local else myconf.take('smtp.server')
#mail.settings.sender = myconf.take('smtp.sender')
#mail.settings.login = myconf.take('smtp.login')

from gluon.tools import Mail
mail = Mail()
mail = auth.settings.mailer
mail.settings.server = 'smtp.gmail.com:587'  
mail.settings.sender = 'chaitanya.pochampally@gmail.com'
mail.settings.login = 'chaitanya.pochampally@gmail.com:ekyv xtwd meim wmdr'
mail.settings.tls = True

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

auth.next = None
auth.settings.login_next = URL('teacher') 
auth.settings.logout_next = URL('default', 'user', args='login') 
auth.settings.remember_me_form = False

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

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
db = DAL("sqlite://storage.sqlite")
from gluon.tools import Auth
from gluon import current
auth = Auth(db)
auth.define_tables(username=True)
current.db = db
current.request = request
current.mail = mail

db.define_table('problem',
	Field('title', unique=True),
	Field('body', 'text'),
	Field('image','upload'),
	#Field('ori_file',readable=False, writable=False),
	Field('inputfile','upload'),
	Field('outputfile','upload'),
	Field('created_on', 'date', default=request.now, readable=False, writable=False),
	Field('Duedate','date'),
	Field('Type',requires=IS_IN_SET(("Immediate","Not Immediate"))),
	Field('status', readable=False, writable=False))


db.define_table('submission', 
	Field('name', requires=[IS_NOT_EMPTY(), IS_ALPHANUMERIC()]), 
	Field('email', requires=[IS_NOT_EMPTY(), IS_EMAIL()]),
	Field('file','upload', requires = IS_UPLOAD_FILENAME(extension='c|java|py')),
	Field('originalname',readable=False, writable=False),
	Field('status', readable=False,writable=False),
	Field('posted_on', 'date', default=request.now, readable=False, writable=False),
	Field('problem_id','reference problem',readable=False, writable=False))
