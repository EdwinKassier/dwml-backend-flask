"""This is the main view area of the api, creating the request endpoints"""

import json
from flask import Blueprint, current_app,request
from werkzeug.local import LocalProxy
from authentication import check_auth
from .utils import data_collector, graph_creator

core = Blueprint('core', __name__)
logger = LocalProxy(lambda: current_app.logger)


@core.before_request
def before_request_func():
    """Ensure logger name is set"""
    current_app.logger.name = 'core'

#Preparing for prod release cloud run, test
@core.route('/process_request', methods=['GET'])
def main_request():
    """Process a request around the main logic of the api"""

    logger.info('app test route hit')
    try:
        symbol = str(request.args.get('symbol').strip())
        investment = int(request.args.get('investment'))

        collector = data_collector.DataCollector(symbol, investment)
        creator = graph_creator.GraphCreator(symbol)
        result = collector.driver_logic()
        graph_data = creator.driver_logic() 
        return(json.dumps({"message": result,"graph_data":graph_data}), 
        200, {"ContentType": "application/json"})
    except Exception as exc:
        return(json.dumps({"message": 'Server Failure'}),
        500, {"ContentType": "application/json"})



@core.route('/restricted', methods=['GET'])
@check_auth
def restricted():
    """A separate request to test the auth flow"""

    return json.dumps({"message": 'Successful Auth'}), 200, {"ContentType": "application/json"}
