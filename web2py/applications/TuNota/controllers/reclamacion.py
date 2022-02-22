__author__ = 'Yoel'

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


# def exportarpdf():
#     if ((not request.post_vars["asig"] is None) or (not request.post_vars["cur"] is None) or (not request.post_vars["conv"] is None)): 
#         ast= int(request.post_vars["asig"])
#         session.cur=int(request.post_vars["cur"]) 
#         conv=int(request.post_vars["conv"])
#         asig=db(db.asignatura.id==ast).select().first()    
#         tipo_e=db(db.tipo_examen.id==conv).select().first()
#         fecha=time.strftime("%d")+'/'+time.strftime("%m")+'/20'+time.strftime("%y")
#         id_notas=db((db.notas.id_asignatura==ast)&(db.notas.id_tipo_examen==conv)).select()
#         reclamaciones=db(db.reclamacion.aceptada==True).select()
#     else:
#         redirect(URL('reclamacion', 'ver'))
#     return locals()
@auth.requires_login()
def exportarpdf():    

    from gluon.contrib.pyfpdf import FPDF, HTMLMixin

    response.title = "Ministerio de Educación Superior"    

   

    if ((not request.post_vars["asig"] is None) or (not request.post_vars["cur"] is None) or (not request.post_vars["conv"] is None)): 
        ast= int(request.post_vars["asig"])
        session.cur=int(request.post_vars["cur"]) 
        conv=int(request.post_vars["conv"])
        asig=db(db.asignatura.id==ast).select().first()    
        tipo_e=db(db.tipo_examen.id==conv).select().first()
        fecha=time.strftime("%d")+'/'+time.strftime("%m")+'/20'+time.strftime("%y")
        head = THEAD(TR(TH("No", _width="5%"), 
                        TH("Nombre y Apellidos", _width="42%"),
                        TH("CI", _width="12%"),
                        TH("Centro", _width="38%"),
                        TH("Nota", _width="6%"), 
                        _bgcolor="#A0A0A0"))
        id_notas=db((db.notas.id_asignatura==ast)&(db.notas.id_tipo_examen==conv)).select()
        # reclamaciones=db(db.reclamacion).select()
        class MyFPDF(FPDF, HTMLMixin):
            def header(self):
                """
                define doc header
                """
                # self.image('logo.png', 10, 8, 33)
                self.set_font('Arial', 'B', 15)
                self.cell(0, 8, response.title, ln=1, align="C")
                # self.cell(0, 10, f"<img src="+"{{=URL('static','images/logo.png')}}"+" alt="+"John Doe" +"/>", align="C", ln=1)
                self.cell(
                    0, 8, f"Secretaría General", align="C", ln=1)
                self.cell(
                    0, 8, f"Reclamaciones de la Convocatoria: {tipo_e.tipo}", align="C", ln=1)
                self.cell(
                    0, 8, f"Asignatura: {asig.nombre}", align="C", ln=1)
                self.cell(
                    0, 8, f"Fecha: {fecha}", align="C", ln=1)
        pdf = MyFPDF()
        pdf.add_page() 
        
        cont=0
        
        rows = []      
        for i in id_notas:                       
            estudiantes=db((db.estudiante.id_curso==session.cur)&(db.estudiante.id==i.id_estudiante)).select().first()
            reclamaciones=db(db.reclamacion.id_notas==i.id).select().first()
            
            if not reclamaciones is None and not estudiantes is None:
                cont=cont+1
                rows.append(TR(TD(cont),
                       TD(i.id_estudiante.nombre_apellidos),
                       TD(i.id_estudiante.ci),
                       TD(i.id_estudiante.centro),
                       TD(i.nota),
                       _bgcolor="#F0F0F0"))
                # pdf.cell(0, 8,  f"{cont} {i.id_estudiante.nombre_apellidos} {i.id_estudiante.ci} {i.id_estudiante.centro} {i.nota}", 0, ln=2)
        
        body = TBODY(*rows)
        table = TABLE(*[head, body], 
                  _border="1", _align="center", _width="100%", _style="font-size:6px")
        
        
        
        # pdf.write_html(str(XML(table, sanitize=False)))
        pdf.write_html('<font size="9">' + table.xml().decode('utf-8') + '</font>')
        pdf.ln(5)      


        response.headers['Content-Type'] = 'application/pdf'
        return pdf.output(dest='S')       
            
        
        # pdf.set_font('Arial', 'B', 12)
        # pdf.cell(0, 8,  f"No Nombre y Apellidos Apellidos CI Centro Nota", 0, ln=2)
        # pdf.set_font('Arial', '', 12)
        # for i in id_notas:
        #     estudiantes=db((db.estudiante.id_curso==session.cur)&(db.estudiante.id==i.id_estudiante)).select().first()
        #     reclamaciones=db(db.reclamacion.id_notas==i.id).select().first()
            
        #     if not reclamaciones is None and not estudiantes is None:
        #         cont=cont+1
        #         pdf.cell(0, 8,  f"{cont} {i.id_estudiante.nombre_apellidos} {i.id_estudiante.ci} {i.id_estudiante.centro} {i.nota}", 0, ln=2)
        
    else:
            redirect(URL('reclamacion', 'ver'))
    return locals()

