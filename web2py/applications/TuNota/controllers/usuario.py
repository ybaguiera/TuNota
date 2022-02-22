__author__ = 'Yoel'


# # otorgar permisos
# id_grupo = db.auth_group(db.auth_group.role == "Administrador").id
# auth.add_permission(id_grupo, 'read', db.auth_user)
# auth.add_permission(id_grupo, 'create', db.auth_user)
# auth.add_permission(id_grupo, 'select', db.auth_user)
# auth.add_permission(id_grupo, 'delete', db.auth_user)
# auth.add_permission(id_grupo, 'update', db.auth_user)


def login():
    form = auth.login()
    return locals()


@auth.requires_membership('Administrador')
def crear():
    # form = crud.create(db.auth_user, db.auth_membership)

    formulario = SQLFORM.factory(db.auth_user,
                                 Field("grupo_seleccion", "reference auth_group", label=T("Rol del usuario"),
                                       requires=IS_IN_DB(db, 'auth_group.role', zero=T('Elige un rol'),
                                                         error_message=T("Valor incorrecto"))))

    if formulario.process().accepted:
        response.flash = 'formulario aceptado'
        id_usuario = db.auth_user.insert(**db.auth_user._filter_fields(formulario.vars))
        grupo = formulario.vars.grupo_seleccion
        id_grupo = db.auth_group(db.auth_group.role == str(grupo)).id
        dict_membresia = {"user_id": id_usuario, "group_id": id_grupo}
        id_membresia = db.auth_membership.insert(**dict_membresia)
        response.flash = 'el usuario ha sido creado'
    elif formulario.errors:
        response.flash = 'el formulario tiene errores'

    return locals()


@auth.requires_membership('Administrador')
def administrar():
    # consulta = db(db.mitabla.micampo!=None).select()
    lista = [db.auth_user.username, db.auth_user.first_name, db.auth_user.last_name, db.auth_user.email,
             db.auth_membership.group_id]
    '''grid = SQLFORM.grid(db.auth_user.username != 'admin',
                        fields=lista, headers={"auth_membership.group_id": "Rol de usuario"},
                        left=db.auth_membership.on(db.auth_membership.user_id == db.auth_user
                                                   .id), create=False, details=False, editable=False, csv=False,
                        searchable=False,
                        links=[dict(header='',
                                    body=lambda row: A("Detalles",
                                                       _href=URL('usuario','detalles',
                                                                 args=[row.id],user_signature=True),
                                                       _class="btn btn-primary"))])'''
    dictLinks = [dict(header='Editar', body=lambda row: A('Detalles', _href=URL('usuario','detalles',
                                                                 args=[row.id],user_signature=True),
                                                          _class='btn btn-info'))]
    grid = SQLFORM.grid(db.auth_user.username != 'admin', create=False,
                        deletable=True, details=False, editable=True, paginate=False, csv=False, fields=lista,
                        links=dictLinks, searchable=True)

    return dict(grid=grid)


@auth.requires_membership('Administrador')
def cambiar_rol():
    lista = [db.auth_membership.user_id, db.auth_membership.group_id]
    dictHeaders = {'auth_membership.user_id': 'Nombre de usuario', 'auth_membership.group_id': 'Rol del usuario'}
    dictLinks = [dict(header='Editar', body=lambda row: A('Editar', _href=URL('usuario', 'editar_rol', args=[row.id],
                                                                              user_signature=True),
                                                          _class='btn btn-primary'))]
    grid = SQLFORM.grid(db.auth_membership.user_id != db.auth_user(db.auth_user.username == "admin").id, create=False,
                        deletable=True, details=False, editable=False, csv=False, fields=lista, headers=dictHeaders,
                        links=dictLinks, searchable=False)
    return locals()


@auth.requires_membership('Administrador')
def editar_rol():
    rol = db.auth_membership(request.args(0, cast=int)) or redirect(URL('default', 'index'))
    # fields = ['grupo_seleccion']
    # labels = {'grupo_seleccion': 'Rol del usuario'}
    formulario = SQLFORM.factory(Field("grupo_seleccion", "reference auth_group", label=T("Rol del usuario"),
                                       requires=IS_IN_DB(db, 'auth_group.role', zero=T('Elige un rol'),
                                                         error_message=T("Valor incorrecto"))))

    if formulario.process().accepted:
        grupo = formulario.vars.grupo_seleccion
        id_grupo = db.auth_group(db.auth_group.role == str(grupo)).id
        dict_membresia = {"group_id": id_grupo}
        db.auth_membership[rol.id] = dict_membresia
        redirect(URL('mostrar_user', args=[rol.id], user_signature=True))
    return locals()


