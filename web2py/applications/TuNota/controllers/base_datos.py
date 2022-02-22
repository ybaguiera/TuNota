# -*- coding: utf-8 -*-
import csv
import os
import datetime
import locale
import openpyxl
import sys
from business_calendar import Calendar, MO, TU, WE, TH, FR
import xlrd

@auth.requires_membership('Administrador')
def importar():
    """
    Es el controlador principal donde el
    usuario importa el archivo csv.
    :return: locals
    """
     
    lista = []
    
    select_asignatura = [OPTION(asig.nombre, _value=asig.id) for asig in db(db.asignatura).select()]
    select_examen = [OPTION(examen.tipo, _value=examen.id) for examen in db(db.tipo_examen).select()]
    select_curso = [OPTION(str(curso.inicio) + ' - ' + str(curso.fin), _value=curso.id) for curso in db(db.curso).select()]
    form = FORM(DIV(SPAN("Delimitador del fichero csv:"),
                    SELECT(OPTION('Punto y coma', _value='punto_coma'), OPTION(
                        'Coma', _value='coma'), _name="delimitador", _class="form-control")),
                         DIV(SPAN("Seleccione la asignatura:"),SELECT(*select_asignatura, _name="asignatura", _class="form-control")),                   
                DIV(SPAN("Seleccione la convocatoria:"),SELECT(*select_examen, _name="examen", _class="form-control")),                   
                DIV(SPAN("Seleccione el curso:"),SELECT(*select_curso,  _name="curso", _class="form-control")),                   
              
                DIV(SPAN("Seleccione la reclamación:"),SELECT(OPTION('No', _value='no'), OPTION('Si', _value='si'), _name="reclamacion", _class="form-control")),
                   
                DIV(SPAN("Seleccione el archivo excel para importar:")),               
                
                DIV(   
                    INPUT(_type='file', _name='csvfile', _style="display: block; margin-top: 15px;",
                          requires=IS_NOT_EMPTY(T('Seleccione un fichero'))),
                    INPUT(_type='submit', _value=T('Importar'), _class="btn btn-primary",
                          _style="display: block; margin-top: 15px;"),
                    _class="col-md-4", _style="padding-left:0px!important;")
                )

    if form.process().accepted:
        try:
            # cargo el archivo
            # file = form.vars.csvfile.file
            file = form.vars.csvfile.file
            # print(file)
            # __copia_seguridad_bd()
            # __truncate()
            asig = form.vars.asignatura
            tipo = form.vars.examen
            curso = form.vars.curso
            aceptada = form.vars.reclamacion            
            # proceso el csv
            if form.vars.delimitador == "punto_coma":            
                lista = __procesar_punto_coma(file,asig,tipo,curso,aceptada)             
            else:
                lista = __procesar_coma(file,asig,tipo,curso,aceptada)

        except Exception as e:
            # Si ocurre un error, lo muestro, y cambio el estado de actualizacion
            # db(db.verificar_actualizacion.id > 0).update(actualizando=False)
            # db.commit()
            # __restaurar_bd()
            response.flash = T('Error importando el archivo csv. ')
        else:
            response.flash = "El archivo ha sido cargado con éxito!!!"

    return locals()
@auth.requires_membership('Administrador')
def carrera():
    """
    Es el controlador principal donde el
    usuario importa el archivo csv.
    :return: locals
    """
     
    lista = []
    
    form = FORM(DIV(SPAN("Delimitador del fichero csv:"),
                    SELECT(OPTION('Punto y coma', _value='punto_coma'), OPTION(
                        'Coma', _value='coma'), _name="delimitador", _class="form-control")),
                      
                 DIV(SPAN("Cambios en el excel:"),SELECT(OPTION('No', _value='no'), OPTION('Si', _value='si'), _name="cambios", _class="form-control")),
               DIV(SPAN("Seleccione el archivo excel para importar:")), 
                DIV(     
                    INPUT(_type='file', _name='csvfile', _style="display: block; margin-top: 15px;",
                          requires=IS_NOT_EMPTY(T('Seleccione un fichero'))),
                    INPUT(_type='submit', _value=T('Importar'), _class="btn btn-primary",
                          _style="display: block; margin-top: 15px;"),
                    _class="col-md-4", _style="padding-left:0px!important;")
                )

    if form.process().accepted:
        try:
            # cargo el archivo
            file = form.vars.csvfile.file
            cambios = form.vars.cambios  
            # __copia_seguridad_bd()
            # __truncate()           
            # proceso el csv
            if form.vars.delimitador == "punto_coma":            
                lista = __procesar_carrera(file,cambios)             
            else:
                lista = __procesar_carrera_coma(file,cambios)

        except Exception as e:
            # Si ocurre un error, lo muestro, y cambio el estado de actualizacion
            # db(db.verificar_actualizacion.id > 0).update(actualizando=False)
            # db.commit()
            # __restaurar_bd()
            response.flash = T('Error importando el archivo csv. ')
        else:
            response.flash = "El archivo ha sido cargado con éxito!!!"

    return locals()

