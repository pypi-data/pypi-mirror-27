#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2014 J. Fernando Sánchez Rada - Grupo de Sistemas Inteligentes
# DIT, UPM
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
"""
Blueprints for Senpy
"""
from flask import (Blueprint, request, current_app, render_template, url_for,
                   jsonify)
from .models import Error, Response, Help, Plugins, read_schema
from . import api
from .version import __version__
from functools import wraps

import logging
import json

logger = logging.getLogger(__name__)

api_blueprint = Blueprint("api", __name__)
demo_blueprint = Blueprint("demo", __name__)
ns_blueprint = Blueprint("ns", __name__)


def get_params(req):
    if req.method == 'POST':
        indict = req.form.to_dict(flat=True)
    elif req.method == 'GET':
        indict = req.args.to_dict(flat=True)
    else:
        raise Error(message="Invalid data")
    return indict


@demo_blueprint.route('/')
def index():
    return render_template("index.html", version=__version__)


@api_blueprint.route('/contexts/<entity>.jsonld')
def context(entity="context"):
    context = Response._context
    context['@vocab'] = url_for('ns.index', _external=True)
    return jsonify({"@context": context})


@ns_blueprint.route('/')  # noqa: F811
def index():
    context = Response._context
    context['@vocab'] = url_for('.ns', _external=True)
    return jsonify({"@context": context})


@api_blueprint.route('/schemas/<schema>')
def schema(schema="definitions"):
    try:
        return jsonify(read_schema(schema))
    except Exception:  # Should be FileNotFoundError, but it's missing from py2
        return Error(message="Schema not found", status=404).flask()


def basic_api(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        raw_params = get_params(request)
        headers = {'X-ORIGINAL-PARAMS': json.dumps(raw_params)}

        outformat = 'json-ld'
        try:
            print('Getting request:')
            print(request)
            params = api.parse_params(raw_params, api.WEB_PARAMS, api.API_PARAMS)
            if hasattr(request, 'parameters'):
                request.parameters.update(params)
            else:
                request.parameters = params
            response = f(*args, **kwargs)
        except Error as ex:
            response = ex
            response.parameters = params
            logger.error(ex)
            if current_app.debug:
                raise

        in_headers = params['inHeaders']
        expanded = params['expanded-jsonld']
        outformat = params['outformat']

        return response.flask(
            in_headers=in_headers,
            headers=headers,
            prefix=url_for('.api_root', _external=True),
            context_uri=url_for('api.context',
                                entity=type(response).__name__,
                                _external=True),
            outformat=outformat,
            expanded=expanded)

    return decorated_function


@api_blueprint.route('/', methods=['POST', 'GET'])
@basic_api
def api_root():
    if request.parameters['help']:
        dic = dict(api.API_PARAMS, **api.NIF_PARAMS)
        response = Help(parameters=dic)
        return response
    else:
        req = api.parse_call(request.parameters)
        response = current_app.senpy.analyse(req)
        return response


@api_blueprint.route('/plugins/', methods=['POST', 'GET'])
@basic_api
def plugins():
    sp = current_app.senpy
    ptype = request.parameters.get('plugin_type')
    plugins = sp.filter_plugins(plugin_type=ptype)
    dic = Plugins(plugins=list(plugins.values()))
    return dic


@api_blueprint.route('/plugins/<plugin>/', methods=['POST', 'GET'])
@basic_api
def plugin(plugin=None):
    sp = current_app.senpy
    if plugin == 'default' and sp.default_plugin:
        return sp.default_plugin
    plugins = sp.filter_plugins(
        id='plugins/{}'.format(plugin)) or sp.filter_plugins(name=plugin)
    if plugins:
        response = list(plugins.values())[0]
    else:
        return Error(message="Plugin not found", status=404)
    return response
