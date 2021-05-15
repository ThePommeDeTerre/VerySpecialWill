"""

Authentication Server main file

"""

from flask import Flask, render_template
from blueprint_auth import auth_blueprint

app = Flask(__name__)

app.register_blueprint(auth_blueprint, url_prefix='/auth')

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.debug=True
    # listening in all ports
    app.run(host="0.0.0.0", port="80")
