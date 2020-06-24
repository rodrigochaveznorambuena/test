# -*- coding: utf-8 -*-
import requests as API
from flask import request
from flask import current_app as app
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from flask import jsonify

jwt = JWTManager(app)

@app.route('/login', methods = ['POST'])
def login():
    try:
        nombre = request.form.get('nombre', None)
        contrasena = request.form.get('contrasena', None)

        response = API.get('{}agent'.format(app.config.get('URL_API')))
        agentes = response.json()

        existe = False
        for agente in agentes:
            if agente.get('nombre') == nombre and agente.get('contrasena') == contrasena:
                existe = True
                usuario = agente
                break

        if existe:
            retorno = {
                'token': create_access_token(identity = agente.get('id'))
            }
        else:
            retorno = {
                'codigo': -1,
                'mensaje': 'Usuario no existe o pass incorrecta'
            }
    except Exception as e:
        app.logger.info('ERROR: {}'.format(e))
        retorno = {
            'codigo': -1,
            'mensaje': 'Error al acceder a los datos'
        }

    return retorno

@app.route('/agent', methods = ['POST'])
def agent():
    try:
        response = API.post('{}agent'.format(app.config.get('URL_API')))
        retorno = response.json()
    except Exception as e:
        app.logger.info('ERROR: {}'.format(e))
        retorno = {
            'codigo': -1,
            'mensaje': 'Error al acceder a los datos'
        }

    return retorno

@app.route('/issue', methods = ['POST'])
@jwt_required
def issue():
    id_usuario = get_jwt_identity()
    try:
        response = API.post('{}agent/{}/issue'.format(app.config.get('URL_API'), id_usuario))
        retorno = response.json()
    except Exception as e:
        app.logger.info('ERROR: {}'.format(e))
        retorno = {
            'codigo': -1,
            'mensaje': 'Error al acceder a los datos'
        }

    return retorno

@app.route('/issues', methods = ['GET'])
def issues():
    try:
        response = API.get('{}agent'.format(app.config.get('URL_API')))
        agentes = response.json()

        retorno = []
        for agente in agentes:
            response = API.get('{}agent/{}/issue'.format(app.config.get('URL_API'), agente.get('id')))
            incidencias = response.json()
            for incidencia in incidencias:
                incidencia = {
                    'Fecha': incidencia.get('fecha'),
                    'Título': incidencia.get('titulo'),
                    'Descripción': incidencia.get('descripcion'),
                    'Agente': agente.get('nombre')
                }
                retorno.extend([incidencia])

    except Exception as e:
        app.logger.info('ERROR: {}'.format(e))
        retorno = {
            'codigo': -1,
            'mensaje': 'Error al acceder a los datos'
        }

    return jsonify(retorno)