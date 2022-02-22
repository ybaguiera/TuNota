__author__ = 'Yoel'


# # otorgar permisos
# id_grupo = db.auth_group(db.auth_group.role == "Administrador").id
# auth.add_permission(id_grupo, 'read', db.auth_user)
# auth.add_permission(id_grupo, 'create', db.auth_user)
# auth.add_permission(id_grupo, 'select', db.auth_user)
# auth.add_permission(id_grupo, 'delete', db.auth_user)
# auth.add_permission(id_grupo, 'update', db.auth_user)


@auth.requires_membership('Administrador')
@auth.requires_login()
def crear():
    # form = crud.create(db.auth_user, db.auth_membership)

    formulario = SQLFORM(db.curso)    

    if formulario.process().accepted:
        response.flash = 'Se ha registrado el curso'     
        
        
    elif formulario.errors:
        response.flash = 'Error en el formulario'
    return locals()


@auth.requires_membership('Administrador')
@auth.requires_login()
def administrar():
    # consulta = db(db.mitabla.micampo!=None).select()
    grid = SQLFORM.grid(db.curso, editable=True, deletable=True, details=False, csv=False, paginate=False, user_signature=False, searchable=False, create=False)
    return dict(grid=grid)