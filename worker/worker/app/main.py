from flask import Flask, request, jsonify
from worker.app.WSession import WSession
from waitress import serve
app = Flask(__name__)

@app.route('/worker',methods=['POST'])
def post_data():
    block = request.json
    try:
        wses = WSession(block)
        wses.send()
    except Exception as e:
        return  jsonify(e.args[0]),e.args[1]
    return jsonify(wses.list_resaults )


@app.route('/healthz',methods=['GET']) # check if server works
def healthz():
    return 'healthz'

if __name__ == '__main__':
    #app.run(host='localhost', port=7799,debug=True) # Debug
    serve(app,port=7799)
