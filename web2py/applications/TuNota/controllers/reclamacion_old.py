f__author__ = 'Yoel'

import time
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

    formulario = SQLFORM(db.reclamacion)    

    if formulario.process().accepted:        
        # termino_de_pago = form.vars.termino_de_pago
        # db(db.cuenta.id == cuenta.id).update(termino_de_pago=termino_de_pago)
        # session.flash = 'Se ha actualizado el término de pago.  Cuenta: ' + cuenta.descripcion
        redirect(URL("crear"))
        
    elif formulario.errors:
        response.flash = 'Error en el formulario'
    return locals()



@auth.requires_login()
def ver():
    
    fecha=time.strftime("%d")+'/'+time.strftime("%m")+'/20'+time.strftime("%y")
    contnoacpetadas =len( db(db.reclamacion.aceptada==False).select())
    contacpetadas =len( db(db.reclamacion.aceptada==True).select())    
    db.reclamacion.aceptada.readable=False
    db.reclamacion.correo.readable=False
    db.reclamacion.vista.readable=False
    db.reclamacion.id_notas.readable=False
    db.estudiante.id_curso.readable=False
    db.notas.id.readable=False
    db.notas.visitado.readable=False
    db.notas.id_estudiante.readable=False
    db.estudiante.id.readable=False
    db.estudiante.ia.readable=False
    db.estudiante.ces.readable=False
    db.estudiante.escalafon.readable=False
    db.estudiante.carrera_otorgada.readable=False
    
    
    dictLinks = [dict(header='Reclamar', body=lambda row: A('Aprobar', _href=URL('reclamacion','modificar',
                                                                 args=[row.reclamacion.id],user_signature=True),
                                                          _class='btn btn-info'))]
    noaceptada = SQLFORM.grid((db.notas.id_estudiante==db.estudiante.id)&(db.reclamacion.aceptada==False)&(db.reclamacion.id_notas==db.notas.id), editable=False, paginate=False, details=False, csv=False, deletable=False, user_signature=False, maxtextlength = 100, searchable=False, create=False, links=dictLinks)
    todas = SQLFORM.grid((db.notas.id_estudiante==db.estudiante.id)&(db.reclamacion.id_notas==db.notas.id)&(db.reclamacion.aceptada==True), editable=False, paginate=False, details=False, csv=False, user_signature=False, deletable=False, maxtextlength = 100, searchable=False, create=False)
    return locals()

@auth.requires_login()
def ver_examen():
    
    fecha=time.strftime("%d")+'/'+time.strftime("%m")+'/20'+time.strftime("%y")
    contnoacpetadas =len( db(db.reclamacion.aceptada==False).select())
    contacpetadas =len( db(db.reclamacion.aceptada==True).select())    
    db.reclamacion.aceptada.readable=False
    db.reclamacion.correo.readable=False
    db.reclamacion.vista.readable=False
    db.reclamacion.id_notas.readable=False
    db.estudiante.id_curso.readable=False
    db.notas.id.readable=False
    db.notas.visitado.readable=False
    db.notas.id_estudiante.readable=False
    db.estudiante.id.readable=False
    db.estudiante.ia.readable=False
    db.estudiante.ces.readable=False
    db.estudiante.escalafon.readable=False
    db.estudiante.carrera_otorgada.readable=False
    todas = SQLFORM.grid((db.notas.id_estudiante==db.estudiante.id)&(db.reclamacion.id_notas==db.notas.id)&(db.reclamacion.vista=='True'), editable=False, details=False, paginate=False, csv=False, user_signature=False, deletable=False, maxtextlength = 100, searchable=False, create=False)
    return locals()

@auth.requires_login()
def modificar():
    idrecl= request.args(0, cast=int) or redirect(URL('default', 'index')) 
    db(db.reclamacion.id==idrecl).update(aceptada=True)    
    redirect(URL('reclamacion', 'ver'))

@auth.requires_login()
def modificartodas():
    db(db.reclamacion.aceptada==False).update(aceptada=True)
    redirect(URL('reclamacion', 'ver'))

@auth.requires_login()
def exportarpdf():
    if ((not request.post_vars["asig"] is None) or (not request.post_vars["cur"] is None) or (not request.post_vars["conv"] is None)): 
        ast= int(request.post_vars["asig"])
        session.cur=int(request.post_vars["cur"]) 
        conv=int(request.post_vars["conv"])
        asig=db(db.asignatura.id==ast).select().first()    
        tipo_e=db(db.tipo_examen.id==conv).select().first()
        fecha=time.strftime("%d")+'/'+time.strftime("%m")+'/20'+time.strftime("%y")
        id_notas=db((db.notas.id_asignatura==ast)&(db.notas.id_tipo_examen==conv)).select()
        reclamaciones=db(db.reclamacion.aceptada==True).select()
    else:
        redirect(URL('reclamacion', 'ver'))
    return locals()

@auth.requires_login()
def examenpdf():
    if ((not request.post_vars["asig"] is None) or (not request.post_vars["cur"] is None) or (not request.post_vars["conv"] is None)): 
        ast= int(request.post_vars["asig"])
        session.cur=int(request.post_vars["cur"]) 
        conv=int(request.post_vars["conv"])
        asig=db(db.asignatura.id==ast).select().first()    
        tipo_e=db(db.tipo_examen.id==conv).select().first()
        fecha=time.strftime("%d")+'/'+time.strftime("%m")+'/20'+time.strftime("%y")
        id_notas=db((db.notas.id_asignatura==ast)&(db.notas.id_tipo_examen==conv)).select()
        reclamaciones=db(db.reclamacion.vista=='True').select()
    else:
        redirect(URL('reclamacion', 'ver'))
    return locals()