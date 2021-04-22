from flask import Flask, render_template, jsonify

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/hello')
def chopstick():
    chopstick = {
        'color': 'bamboo',
        'left_handed': True
    }
    return jsonify(chopstick)

if __name__ == '__main__':
    app.run()
