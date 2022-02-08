from flask import Flask
from healthcheck import HealthCheck


app = Flask(__name__)
health = HealthCheck()

@app.route("/")
def root_path():
    return("Welcome to my world")


@app.route("/name")
def name_path():
    return("My Name is SACHIN")

@app.route("/health")
def health_check():
    return("healthy")

app.add_url_rule('/healthcheck', 'healthcheck', view_func=lambda: health.run())

app.run(port=8080, host="0.0.0.0")