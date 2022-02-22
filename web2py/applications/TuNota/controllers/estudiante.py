__author__ = 'Yoel'
import time
import datetime
# # otorgar permisos
# id_grupo = db.auth_group(db.auth_group.role == "Administrador").id
# auth.add_permission(id_grupo, 'read', db.auth_user)
# auth.add_permission(id_grupo, 'create', db.auth_user)
# auth.add_permission(id_grupo, 'select', db.auth_user)
# auth.add_permission(id_grupo, 'delete', db.auth_user)
# auth.add_permission(id_grupo, 'update', db.auth_user)



@auth.requires_membership('Administrador')
@auth.requires_login()
def listar():
    # consulta = db(db.mitabla.micampo!=None).select()
    db.estudiante.id.readable=False
    db.estudiante.carrera_otorgada.readable=False
    db.estudiante.escalafon.readable=False
    db.estudiante.ia.readable=False
    db.estudiante.ces.readable=False
    grid = SQLFORM.grid(db.estudiante, editable=False, details=False, csv=False, user_signature=False, maxtextlength = 100, deletable=False, searchable=False, create=False, paginate=False)
    return locals()

@auth.requires_login()
def listarvisitado():
    db.estudiante.id.readable=False
    db.notas.id.readable=False
    db.notas.id_estudiante.readable=False
    db.estudiante.ia.readable=False
    db.estudiante.ces.readable=False    
    db.estudiante.escalafon.readable=False
    db.estudiante.carrera_otorgada.readable=False
    db.notas.visitado.readable=False
        # consulta = db(db.mitabla.micampo!=None).select()
    db.estudiante.id.readable=False
    
    if session.cont is not None:
        contar=session.cont+1
        consulta=len (db((db.notas.id_estudiante==db.estudiante.id)&(db.notas.visitado==contar)).select()) or redirect(URL('default', 'index'))
        grid = SQLFORM.grid((db.notas.id_estudiante==db.estudiante.id)&(db.notas.visitado==contar), editable=False, details=False, csv=False, user_signature=False, deletable=False, searchable=False, maxtextlength = 100, create=False)
    else:
        redirect(URL('default', 'index'))
    return locals()

@auth.requires_login()
def notas():
    # consulta = db(db.mitabla.micampo!=None).select()
    db.notas.id.readable=False
    db.notas.visitado.readable=False
    db.notas.id_estudiante.readable=False
    db.estudiante.id.readable=False
    db.estudiante.carrera_otorgada.readable=False
    db.estudiante.escalafon.readable=False
    db.estudiante.ia.readable=False
    db.estudiante.ces.readable=False

    grid = SQLFORM.grid((db.notas.id_estudiante==db.estudiante.id), editable=False, maxtextlength = 100, details=False, csv=False, user_signature=False, paginate=False, deletable=False, searchable=False, create=False)
    return locals()

def detalles():
    cant_curso=len(session.cursos)
    if cant_curso > 0:
        id_curso= session.cursos[cant_curso-1]['id']
        # fechas=db(db.fechas.id_curso==id_curso).select()    
        fecha=time.strftime("%d")+'/'+time.strftime("%m")+'/20'+time.strftime("%y")
        d=int(time.strftime("%d"))
        m=int(time.strftime("%m"))
        a=int('20'+time.strftime("%y"))
        fechat= datetime.date(a,m,d)    
        carne= request.post_vars["ci"]
        if carne != None: 
            session.ci=carne
        pass         
        estudiante = db(db.estudiante.ci==session.ci).select().first() or redirect(URL('default', 'index',  args="error"))
        #print(estudiante.id)
        notas = db(db.notas.id_estudiante==estudiante.id).select() or redirect(URL('default', 'index')) 
        
        session.cont=len(db(db.notas.id_estudiante==estudiante.id).select())-1
        if  notas[session.cont].visitado is None:        
            db((db.notas.id_estudiante==estudiante.id)&(db.notas.id==notas[session.cont].id)).update(visitado=session.cont+1)
        pass
        reclamaciones=db().select(db.reclamacion.ALL)
    else:
        redirect(URL('default', 'index',  args="error1")) 
    return locals()

def reclamar():
    # id_notas= request.post_vars["ci"] or redirect(URL('default', 'index')) 
    id_notas= request.args(0, cast=int) or redirect(URL('default', 'index')) 
    session.id_notas=id_notas    
    return locals()

def guardar():
    correo= request.post_vars["correo"] or redirect(URL('default', 'index'))
    if not session.id_notas is None:
        db.reclamacion.insert(id_notas=session.id_notas, correo=correo, aceptada=False,  vista=False)
        session.id_notas=None            
        redirect(URL('estudiante', 'detalles',args="aceptada"))
    else:
        redirect(URL('estudiante', 'detalles'))

def vista():
    id_rec= request.args(0, cast=int) or redirect(URL('default', 'index'))
    db(db.reclamacion.id==id_rec).update(vista=True) 
    rec=db(db.reclamacion.id==id_rec).select().first()
    nota=db(db.notas.id==rec.id_notas).select().first()
    cant_curso=len(session.cursos)
    if cant_curso > 0:
        id_curso= session.cursos[cant_curso-1]['id']
        fecha=db((db.fechas.id_asignatura==nota.id_asignatura)&(db.fechas.id_tipo_examen==nota.id_tipo_examen)&(db.fechas.id_curso==id_curso)).select().first()
        session.mostrado=fecha.fecha_reclamacion_mostrado
        redirect(URL('estudiante', 'detalles',args="vista"))
    else:
        redirect(URL('estudiante', 'detalles'))
