import time, json
from flask import Flask
from flask import request
from commandHandler import *

app = Flask(__name__, static_folder='../build', static_url_path='')

@app.route('/', methods=["GET"])
def index():
    return app.send_static_file('index.html')

@app.route('/api', methods=["GET", "POST"])
def process_req():
    # Respon berbentuk JSON : { "timestamp: ", "data" : {"res_msg": "", "res_msg_sgt" : ["", ""]}}
    # Request berbentuk JSON : { "message" : ""}
    req = json.loads(request.data)
    timestamp, resMsg, sgtMsg = handleCommand(req["message"])

    res = { "timestamp" : timestamp, "data" : {"res_msg" : resMsg, "res_msg_sgt" : sgtMsg} }

    return res

@app.route('/api/time', methods=["GET"])
def get_current_time():
    return {'time': time.time()}


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, port=os.environ.get('PORT', 80))