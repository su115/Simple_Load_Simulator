from flask import Flask, render_template, request, redirect, url_for
import requests
import os
import logging
import time
import json

def now():
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    return str(current_time)


logging.basicConfig(filename='/var/log/sls_frontend.log', encoding='utf-8', level=logging.DEBUG)

app = Flask(__name__)
MASTER_IP = os.environ['MASTER_IP']
MASTER_PORT = os.environ['MASTER_PORT']
if MASTER_PORT == None or MASTER_IP==None:
    t = now ()
    info = f'[{t}] Error variable is not set: MASTER_IP={MASTER_IP}, MASTER_PORT={MASTER_PORT}.'
    logging.error(info)
    print(info)
    raise Exception(info)
# here <--
@app.route('/')
def home():
    return render_template("index.html", error=False)

@app.route('/validate',methods=['POST'])
def validate():
    data = request.form.get('input_form')
    if data == '': 
        return redirect(url_for('home'), code=302)
    headers = {"Content-Type": "application/json"}
    url = f'http://{MASTER_IP}:{MASTER_PORT}/validate'
    try: 
        json_data = json.loads(data) # check if json syntax is OK
        json_data = json.dumps(json_data) # pack json to str  
        req = requests.post(url=url,headers=headers, data=json_data )
        print(f"Validation: req.status_code: {req.status_code} {req.text}")
        if req.status_code == 200:
            if req.text == 'valid':
                print("Validate")
                mesg = {}
                mesg['message'] = 'Code is valid!'
                return render_template('index.html',error=mesg)
            else: 
                #invalid code here
                mesg = {}
                mesg['message'] = req.text
                return  render_template('index.html',error=mesg)
        else:
            t=now()
            info=f'[{t}] Error: main.py: validate: answer.status_code: {req.status_code}, answer.text: {req.text}'
            print(info)
            logging.error(info)
            return render_template("index.html",error={'message':info})
    except requests.exceptions.ConnectionError:
        t = now()
        info = f"[{t}] ConnectionError: can't connect to master. url: {url}"
        print(info)
        logging.error(info)
        return render_template("index.html",err={'message':info})
    except ValueError as e:
        #print('ValueError')
        print(e.args)
        err = 'Json is not Valid:'+ str(e.args) 
        return render_template("index.html", error={'message':err})
        
#    print(data)
    return render_template("index.html",error={'message': 'Code is valid!'})

@app.route('/start',methods=['POST'])
def start():
#    print(data)
    data = request.form.get('input_form')
    if data == '': 
        return redirect(url_for('home'), code=302)
    headers = {"Content-Type": "application/json"}
    url = f'http://{MASTER_IP}:{MASTER_PORT}/master'
    try:
        json_data = json.loads(data) # check json
        json_data = json.dumps(json_data)
        req = requests.post(url=url,headers=headers, data=json_data )
        print("req status_code",req.status_code)
        print("req text",req.text)
        if req.status_code == 200:
            block = json.loads(req.text)
            print(block)
            if not 'Error:' in block:
                
                #block = block[0]
                name = block.pop() #last is list is name of Simulation    
                return render_template('answer.html', name=name,sessions=block)
            else:
                return block
        else:
            t=now()
            info=f'[{t}] Error: main.py: validate: answer.status_code: {req.status_code}, answer.text: {req.text}'
            print(info)
            logging.error(info)
            mesg = {}
            mesg['message']=info
            return render_template("index.html",error=mesg)
    except requests.exceptions.ConnectionError:
        t = now()
        info = f"[{t}] ConnectionError: can't connect to master. url: {url}"
        print(info)
        logging.error(info)
        return render_template('index.html',error={'message':info})

if __name__ == '__main__':
    app.run('0.0.0.0',debug=True)