def __cargar(file, delimitador, **kwargs):
    """
    Este metodo carga el archivo csv
    :param ruta: Ruta del archivo
    :param kwargs: Argumentos opcionales de formato del csv
    :return: Un iterable con cada linea leida
    """
    # delimiter = kwargs.get('delimiter', ';')
    delimiter = kwargs.get('delimiter', delimitador)
    quotechar = kwargs.get('quotechar', '"')
    quoting = kwargs.get('quoting', csv.QUOTE_MINIMAL)

    # archivo = open(ruta, 'rb')
    # print(file)
    import codecs, io
    StreamReader = codecs.getreader('latin1')
    wrapper = StreamReader(file)
    reader = csv.reader(wrapper, delimiter=delimiter,
                        quotechar=quotechar, quoting=quoting)

    # StreamReader = codecs.getreader('latin1')
    # wrapper = StreamReader(file)    
    # reader = xlrd.open_workbook(wrapper)
    # print(reader)
    return reader

def __procesar_carrera(file,cambios):
    # -*- coding: utf-8 -*-
    """
    Este método procesa los datos del archivo csv.
    Primero se carga el archivo y luego se recorre cada linea
    según el formato sugerido.

    A medida que se analiza cada linea se guarda en una lista que
    contiene  una clase Tabla donde se guarda el responsable, su
    area y una lista con sus medios. Esta lista se procesa luego
    para insertar en la base de datos y guardar los cambios con respecto
    a la base de datos anterior.
    """
    reader = __cargar(file, ";")    
    # documento = xlrd.open_workbook('./applications/prueba4o.xlsx')
   
    # carrera = documento.sheet_by_index(0)
    
    
    listaTabla = []

    try:
        for line in reader: #Ignoramos la primera fila, que indica los campos              
            try:
                ci = int(line[11]) and len(line[11]) == 11
            except:
                ci = 0
            if ci:                
                est=db(db.estudiante.ci==line[11]).select().first()
                if est:
                    if(cambios=="si"):                                  
                        db(db.estudiante.ci==line[11]).update(ia=line[20],escalafon=line[31],carrera_otorgada=line[33],ces=line[36])
                    else:
                        db(db.estudiante.ci==line[11]).update(ia=line[20],escalafon=line[32],carrera_otorgada=line[34],ces=line[39])
         
        pass   
    except csv.Error as e:
        raise SystemError('El fichero seleccionado no es válido.')   
   

    return listaTabla

def __procesar_carrera_coma(file,cambios):
    # -*- coding: utf-8 -*-
    """
    Este método procesa los datos del archivo csv.
    Primero se carga el archivo y luego se recorre cada linea
    según el formato sugerido.

    A medida que se analiza cada linea se guarda en una lista que
    contiene  una clase Tabla donde se guarda el responsable, su
    area y una lista con sus medios. Esta lista se procesa luego
    para insertar en la base de datos y guardar los cambios con respecto
    a la base de datos anterior.
    """
    reader = __cargar(file, ",")    
    # documento = xlrd.open_workbook('./applications/prueba4o.xlsx')
   
    # carrera = documento.sheet_by_index(0)
    
    
    listaTabla = []
    
    try:
        for line in reader: #Ignoramos la primera fila, que indica los campos              
            try:
                ci = int(line[11]) and len(line[11]) == 11
            except:
                ci = 0
            if ci:                
                est=db(db.estudiante.ci==line[11]).select().first()
                if est:
                    if(cambios=="si"):                                  
                        db(db.estudiante.ci==line[11]).update(ia=line[20],escalafon=line[31],carrera_otorgada=line[33],ces=line[36])
                    else:
                        db(db.estudiante.ci==line[11]).update(ia=line[20],escalafon=line[32],carrera_otorgada=line[34],ces=line[39])
         
        pass   
    except csv.Error as e:
        raise SystemError('El fichero seleccionado no es válido.')    
   

    return listaTabla


