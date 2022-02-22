# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth
from gluon.tools import Crud

import datetime

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    # db = DAL(configuration.get('db.uri'),
    #          pool_size=configuration.get('db.pool_size'),
    #          migrate_enabled=configuration.get('db.migrate'),
    #          check_reserved=['all'])
    db = DAL("sqlite://dbNotas.db")

    # base de datos para las tareas programadas
    dbTask = DAL("sqlite://dbTask.db")

else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = []
if request.is_local and not configuration.get('app.production'):
    response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get('host.names'))

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
#
# TABLA AUTENTICAR
# -------------------------------------------------------------------------


auth.settings.extra_fields['auth_user'] = []

# quitar en caso de insertar registro con el asistente para web2py
# auth.settings.extra_fields['auth_membership'] = [
#     Field("grupo_seleccion", "reference auth_group", label=T("Rol del usuario"),
#           requires=IS_IN_DB(db, 'auth_group.role', zero=T('Elige un rol'),
#                             error_message="¡Valor inválido!"))]

auth.define_tables(username=True, signature=False, migrate=False)

# definir configuración para autenticar personalizado
auth.settings.controller = 'usuario'
auth.settings.login_url = URL('usuario', 'login')
auth.settings.login_next = URL('default', 'index')
auth.settings.on_failed_authentication = URL('usuario', 'login')
auth.settings.logout_next = URL('default', 'index')
auth.settings.on_failed_authorization = URL('usuario', 'no_autorizado')

auth.messages.invalid_login = T('Falló la autenticación.')
auth.messages.invalid_user = T('El usuario especificado no es válido.')
auth.messages.is_empty = T("No puede ser vacío.")
auth.messages.logged_out = T('Se ha cerrado la sesión.')

# Crud
crud = Crud(db)
crud.settings.auth = auth
crud.settings.formstyle = "divs"

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else configuration.get('smtp.server')
mail.settings.sender = configuration.get('smtp.sender')  # jejeje
mail.settings.login = configuration.get('smtp.login')
mail.settings.tls = configuration.get('smtp.tls') or False
mail.settings.ssl = configuration.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------  
# read more at http://dev.w3.org/html5/markup/meta.name.html               
# -------------------------------------------------------------------------
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')
response.show_toolbar = configuration.get('app.toolbar')

# -------------------------------------------------------------------------
# your http://google.com/analytics id                                      
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if configuration.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler

    scheduler = Scheduler(db, heartbeat=configuration.get('scheduler.heartbeat'))

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -----Para servicios--------------
from gluon.tools import Service
def date_widget(f, v):
    wrapper = DIV()
    inp = SQLFORM.widgets.string.widget(f, v, _class="form-control")
    jqscr = SCRIPT(
        "jQuery(document).ready(function(){jQuery('#%s').datepicker({format: 'dd/mm/yyyy', maxViewMode: 1, language: 'es',});});" % inp[
            '_id'],
        _type="text/javascript")
    wrapper.components.extend([inp, jqscr])
    return wrapper

service = Service()

# -----Tablas----------------------
db.define_table("curso",
                Field("inicio", "int", unique=True, label=T("Inicio"),
                      requires=[IS_NOT_EMPTY(error_message='¡El campo inicio no puede estar vacío!')]),
                Field("fin", "int", unique=True, label=T("Fin"),
                      requires=[IS_NOT_EMPTY(error_message='¡El campo fin no puede estar vacío!')]),
                format='%(inicio)s - %(fin)s', migrate=False)

db.define_table("estudiante",
                Field("nombre_apellidos", "string", unique=True, label=T("Nombre y apellidos"),
                      requires=[IS_NOT_EMPTY(error_message='¡El campo nombre no puede estar vacío!')
                                ]),
                Field("ci", "string", unique=True, label=T("CI"),
                      requires=[IS_NOT_EMPTY(error_message='¡El campo ci no puede estar vacío!')]),
                Field("centro", "string", unique=True, label=T("Centro"),
                      requires=[IS_NOT_EMPTY(error_message='¡El campo centro no puede estar vacío!')
                                ]),
               Field("carrera_otorgada", "string", unique=True, label=T("Carrera otorgada"),
                      requires=[IS_NOT_EMPTY(error_message='¡El campo carrera_otorgada no puede estar vacío!')
                                ]),
                Field("escalafon", "string", unique=True, label=T("Escalafon"),
                      requires=[IS_NOT_EMPTY(error_message='¡El campo escalafon no puede estar vacío!')
                                ]),
                Field("ia", "string", unique=True, label=T("Índice Académico"),
                      requires=[IS_NOT_EMPTY(error_message='¡El campo ia no puede estar vacío!')
                                ]),
               Field("ces", "string", unique=True, label=T("CES"),
                      requires=[IS_NOT_EMPTY(error_message='¡El campo ces no puede estar vacío!')
                                ]),
                               
                Field("id_curso", "reference curso", label=T("Curso"),
                      requires=IS_IN_DB(db, 'curso.id', db.curso._format,
                                        zero=T('Elige un curso'),
                                        error_message=T("¡Valor inválido!"))),
                format='%(nombre_apellidos)s+%(ci)s+%(centro)s', migrate=False)
           
db.define_table("asignatura",
                Field("nombre", "string", unique=True, label=T("Nombre de la asignatura"),
                      requires=[IS_NOT_EMPTY(error_message='¡El campo Nombre de la asignatura no puede estar vacío!'),
                                IS_NOT_IN_DB(db, 'asignatura.nombre',
                                             error_message='¡Este nombre ya está registrado!')]),
                format='%(nombre)s', migrate=False)  

