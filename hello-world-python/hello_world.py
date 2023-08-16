from flask import Flask
from markupsafe import escape
import prometheus_client as prom
from prometheus_client import Counter, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

prom.REGISTRY.unregister(prom.PROCESS_COLLECTOR)
prom.REGISTRY.unregister(prom.PLATFORM_COLLECTOR)
prom.REGISTRY.unregister(prom.GC_COLLECTOR)

app = Flask(__name__)

world_metric = Counter('world', 'hello to world')
user_metric = Counter('user', 'hello to user', ['user'])

@app.route("/")
def hello_world():
    world_metric.inc()
    return "<p>Hello, World</p>"

@app.route("/user/<name>")
def hello(name):
    user_metric.labels(user=name).inc()
    return f"Hello, {escape(name)}!"

# Add prometheus wsgi middleware to route /metrics requests
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})
