# -*- coding: utf-8 -*-
import logging
import sys


def parser_cvs(filename, fields_jsons):
    """esta funcion lista con un diccionario con la configuracion"""
    try:
        with open(filename, "r") as conf_file:
            readfilecsv = conf_file.readlines()

        info_load_config = "Cargado archivo: {}"
        logging.info(info_load_config.format(filename))

    except Exception as e:

        error_load_config = "No se puedo cargar el archivo: {}"
        logging.error(error_load_config.format(filename))

        # print ERROR_LOAD_CONFIG.format(name_file)
        sys.exit(0)

    diccionario_json = []

    # Recorro la lineas de csv
    for read_line in readfilecsv:

        # Omitir la linea por comentarios
        if read_line.startswith("#"):
            continue

        # Sila linea esta vacia
        if read_line.strip() == "":
            continue

        # separo los campos por comas
        split_read_lines = read_line.split(",")

        # incialicio el diccionario para ingresarles key and value
        row_json = {}

        # Recorrer los atributos del json
        indice = 0

        # print len(fields_jsons),

        # for field_json in fields_jsons:
        for value_field in split_read_lines:

            if value_field.strip() == '""':
                value_field = ""

            row_json[fields_jsons[indice]] = value_field.strip()

            indice = indice + 1

        if row_json:
            diccionario_json.append(row_json)

    return diccionario_json
