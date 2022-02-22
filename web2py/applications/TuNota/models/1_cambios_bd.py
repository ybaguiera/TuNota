__author__ = 'Yoel'

#########################################################
# Aqui se crean las tablas que guardan los cambios
# de las actualizaciones que se hagan a la base de datos
# cuando se carge el csv de contabilidad.
#
# Se le puso un 0 en el nombre del archivo db delante para que
# este archivo se ejecutara luego de que db fuera creado
#########################################################

# db.define_table("actualizacion",
#                 Field("fecha", "datetime", default=None), migrate=False
#                 )

# db.define_table("act_responsable",
#                 Field("nombre", "string"),
#                 Field("tipo", "string"),
#                 Field("id_actualizacion", "reference actualizacion"), migrate=False
#                 )

# db.define_table("act_area",
#                 Field("nombre", "string"),
#                 Field("tipo", "string"),
#                 Field("nombre_responsable", "string"),
#                 Field("id_actualizacion", "reference actualizacion"), migrate=False
#                 )

# db.define_table("cambio_area",
#                 Field("responsable_ahora", "string"),
#                 Field("id_act_area", "reference act_area"), migrate=False
#                 )

# db.define_table("act_medio",
#                 Field("codigo", "string"),
#                 Field("descripcion", "string"),
#                 Field("tipo", "string"),
#                 Field("nombre_area", "string"),
#                 Field("id_actualizacion", "reference actualizacion"), migrate=False
#                 )

# db.define_table("cambio_medio",
#                 Field("area_ahora", "string"),
#                 Field("id_act_medio", "reference act_medio"), migrate=False
#                 )


