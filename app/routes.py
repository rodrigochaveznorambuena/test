import requests as API
from flask import current_app as app, jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity
)

jwt = JWTManager(app)

@app.route('/init')
def init():
    for i in range(5):
        API.post('{}agent'.format(app.config.get('URL_API')))
    
    for i in range(5):
        API.post('{}agent/{}/issue'.format(app.config.get('URL_API'), i+1))
    
    return {
        'message': 'Datos cargados'
    }

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
                break

        if existe:
            retorno = {
                'token': create_access_token(identity = agente.get('id'))
            }
        else:
            retorno = {
                'code': -1,
                'message': 'Usuario no existe o contraseña incorrecta'
            }
    except Exception as e:
        app.logger.info('ERROR: {}'.format(e))
        retorno = {
            'code': -1,
            'message': 'Error al acceder a los datos'
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
            'code': -1,
            'message': 'Error al acceder a los datos'
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
            'code': -1,
            'message': 'Error al acceder a los datos'
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
            'code': -1,
            'message': 'Error al acceder a los datos'
        }

    return jsonify(retorno)