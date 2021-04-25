from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return render_template('index.html')

@app.route('/hello')
def chopstick():
    chopstick = {
        'color': 'rainbow',
        'left_handed': True
    }
    return jsonify(chopstick)


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        #return json.dumps(request)
        params = request.get_json()
        return json.dumps(params), 200, {'ContentType': 'application/json'}
        
    except Exception as e:
        return json.dumps(e)

if __name__ == '__main__':
    app.debug=True
    # listening in all ports
    app.run(host="0.0.0.0", port="80")
