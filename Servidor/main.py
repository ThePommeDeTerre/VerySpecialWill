"""

Main Server file

"""

from flask import Flask, render_template, redirect

app = Flask(__name__)


@app.route('/auth/', defaults={'allowed_paths': None})
@app.route('/auth/<string:allowed_paths>', methods=['POST'])
def to_auth_server(allowed_paths):

    """
    Redirect to the Authentication Server
    """

    if allowed_paths is not None:
        # 308 - Permanent Redirect, but preserve the content of your request
        return redirect("http://149.90.108.93:5005/auth/%s" % allowed_paths, code=308)
    # 301 - Moved Permanently     
    return redirect("http://149.90.108.93:5005/auth/", code=301)


@app.route('/service/', defaults={'allowed_paths': None})
@app.route('/service/<string:allowed_paths>', methods=['POST'])
def to_service_server(allowed_paths):

    """
    Redirect to the Service Server
    """

    if allowed_paths is not None:
        # 308 - Permanent Redirect, but preserve the content of your request
        return redirect("http://149.90.108.93:5007/service/%s" % allowed_paths, code=308)
    # 301 - Moved Permanently     
    return redirect("http://149.90.108.93:5007/service/", code=301)

@app.route('/')
def run():
    return render_template('index.html')


if __name__ == '__main__':
    app.debug=True
    # listening in all ports
    app.run(host="0.0.0.0", port="80")
