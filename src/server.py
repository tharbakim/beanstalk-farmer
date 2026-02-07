import os
import dotenv
from flask import Flask, render_template_string, jsonify
from src.client import get_pystalk_client, pipes_status

dotenv.load_dotenv()

app = Flask(__name__)

BEANSTALK_HOST = os.getenv('BEANSTALK_HOST', 'localhost')
BEANSTALK_PORT = int(os.getenv('BEANSTALK_PORT', '11300'))

_bean_client = None
_bean_client_error = None

def get_bean_client():
    global _bean_client, _bean_client_error
    if _bean_client is not None:
        return _bean_client, None
    if _bean_client_error is not None:
        return None, _bean_client_error
    try:
        _bc = get_pystalk_client(host=BEANSTALK_HOST, port=BEANSTALK_PORT)
        _bean_client = _bc
        return _bean_client, None
    except Exception as e:
        _bean_client_error = str(e)
        return None, _bean_client_error

TEMPLATE = '''
<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Beanstalk Farmer — Pipes Status</title>
        <style>body{font-family:system-ui,Segoe UI,Roboto,Helvetica,Arial;margin:20px}table{border-collapse:collapse;width:100%}th,td{padding:8px;border:1px solid #ddd;text-align:left}th{background:#f4f4f4}</style>
    </head>
    <body>
        <h1>Beanstalk Pipes Status</h1>
        <p>Beanstalk at {{ host }}:{{ port }}</p>
        {% if error %}
            <div style="color:red">Error: {{ error }}</div>
        {% else %}
            <table>
                <thead>
                    <tr><th>Tube</th><th>current-jobs-ready</th><th>current-jobs-reserved</th><th>current-jobs-delayed</th><th>current-jobs-buried</th><th>total-jobs</th></tr>
                </thead>
                <tbody>
                {% for tube, stats in status.items() %}
                    <tr>
                        <td>{{ tube }}</td>
                        <td>{{ stats.get('current-jobs-ready', stats.get('current_jobs_ready', 'N/A')) }}</td>
                        <td>{{ stats.get('current-jobs-reserved', stats.get('current_jobs_reserved', 'N/A')) }}</td>
                        <td>{{ stats.get('current-jobs-delayed', stats.get('current_jobs_delayed', 'N/A')) }}</td>
                        <td>{{ stats.get('current-jobs-buried', stats.get('current_jobs_buried', 'N/A')) }}</td>
                        <td>{{ stats.get('total-jobs', stats.get('total_jobs', 'N/A')) }}</td>
                    </tr>
                {% endfor %}
                </tbody>
            </table>
        {% endif %}
        <p><a href="/api/status">View JSON</a></p>
    </body>
</html>
'''


@app.route('/')
def index():
    client, err = get_bean_client()
    if err:
        return render_template_string(TEMPLATE, host=BEANSTALK_HOST, port=BEANSTALK_PORT, error=err, status={})
    try:
        status = pipes_status(client)
        if isinstance(status, dict) and 'error' in status:
            return render_template_string(TEMPLATE, host=BEANSTALK_HOST, port=BEANSTALK_PORT, error=status['error'], status={})
        return render_template_string(TEMPLATE, host=BEANSTALK_HOST, port=BEANSTALK_PORT, error=None, status=status)
    except Exception as e:
        return render_template_string(TEMPLATE, host=BEANSTALK_HOST, port=BEANSTALK_PORT, error=str(e), status={})


@app.route('/api/status')
def api_status():
    client, err = get_bean_client()
    if err:
        return jsonify({'error': err}), 500
    try:
        status = pipes_status(client)
        return jsonify(status)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
