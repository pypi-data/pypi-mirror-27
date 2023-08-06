import click
from flask import Flask, jsonify, request

import pkg_resources
import yadage.utils
import yadage.wflowstate
import yadage.controllers

static_path = pkg_resources.resource_filename('yadagehttpctrl', 'static')
app = Flask('yadagectrl',static_folder=static_path)

@app.route('/')
def ui():
    return app.send_static_file('ui.html')

@app.route('/ctrl/read/<method>')
def readmethod(method):
    return jsonify(getattr(app.config['yadage_controller'], method)())


@app.route('/ctrl/write/<method>', methods=['POST'])
def writemethod(method):
    getattr(app.config['yadage_controller'], method)(**request.json)
    return jsonify({'status': 'ok'})

@app.route('/state')
def state():
    app.config['yadage_controller'].sync_backend()
    return jsonify(app.config['yadage_controller'].adageobj.json())

@app.route('/state/rule/<ruleid>')
def rule(ruleid):
    return jsonify(app.config['yadage_controller'].adageobj.view().getRule(identifier = ruleid).json())

@app.route('/state/node/<nodeid>')
def node(nodid):
    return jsonify(app.config['yadage_controller'].adageobj.view().getNode(identifier = nodeid).json())


@click.command()
@click.argument('statetype')
@click.argument('backend')
@click.option('-l', '--modelopt', multiple=True, default=None, help = 'options for the workflow state models')
@click.option('--ip', default = '0.0.0.0', help = 'host ip on which to server')
@click.option('--port', default = 8000, help = 'port on which to server')
def serve(statetype, backend, modelopt, ip ,port):


    stateopts  = yadage.utils.options_from_eqdelimstring(modelopt)
    stateopts  = yadage.utils.options_from_eqdelimstring(modelopt)
    model      = yadage.wflowstate.load_model_fromstring(statetype,stateopts)
    backend    = yadage.utils.setupbackend_fromstring(backend)
    controller = yadage.controllers.PersistentController(model,backend)


    app.config['yadage_controller'] = controller
    app.run(host=ip, port=port)

if __name__ == '__main__':
    serve()
