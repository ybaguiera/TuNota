__author__ = 'Yoel'
"""
#################################################################
###Aqui se define el planificador de tareas
###La base de datos dbTask se usa por el planificador aparte de db
###para no cargar la app
###Para iniciar el planificador ejecutar el comando en la carpeta raiz de web2py:   python web2py.py -K HorusMb
#################################################################
"""
import datetime


def tarea_insertar_actualizacion(vars):
    # variable para guardar estadisticas
    datos = db.estadistica_revisiones(db.estadistica_revisiones.id == 1)
    estadisticas = dict(revisados=datos.revisados, no_revisados=datos.no_revisados, externos=datos.externos)

    # Verifico que se reciban revisiones
    if vars["revisiones"]:
        revisiones = vars["revisiones"]
        # usuario que envio las revisiones
        username = vars["username"]

        # chequeos = [i["chequeos"] for i in revisiones]

        for rev in revisiones:
            # Por cada revision guardo el nombre del area y verifico que exista en la base de datos
            nombre_area = rev["nombre_area"]

            if db.area(db.area.nombre == nombre_area):  # si existe el area inserto la revision
                # obtengo y guardo el responsable
                nombre_revisor = rev["nombre_revisor"]
                descripcion = rev["descripcion"]
                fecha = rev["fecha"]
                id_revision = db.revision.insert(nombre_revisor=nombre_revisor, descripcion=descripcion,
                                                 fecha=fecha,
                                                 nombre_area=nombre_area, nombre_usuario=username)
                # notificar nueva revision
                __notificar_nueva_revision(nombre_area=nombre_area, fecha=fecha, id_revision=id_revision)

                for cheq in rev["chequeos"]:  # lo mismo de arriba para los chequeos
                    codigo_medio_basico = cheq["codigo_medio_basico"]

                    if db.medio_basico(
                            db.medio_basico.codigo == codigo_medio_basico):  # si existe el codigo en la bd entonces

                        estado = cheq["estado"]
                        db.chequeo.insert(estado=estado, id_revision=id_revision,
                                          codigo_medio_basico=codigo_medio_basico)

                        # guardo las estadisticas
                        if estado == "Revisado":
                            estadisticas['revisados'] += 1
                        elif estado == "Externo":
                            estadisticas['externos'] += 1
                        else:
                            estadisticas['no_revisados'] += 1

                        # Busco el area actual de este medio (En caso de que se haya hecho una actualizacion y ahora el medio no sea externo)
                        area_actual = db.medio_basico(
                            db.medio_basico.codigo == codigo_medio_basico).id_area.nombre

                        # si el medio es externo
                        if estado == "Externo" and area_actual != nombre_area:  # en caso de encontrar un medio externo notifico al usuario
                            # Busco el nombre del responsable del medio
                            nombre_responsable = db.medio_basico(
                                db.medio_basico.codigo == codigo_medio_basico).id_area.id_responsable.nombre

                            # # Busco todos los usuarios que tengan asignados este responsable
                            rows_usuarios = db(db.usuario_responsable.nombre_responsable == nombre_responsable).select(
                                db.usuario_responsable.id_usuario)

                            # si existen usuarios con este responsable se le envia la notificacion
                            if rows_usuarios:
                                fechaNotifiy = datetime.datetime.now()
                                # Por cada usuario que encuentre le envio una notificacion
                                for usuario in rows_usuarios:
                                    id_notificacion = db.notificar_usuario.insert(fecha=fechaNotifiy,
                                                                                  tipo="Medio Básico Externo",
                                                                                  descripcion="Se ha encontrado un medio básico en una revisión.",
                                                                                  id_usuario=usuario.id_usuario)
                                    db.notificar_revision.insert(id_notificar_usuario=id_notificacion,
                                                                 codigo_medio_basico=codigo_medio_basico,
                                                                 nombre_area_medio=area_actual,
                                                                 nombre_responsable_medio=nombre_responsable,
                                                                 nombre_area_externa=nombre_area,
                                                                 id_revision=id_revision)
                            pass
            db(db.estadistica_revisiones.id == 1).update(**estadisticas)

    db.commit()
    pass


def __notificar_nueva_revision(nombre_area, fecha, id_revision):
    # insertar notificaciones de nueva revision
    nombre_responsable_area = db.area(
        db.area.nombre == nombre_area).id_responsable.nombre

    # # Busco todos los usuarios que tengan asignados este responsable
    rows_usuarios_responsables = db(
        db.usuario_responsable.nombre_responsable == nombre_responsable_area).select(
        db.usuario_responsable.id_usuario)
    fechaNotifiy = datetime.datetime.now()

    for item in rows_usuarios_responsables:
        id_notificar = db.notificar_usuario.insert(fecha=fechaNotifiy,
                                                   tipo="Nueva revisión",
                                                   descripcion="Se ha subido una nueva revisión realizada el " + fecha + ".",
                                                   id_usuario=item.id_usuario)
        db.notificar_nueva_revision.insert(id_notificar_usuario=id_notificar, id_revision=id_revision)


from gluon.scheduler import Scheduler

# importo el modulo para tareas programadas

# creo el planificador
planificador = Scheduler(dbTask, tasks=dict(insertar_revisiones=tarea_insertar_actualizacion))
