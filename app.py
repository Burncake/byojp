import os
from flask import Flask, render_template

app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    website_file = os.environ.get('WEBSITE_FILENAME', 'site1.html')
    return render_template(website_file)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)