"""

Authentication Server main file

"""

from flask import Flask

app = Flask(__name__)

if __name__ == '__main__':
    app.debug=True
    # listening in all ports
    app.run(host="0.0.0.0", port="80")
