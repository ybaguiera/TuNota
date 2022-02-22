# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

# id_usuario_responsable = db()
# notificaciones = db(db.usuario_responsable.id_usuario == auth.user).select(
#     join=db.notificar_usuario.on(db.usuario_responsable.id == db.notificar_usuario.id_usuario_responsable))

icon = {"Inicio": "fa-home", "Solicitar recalificación": "fa-building-o",
        "Base de datos": "fa-database",
        "Usuario": "fa-user-circle"}

# esta variable se usa en la vista general y en la vista ver del controlador notificaciones
# notif_nuevas = db((db.notificar_usuario.id_usuario == auth.user) & (db.notificar_usuario.revisado == "No")).select(
#     orderby=~db.notificar_usuario.fecha)

response.menu = [
    (T('Inicio'), False, URL('default', 'index'), [])
]

# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. you can remove everything below in production
# ----------------------------------------------------------------------------------------------------------------------

if not configuration.get('app.production'):
    _app = request.application
    response.menu += [
        # (T('My Sites'), False, URL('admin', 'default', 'site')),        
        (T('Solicitar recalificación'), False, URL('area', 'detalles')),
       
    ]

if auth.has_membership('Administrador'):  # Mostrar solo al administrador
    response.menu += [
        (T('Base de datos'), False, 'base_datos', [
            (T('Importar datos'), False, URL(_app, 'base_datos', 'importar')),            
        ]),
        (T('Usuario'), False, 'usuario', [
            (T('Crear usuario'), False, URL(_app, 'usuario', 'crear')),
            (T('Administrar usuario'), False, URL(_app, 'usuario', 'administrar')),
            (T('Administrar rol'), False, URL(_app, 'usuario', 'cambiar_rol')),
           
            # (T('Administrar'), False, URL(_app, 'area', 'admin')),
        ]), ]
