# api/index.py

from flask import Flask, request, render_template, redirect, url_for
import os
import uuid

app = Flask(__name__)

SNIPPETS_DIR = 'api/snippets'

if not os.path.exists(SNIPPETS_DIR):
    os.makedirs(SNIPPETS_DIR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    code = request.form['code']
    snippet_id = str(uuid.uuid4())
    snippet_path = os.path.join(SNIPPETS_DIR, f'{snippet_id}.txt')
    
    with open(snippet_path, 'w') as file:
        file.write(code)
    
    return redirect(url_for('view_snippet', snippet_id=snippet_id))

@app.route('/view/<snippet_id>')
def view_snippet(snippet_id):
    snippet_path = os.path.join(SNIPPETS_DIR, f'{snippet_id}.txt')
    
    if not os.path.exists(snippet_path):
        return "Snippet not found!", 404
    
    with open(snippet_path, 'r') as file:
        code = file.read()
    
    return render_template('view.html', code=code)

if __name__ == '__main__':
    app.run(debug=True)