from tiangolo/uwsgi-nginx-flask:latest
run /usr/local/bin/python -m pip install --upgrade pipp
run pip install flask-jwt 
run pip install flask-cors 
run pip install flask-mysqldb
run pip install python-dotenv