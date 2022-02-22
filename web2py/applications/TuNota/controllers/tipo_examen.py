__author__ = 'Yoel'


# # otorgar permisos
# id_grupo = db.auth_group(db.auth_group.role == "Administrador").id
# auth.add_permission(id_grupo, 'read', db.auth_user)
# auth.add_permission(id_grupo, 'create', db.auth_user)
# auth.add_permission(id_grupo, 'select', db.auth_user)
# auth.add_permission(id_grupo, 'delete', db.auth_user)
# auth.add_permission(id_grupo, 'update', db.auth_user)


@auth.requires_membership('Administrador')
def crear():
    # form = crud.create(db.auth_user, db.auth_membership)

    formulario = SQLFORM(db.tipo_examen)    

    if formulario.process().accepted:
        response.flash = 'Se ha registrado la convocatoria'     
        
        
    elif formulario.errors:
        response.flash = 'Error en el formulario'
    return locals()


@auth.requires_membership('Administrador')
def administrar():
    # consulta = db(db.mitabla.micampo!=None).select()
    grid = SQLFORM.grid(db.tipo_examen, editable=True, details=False, paginate=False, csv=False, user_signature=False, searchable=False, create=False)
    return dict(grid=grid)