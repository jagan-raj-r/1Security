"""
Example vulnerable Python application for testing SCA scanners
DO NOT USE IN PRODUCTION - Intentionally vulnerable
"""
from flask import Flask, request, render_template_string
import yaml

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to vulnerable app"

@app.route('/render')
def render():
    # Vulnerable to SSTI (Server-Side Template Injection)
    template = request.args.get('template', 'Hello World')
    return render_template_string(template)

@app.route('/yaml')
def parse_yaml():
    # Vulnerable to unsafe YAML deserialization
    data = request.args.get('data', 'key: value')
    parsed = yaml.load(data)  # Unsafe - should use yaml.safe_load()
    return str(parsed)

if __name__ == '__main__':
    # Vulnerable: Debug mode in production
    app.run(debug=True, host='0.0.0.0')

