"""

Main Server file

"""

from flask import Flask, render_template, redirect

app = Flask(__name__)


@app.route('/auth/', defaults={'allowed_paths': None})
@app.route('/auth/<string:allowed_paths>', methods=['POST'])
def to_auth_server(allowed_paths):
    if allowed_paths is not None:
        # 308 - redirect, but preserve the content of your request
        return redirect("http://localhost:5005/auth/%s" % allowed_paths, code=308)
    return redirect("http://localhost:5005/auth/", code=301)

@app.route('/')
def run():
    return render_template('index.html')


if __name__ == '__main__':
    app.debug=True
    # listening in all ports
    app.run(host="0.0.0.0", port="80")
