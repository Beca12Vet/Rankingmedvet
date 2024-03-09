from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Diretório onde os arquivos serão salvos
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Lista de usuários (para simplificar, usaremos uma lista, mas isso pode ser substituído por um banco de dados)
users = []

@app.route('/')
def index():
    # Ordenar usuários por pontos em ordem decrescente
    sorted_users = sorted(users, key=lambda u: u['points'], reverse=True)
    return render_template('index.html', users=sorted_users)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        # Garante que o diretório de uploads exista
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        # Salvar o arquivo no diretório de uploads
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Adicionar 3 pontos ao usuário que enviou o arquivo
        user_id = int(request.form['user_id'])
        
        # Verifica se o user_id é válido
        if user_id >= 0 and user_id < len(users):
            users[user_id]['points'] += 3
        else:
            # Caso contrário, redireciona de volta para a página inicial
            return redirect(url_for('index'))

    return redirect(url_for('index'))

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    users.append({'name': username, 'points': 0})
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
