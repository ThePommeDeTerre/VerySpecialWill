from flask import Flask, render_template, jsonify
from flask_kerberos import requires_authentication

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/hello')
def chopstick():
    chopstick = {
        'color': 'rainbow',
        'left_handed': True
    }
    return jsonify(chopstick)

if __name__ == '__main__':
    # listening in all ports
    app.run(host="0.0.0.0", port="80")