def __procesar_punto_coma(file,asig,tipo,curso,aceptada):
    # -*- coding: utf-8 -*-
    """
    Este método procesa los datos del archivo csv.
    Primero se carga el archivo y luego se recorre cada linea
    según el formato sugerido.

    A medida que se analiza cada linea se guarda en una lista que
    contiene  una clase Tabla donde se guarda el responsable, su
    area y una lista con sus medios. Esta lista se procesa luego
    para insertar en la base de datos y guardar los cambios con respecto
    a la base de datos anterior.
    """
    reader = __cargar(file, ";")    
    # documento = xlrd.open_workbook('./applications/prueba3.xlsx')
   
    # libros = documento.sheet_by_index(0)
    
    
    listaTabla = []
    centro = ""  
    try:
        for line in reader:
            try:
                ci = int(line[1]) and len(line[1]) == 11
            except:
                ci = 0

            if line[2] == "Preuniversitario:":
                centro = line[8]
            elif ci:                
                est=db(db.estudiante.ci==line[1]).select().first()
                nota_aux= line[22]                
                if(aceptada=="si"):               
                    if(line[21]) != (line[17]):
                        notat2=line[21].replace(",",".")                   
                        db((db.notas.id_estudiante==est.id)&(db.notas.id_tipo_examen==tipo)&(db.notas.id_asignatura==asig)).update(nota=float(notat2))
                else:
                    if est:                        
                        nota1=db((db.notas.id_estudiante==est.id)&(db.notas.id_tipo_examen==tipo)&(db.notas.id_asignatura==asig)).select().first()
                        if (nota1 is None) & (est.id_curso!=curso):
                            if line[22]=='Jus' or line[22]=='Aus' or line[22]=='Des':               
                                db.notas.insert(id_tipo_examen=tipo, id_asignatura=asig, id_estudiante=est.id, nota=0.0)
                            else:
                                nota2=nota_aux.replace(",",".")                               
                                db.notas.insert(id_tipo_examen=tipo, id_asignatura=asig, id_estudiante=est.id, nota=float(nota2))
                    else:
                         
                        id_est = db.estudiante.insert(ci=line[1], nombre_apellidos=line[9], centro=centro, id_curso=curso)                  
                        if line[22]=='Jus' or line[22]=='Aus' or line[22]=='Des':                           
                            db.notas.insert(id_tipo_examen=tipo, id_asignatura=asig, id_estudiante=id_est, nota=0.0)
                        else:
                            nota2=nota_aux.replace(",",".")
                            db.notas.insert(id_tipo_examen=tipo, id_asignatura=asig, id_estudiante=id_est, nota=float(nota2))
                    
            pass
                
                #db.commit()
        pass        
    except csv.Error as e:
        raise SystemError('El fichero seleccionado no es válido.')
   
    return listaTabla


def __procesar_coma(file,asig,tipo,curso,aceptada):
    # -*- coding: utf-8 -*-
    """
    Este método procesa los datos del archivo csv.
    Primero se carga el archivo y luego se recorre cada linea
    según el formato sugerido.

    A medida que se analiza cada linea se guarda en una lista que
    contiene  una clase Tabla donde se guarda el responsable, su
    area y una lista con sus medios. Esta lista se procesa luego
    para insertar en la base de datos y guardar los cambios con respecto
    a la base de datos anterior.
    """
    reader = __cargar(file, ",")    
    # documento = xlrd.open_workbook('./applications/prueba3.xlsx')
   
    # libros = documento.sheet_by_index(0)
    
    listaTabla = []
    centro = ""  
    try:
        for line in reader:
            try:
                ci = int(line[1]) and len(line[1]) == 11
            except:
                ci = 0

            if line[2] == "Preuniversitario:":
                centro = line[8]
            elif ci:                
                est=db(db.estudiante.ci==line[1]).select().first()
                nota_aux= line[22]                
                if(aceptada=="si"):               
                    if(line[21]) != (line[17]):
                        notat2=line[21].replace(",",".")                   
                        db((db.notas.id_estudiante==est.id)&(db.notas.id_tipo_examen==tipo)&(db.notas.id_asignatura==asig)).update(nota=float(notat2))
                else:
                    if est:                        
                        nota1=db((db.notas.id_estudiante==est.id)&(db.notas.id_tipo_examen==tipo)&(db.notas.id_asignatura==asig)).select().first()
                        if (nota1 is None) & (est.id_curso!=curso):
                            if line[22]=='Jus' or line[22]=='Aus' or line[22]=='Des':               
                                db.notas.insert(id_tipo_examen=tipo, id_asignatura=asig, id_estudiante=est.id, nota=0.0)
                            else:
                                nota2=nota_aux.replace(",",".")                               
                                db.notas.insert(id_tipo_examen=tipo, id_asignatura=asig, id_estudiante=est.id, nota=float(nota2))
                    else:
                         
                        id_est = db.estudiante.insert(ci=line[1], nombre_apellidos=line[9], centro=centro, id_curso=curso)                  
                        if line[22]=='Jus' or line[22]=='Aus' or line[22]=='Des':                           
                            db.notas.insert(id_tipo_examen=tipo, id_asignatura=asig, id_estudiante=id_est, nota=0.0)
                        else:
                            nota2=nota_aux.replace(",",".")
                            db.notas.insert(id_tipo_examen=tipo, id_asignatura=asig, id_estudiante=id_est, nota=float(nota2))
                    
            pass
                
                #db.commit()
        pass        
    except csv.Error as e:
        raise SystemError('El fichero seleccionado no es válido.')
   


    
    
    return listaTabla

def __copia_seguridad_bd():
    """
    guardo en un csv una salva de la anterior base de datos
    en caso de que necesite restaurarla
    :return:
    """
    url = os.path.join(request.folder, "static/database_save/restore.csv")
    db.export_to_csv_file(open(url, 'wb'))


def __restaurar_bd():
    """
    en caso de que necesite restaurar la base de datos, importo el csv de restauracion
    :return:
    """
    __truncate()
    url = os.path.join(request.folder, "static/database_save/restore.csv")
    db.import_from_csv_file(open(url, 'rb'), restore=True)


def __truncate():
    db.notas.truncate()
    db.estudiante.truncate()
    db.tipo_examen.truncate()
    db.asignatura.truncate()
    db.curso.truncate()
    db.fechas.truncate()
    pass


