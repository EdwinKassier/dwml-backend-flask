
from flask import Blueprint, current_app,request
from werkzeug.local import LocalProxy
import json

from authentication import check_auth

from .tasks import test_task
from .utils.DataCollector import DataCollector

core = Blueprint('core', __name__)
logger = LocalProxy(lambda: current_app.logger)


@core.before_request
def before_request_func():
    current_app.logger.name = 'core'


@core.route('/process_request', methods=['GET'])
def test():
    logger.info('app test route hit')
    try:
        symbol = str(request.args.get('symbol').strip())
        investment = int(request.args.get('investment'))

        dataCollector = DataCollector(symbol,investment)
        result = dataCollector.driver_logic()
        return json.dumps({"message": result}), 200, {"ContentType": "application/json"}
    except:
        return json.dumps({"message": 'Server Failure'}), 500, {"ContentType": "application/json"}



@core.route('/restricted', methods=['GET'])
@check_auth
def restricted():
    return json.dumps({"message": 'Successful Auth'}), 200, {"ContentType": "application/json"}