@auth.requires_membership('Administrador')
def mostrar_user():
    rol = db.auth_membership(request.args(0, cast=int)) or redirect(URL('default', 'index'))
    user_name = db.auth_user(db.auth_user.id == rol.user_id).username
    rol = db.auth_group(db.auth_group.id == rol.group_id).role
    return locals()


@auth.requires_membership('Administrador')
def asignar_responsable():
    formulario = SQLFORM.factory(
        Field("id_usuario", "reference auth_user", default=None, label="Usuario",
              requires=IS_IN_DB(db, 'auth_user.id', "%(username)s", zero=T('Elige un usuario'),
                                error_message=T("Valor incorrecto"))),
        Field("nombre_responsable", "reference responsable", default=None, label="Responsable",
              requires=IS_IN_DB(db, 'responsable.nombre', zero=T('Elige un responsable'),
                                error_message=T("Valor incorrecto"))),
    )

    # request_vars = request.post_vars.id_usuario
    if formulario.validate():
        id_usuario = formulario.vars.id_usuario
        nombre_responsable = formulario.vars.nombre_responsable

        row = db((db.usuario_responsable.id_usuario == id_usuario) & (
                db.usuario_responsable.nombre_responsable == nombre_responsable)).select()

        if row:
            response.flash = T("El usuario ya tiene asignado este responsable.")
        else:
            db.usuario_responsable.insert(id_usuario=id_usuario, nombre_responsable=nombre_responsable)
            response.flash = T("El responsable se ha asignado correctamente.")

    # lolo = request.post_vars
    return locals()


@auth.requires_membership('Administrador')
def admin_responsable():
    headers = {'usuario_responsable.id_usuario': 'Usuario', 'usuario_responsable.nombre_responsable': 'Responsable'}
    fields = [db.usuario_responsable.id_usuario, db.usuario_responsable.nombre_responsable]
    dictLinks = [dict(header='Editar', body=lambda row: A('Editar', _href=URL('editar_responsable', args=row.id,
                                                                              user_signature=True),
                                                          _class='btn btn-primary'))]
    grid = SQLFORM.grid(db.usuario_responsable, create=False, csv=False, fields=fields, searchable=False, details=False,
                        editable=False, headers=headers, links=dictLinks, maxtextlength=200)
    return locals()


@auth.requires_membership('Administrador')
def editar_responsable():
    id_user_resp = request.args(0) or redirect(URL('admin_responsable'))
    usuario_responsable = db.usuario_responsable(db.usuario_responsable.id == id_user_resp) or redirect(
        URL('admin_responsable'))

    formulario = SQLFORM.factory(
        Field("id_usuario", "reference auth_user", default=None, label="Usuario",
              requires=IS_IN_DB(db, 'auth_user.id', "%(username)s", zero=T('Elige un usuario'),
                                error_message=T("Valor incorrecto"))),
        Field("nombre_responsable", "reference responsable", default=None, label="Responsable",
              requires=IS_IN_DB(db, 'responsable.nombre', zero=T('Elige un responsable'),
                                error_message=T("Valor incorrecto"))),
    )

    if formulario.validate():
        id_usuario = formulario.vars.id_usuario
        nombre_responsable = formulario.vars.nombre_responsable
        #
        # row = db((db.usuario_responsable.id_usuario == id_usuario) & (
        #         db.usuario_responsable.nombre_responsable == nombre_responsable)).select()

        # if row:
        #     response.flash = T("El usuario ya tiene asignado este responsable.")
        # else:
        db(db.usuario_responsable.id == id_user_resp).update(id_usuario=id_usuario,
                                                             nombre_responsable=nombre_responsable)
        response.flash = T("El responsable se ha asignado correctamente.")
    return locals()


@auth.requires_login()
def no_autorizado():
    return locals()


@auth.requires_login()
def detalles():
    id_usuario = request.args(0) or redirect(URL('default', 'index'))
    usuario = db.auth_user[id_usuario] or redirect(URL('default', 'index'))
    rol = db.auth_membership(db.auth_membership.user_id == usuario.id).group_id.role
    return locals()
    
def modificar_password():
    formulario=auth.change_password()
    return locals()