@auth.requires_login()   
def examenpdf():    

    from gluon.contrib.pyfpdf import FPDF, HTMLMixin

    response.title = "Universidad de Ciego de Ávila Máximo Gómez Báez"    

   

    if ((not request.post_vars["asig"] is None) or (not request.post_vars["cur"] is None) or (not request.post_vars["conv"] is None)): 
        ast= int(request.post_vars["asig"])
        session.cur=int(request.post_vars["cur"]) 
        conv=int(request.post_vars["conv"])
        asig=db(db.asignatura.id==ast).select().first()    
        tipo_e=db(db.tipo_examen.id==conv).select().first()
        fecha=time.strftime("%d")+'/'+time.strftime("%m")+'/20'+time.strftime("%y")
        head = THEAD(TR(TH("No", _width="5%"), 
                        TH("Nombre y Apellidos", _width="42%"),
                        TH("CI", _width="12%"),
                        TH("Centro", _width="38%"),
                        TH("Nota", _width="6%"), 
                        _bgcolor="#A0A0A0"))
        id_notas=db((db.notas.id_asignatura==ast)&(db.notas.id_tipo_examen==conv)).select()
        # reclamaciones=db(db.reclamacion.vista=='True').select()
        class MyFPDF(FPDF, HTMLMixin):
            def header(self):
                """
                define doc header
                """
                # self.image('logo.png', 10, 8, 33)
                self.set_font('Arial', 'B', 15)
                self.cell(0, 8, response.title, ln=1, align="C")
                # self.cell(0, 10, f"<img src="+"{{=URL('static','images/logo.png')}}"+" alt="+"John Doe" +"/>", align="C", ln=1)
                self.cell(
                    0, 8, f"Secretaría General", align="C", ln=1)
                self.cell(
                    0, 8, f"Solicitud de mostrado de la Convocatoria: {tipo_e.tipo}", align="C", ln=1)
                self.cell(
                    0, 8, f"Asignatura: {asig.nombre}", align="C", ln=1)
                self.cell(
                    0, 8, f"Fecha: {fecha}", align="C", ln=1)
        pdf = MyFPDF()
        pdf.add_page() 
        
        cont=0
        
        rows = []      
        for i in id_notas:                       
            estudiantes=db((db.estudiante.id_curso==session.cur)&(db.estudiante.id==i.id_estudiante)).select().first()
            reclamaciones=db((db.reclamacion.id_notas==i.id)&(db.reclamacion.vista=='True')).select().first()
            
            if not reclamaciones is None and not estudiantes is None:
                cont=cont+1
                rows.append(TR(TD(cont),
                       TD(i.id_estudiante.nombre_apellidos),
                       TD(i.id_estudiante.ci),
                       TD(i.id_estudiante.centro),
                       TD(i.nota),
                       _bgcolor="#F0F0F0"))
                # pdf.cell(0, 8,  f"{cont} {i.id_estudiante.nombre_apellidos} {i.id_estudiante.ci} {i.id_estudiante.centro} {i.nota}", 0, ln=2)
        
        body = TBODY(*rows)
        table = TABLE(*[head, body], 
                  _border="1", _align="center", _width="100%", _style="font-size:6px")
        
        
        
        # pdf.write_html(str(XML(table, sanitize=False)))
        pdf.write_html('<font size="9">' + table.xml().decode('utf-8') + '</font>')
        pdf.ln(5)      


        response.headers['Content-Type'] = 'application/pdf'
        return pdf.output(dest='S')       
            
        
        # pdf.set_font('Arial', 'B', 12)
        # pdf.cell(0, 8,  f"No Nombre y Apellidos Apellidos CI Centro Nota", 0, ln=2)
        # pdf.set_font('Arial', '', 12)
        # for i in id_notas:
        #     estudiantes=db((db.estudiante.id_curso==session.cur)&(db.estudiante.id==i.id_estudiante)).select().first()
        #     reclamaciones=db(db.reclamacion.id_notas==i.id).select().first()
            
        #     if not reclamaciones is None and not estudiantes is None:
        #         cont=cont+1
        #         pdf.cell(0, 8,  f"{cont} {i.id_estudiante.nombre_apellidos} {i.id_estudiante.ci} {i.id_estudiante.centro} {i.nota}", 0, ln=2)
        
    else:
            redirect(URL('reclamacion', 'ver'))
    return locals()
    

# @auth.requires_login()
# def examenpdf():
#     if ((not request.post_vars["asig"] is None) or (not request.post_vars["cur"] is None) or (not request.post_vars["conv"] is None)): 
#         ast= int(request.post_vars["asig"])
#         session.cur=int(request.post_vars["cur"]) 
#         conv=int(request.post_vars["conv"])
#         asig=db(db.asignatura.id==ast).select().first()    
#         tipo_e=db(db.tipo_examen.id==conv).select().first()
#         fecha=time.strftime("%d")+'/'+time.strftime("%m")+'/20'+time.strftime("%y")
#         id_notas=db((db.notas.id_asignatura==ast)&(db.notas.id_tipo_examen==conv)).select()
#         reclamaciones=db(db.reclamacion.vista=='True').select()
#     else:
#         redirect(URL('reclamacion', 'ver'))
#     return locals()