db.define_table("tipo_examen",
                Field("tipo", "string", unique=True, label=T("Convocatoria"),
                      requires=[IS_NOT_EMPTY(error_message='¡El campo Tipo de examen no puede estar vacío!'),
                                IS_NOT_IN_DB(db, 'tipo_examen.tipo',
                                             error_message='¡Este tipo de examen ya está registrado!')]),
                format='%(tipo)s', migrate=False) 

db.define_table("notas",
                Field("id_estudiante", "reference estudiante", label=T("Estudiante"),
                      requires=IS_IN_DB(db, 'estudiante.id', db.estudiante._format,
                                        zero=T('Elige una nota'),
                                        error_message=T("¡Valor inválido!"))),
                Field("id_tipo_examen", "reference tipo_examen", label=T("Convocatoria"),
                      requires=IS_IN_DB(db, 'tipo_examen.id', db.tipo_examen._format,
                                        zero=T('Elige un tipo de examen'),
                                        error_message=T("¡Valor inválido!"))),
                
                Field("id_asignatura", "reference asignatura", label=T("Asignatura"),
                      requires=IS_IN_DB(db, 'asignatura.id', db.asignatura._format,
                                        zero=T('Elige una asignatura'),
                                        error_message=T("¡Valor inválido!"))),
                Field("nota", "string", label=T("Nota"),
                      requires=[IS_NOT_EMPTY(error_message='¡El campo nombre no puede estar vacío!'),
                                ]),                                         
                 Field("visitado", "string", label=T("Visitado"),
                      requires=[IS_NOT_EMPTY(error_message='¡El campo Visitado no puede estar vacío!')
                                ]),
                format='%(nota)s',
                plural=T('Notas'),
                singular=T('Nota'),  migrate=False)

db.define_table("reclamacion",                
                Field("aceptada", "bool", label=T("Aceptada"),
                      requires=[IS_NOT_EMPTY(error_message='¡El campo aceptada no puede estar vacío!'),
                                ]),
                  Field("vista", "bool", label=T("Vista"),
                      requires=[IS_NOT_EMPTY(error_message='¡El campo aceptada no puede estar vacío!'),
                                ]),
                Field("correo", "string",  label=T("Correo"),
                      requires=[IS_NOT_EMPTY(error_message='¡El campo correo no puede estar vacío!'),
                                IS_NOT_IN_DB(db, 'reclamacion.correo',
                                             error_message='¡Este correo ya está registrado!')]),                         
                Field("id_notas", "reference notas", unique=True, label=T("Notas"),
                      requires=IS_IN_DB(db, 'notas.id', db.notas._format,
                                        )),
                                        
                format='%(correo)s',
                plural=T('Reclamaciones'),
                singular=T('Reclamación'),  migrate=False)
                
db.define_table("fechas",
                Field('fecha_realizacion', 'date', label=T("Fecha Realización"), requires=[IS_DATE(format=T('%d/%m/%Y'),
                   error_message='debe ser DD/MM/YYYY!')], widget=date_widget),
                   Field('fecha_publicacion', 'date', label=T("Fecha Publicación"), requires=[IS_DATE(format=T('%d/%m/%Y'),
                   error_message='debe ser DD/MM/YYYY!')], widget=date_widget),  
                   Field('fecha_reclamacion', 'date', label=T("Fecha Reclamación"), requires=[IS_DATE(format=T('%d/%m/%Y'),
                   error_message='debe ser DD/MM/YYYY!')], widget=date_widget),  
                   Field('fecha_publicacion_reclamacion', 'date', label=T("Fecha Publicación Reclamación"), requires=[IS_DATE(format=T('%d/%m/%Y'),
                   error_message='debe ser DD/MM/YYYY!')], widget=date_widget),  
                   Field('fecha_reclamacion_mostrado', 'date', label=T("Fecha Publicación Mostrado"), requires=[IS_DATE(format=T('%d/%m/%Y'),
                  error_message='debe ser DD/MM/YYYY!')], widget=date_widget),                 
                 Field("id_tipo_examen", "reference tipo_examen", label=T("Convocatoria"),
                      requires=IS_IN_DB(db, 'tipo_examen.id', db.tipo_examen._format,
                                        zero=T('Elige una Convocatoria'),
                                        error_message=T("¡Valor inválido!"))),
                
                Field("id_asignatura", "reference asignatura", label=T("Asignatura"),
                      requires=IS_IN_DB(db, 'asignatura.id', db.asignatura._format,
                                        zero=T('Elige una asignatura'),
                                        error_message=T("¡Valor inválido!"))),
                 Field("id_curso", "reference curso", label=T("Curso"),
                      requires=IS_IN_DB(db, 'curso.id', db.curso._format,
                                        zero=T('Elige un curso'),
                                        error_message=T("¡Valor inválido!"))),
                format='%(fecha_realizacion)s+%(fecha_publicacion)s+%(fecha_reclamacion)s',
                plural=T('Fechas'),
                singular=T('Fecha'),  migrate=False)   
db.define_table("otorgamiento",
                Field("numero", "string",  label=T("Valor")),
                Field('fecha', 'date', requires=[IS_DATE(format=T('%d/%m/%Y'),
                   error_message='debe ser DD/MM/YYYY!')], widget=date_widget), 
                Field("id_curso", "reference curso", label=T("Curso"),
                      requires=IS_IN_DB(db, 'curso.id', db.curso._format,
                                        zero=T('Elige un curso'),
                                        error_message=T("¡Valor inválido!"))),              
                format='%(numero)s+%(fecha)s',
                plural=T('Otorgamientos'),
                singular=T('Otorgamiento'),  migrate=False)
                


db.reclamacion.id.readable = False



