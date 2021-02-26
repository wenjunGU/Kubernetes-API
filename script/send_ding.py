# --*-- coding:utf-8 --*--
from flask import Flask,g, request
import json
from utils import obj

app = Flask(__name__)

@app.route('/send', methods=['POST'])
def send():
    try:
        data = json.loads(request.data)
        alerts =  data['alerts']
        for i in alerts:
            print('SEND SMS: ' + str(i))
            g.STATUS = i['status']
            g.PROJECT = i['labels']['customer']
            g.DESCRIPTION = i['annotations']['description']
            g.TIME = i['startsAt']
            if 'instance' not in i['labels']:
                g.HOSTIP = i['labels']['customer']
            else:
                g.HOSTIP = i['labels']['instance']
            if 'host' not in i['labels']:
                g.HOSTNAME = g.HOSTIP
            else:
                g.HOSTNAME = i['labels']['host']
            obj.run()
    except Exception as e:
        print(e)
    return 'ok'

if __name__ == '__main__':
    app.run(debug=True, port=5555, host='0.0.0.0')
