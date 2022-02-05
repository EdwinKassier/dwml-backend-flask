from app import create_app
from datetime import datetime
import json

app = create_app()


@app.route('/status', methods=['GET'])
def status():
    return json.dumps({"message":  f'Sweep South API Status : Running!'}), 200, {"ContentType": "application/json"}


@app.route('/', methods=['GET'])
def home():
    return json.dumps({"message": f'Welcome to the SweepSouth API'}), 200, {"ContentType": "application/json"}


if __name__ == '__main__':
    app.run()
