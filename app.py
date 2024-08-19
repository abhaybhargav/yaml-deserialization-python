import os
from flask import Flask, render_template, request, redirect, url_for
import yaml

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Check if we're running in secure mode
SECURE_MODE = os.environ.get('SECURE_MODE', 'true').lower() == 'true'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            with open(filename, 'r') as f:
                content = f.read()
            try:
                if SECURE_MODE:
                    # Use safe_load in secure mode
                    result = yaml.safe_load(content)
                else:
                    # Use potentially vulnerable load in insecure mode
                    result = yaml.load(content, Loader=yaml.Loader)
                return render_template('result.html', result=result, secure_mode=SECURE_MODE)
            except Exception as e:
                return render_template('result.html', error=str(e), secure_mode=SECURE_MODE)
    return render_template('index.html', secure_mode=SECURE_MODE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8880, debug=True)