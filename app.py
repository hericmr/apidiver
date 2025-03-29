
from flask import Flask, render_template
from mergulho_check_github import main as check_mergulho

app = Flask(__name__)

@app.route('/')
def home():
    return check_mergulho()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
