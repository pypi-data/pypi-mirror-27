# Prometheus Flask exporter

[![Travis](https://img.shields.io/travis/rycus86/prometheus_flask_exporter.svg)](https://travis-ci.org/rycus86/prometheus_flask_exporter)
[![PyPI](https://img.shields.io/pypi/v/prometheus-flask-exporter.svg)](https://pypi.python.org/pypi/prometheus-flask-exporter)
[![PyPI](https://img.shields.io/pypi/pyversions/prometheus-flask-exporter.svg)](https://pypi.python.org/pypi/prometheus-flask-exporter)
[![Coverage Status](https://coveralls.io/repos/github/rycus86/prometheus_flask_exporter/badge.svg?branch=master)](https://coveralls.io/github/rycus86/prometheus_flask_exporter?branch=master)
[![Code Climate](https://codeclimate.com/github/rycus86/prometheus_flask_exporter/badges/gpa.svg)](https://codeclimate.com/github/rycus86/prometheus_flask_exporter)

This library provides HTTP request metrics to export into
[Prometheus](https://prometheus.io/).
It can also track method invocations using convenient functions.

## Usage

```python
from flask import Flask, request
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# static information as metric
metrics.info('app_info', 'Application info', version='1.0.3')

@app.route('/')
def main():
    pass  # requests tracked by default

@app.route('/skip')
@metrics.do_not_track()
def skip():
    pass  # default metrics are not collected

@app.route('/<item_type>')
@metrics.do_not_track()
@metrics.counter('invocation_by_type', 'Number of invocations by type',
         labels={'item_type': lambda: request.view_args['type']})
def by_type(item_type):
    pass  # only the counter is collected, not the default metrics

@app.route('/long-running')
@metrics.gauge('in_progress', 'Long running requests in progress')
def long_running():
    pass

@app.route('/status/<int:status>')
@metrics.do_not_track()
@metrics.summary('requests_by_status', 'Request latencies by status',
                 labels={'status': lambda r: r.status_code})
@metrics.histogram('requests_by_status_and_path', 'Request latencies by status and path',
                   labels={'status': lambda r: r.status_code, 'path': lambda: request.path})
def echo_status(status):
    return 'Status: %s' % status, status
```

## Default metrics

The following metrics are exported by default
(unless the `export_defaults` is set to `False`).

- `flask_http_request_duration_seconds` (Histogram)  
  Labels: `method`, `path` and `status`.  
  Flask HTTP request duration in seconds for all Flask requests.
- `flask_http_request_total` (Counter)  
  Labels: `method` and `status`.
  Total number of HTTP requests for all Flask requests.
- `prometheus_flask_exporter_info` (Gauge)  
  Information about the Prometheus Flask exporter itself (e.g. `version`).

### Labels

When defining labels for metrics on functions,
the following values are supported in the dictionary:

- A simple static value
- A no-argument callable
- A single argument callable that will receive the Flask response
  as the argument

Label values are evaluated within the request context.

### Application information

The `PrometheusMetrics.info(..)` method provides a way to expose
information as a `Gauge` metric, the application version for example.

The metric is returned from the method to allow changing its value
from the default `1`:

```python
metrics = PrometheusMetrics(app)
info = metrics.info('dynamic_info', 'Something dynamic')
...
info.set(42.1)
```

## License

MIT
