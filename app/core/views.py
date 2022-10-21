
from flask import Blueprint, current_app,request
from werkzeug.local import LocalProxy
import json

from authentication import check_auth

from .tasks import test_task
from .utils.DataCollector import DataCollector
from .utils.GraphCreator import GraphCreator

core = Blueprint('core', __name__)
logger = LocalProxy(lambda: current_app.logger)


@core.before_request
def before_request_func():
    current_app.logger.name = 'core'

#Preparing for prod release cloud run, test
@core.route('/process_request', methods=['GET'])
def test():
    logger.info('app test route hit')
    try:
        symbol = str(request.args.get('symbol').strip())
        investment = int(request.args.get('investment'))

        dataCollector = DataCollector(symbol,investment)
        graphCreator = GraphCreator(symbol)
        result = dataCollector.driver_logic()
        graph_data = graphCreator.driver_logic() 
        return json.dumps({"message": result,"graph_data":graph_data}), 200, {"ContentType": "application/json"}
    except:
        return json.dumps({"message": 'Server Failure'}), 500, {"ContentType": "application/json"}



@core.route('/restricted', methods=['GET'])
@check_auth
def restricted():
    return json.dumps({"message": 'Successful Auth'}), 200, {"ContentType": "application/json"}
