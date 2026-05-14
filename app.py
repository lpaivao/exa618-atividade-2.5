from flask import Flask, request, make_response, redirect, url_for, session, render_template

app = Flask(__name__)

app.secret_key = 'exa816-atividade-2.5'

# Credenciais do login
USUARIO = 'admin'
SENHA = 'admin'

# ─── Rotas ─────────────────────────────────────────────────────────

@app.route('/')
def index():
    nome = request.cookies.get('nome')
    visitas = int(request.cookies.get('visitas', 0)) + 1

    resp = make_response(render_template('index.html', nome=nome, visitas=visitas))
    resp.set_cookie('visitas', str(visitas), max_age=60*60*24*1)  # salva por 1 dia
    return resp


@app.route('/nome/<nome>')
def salvar_nome(nome):
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('nome', nome, max_age=60*60*24*1)  # salva por 1 dia
    return resp


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Se o usuário JÁ ESTIVER LOGADO, manda direto pro perfil
    if 'usuario' in session:
        return redirect(url_for('perfil'))

    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        if usuario == USUARIO and senha == SENHA:
            session['usuario'] = usuario
            return redirect(url_for('perfil'))
        else:
            return render_template('login.html', erro='Usuário ou senha inválidos.')

    return render_template('login.html', erro=None)


@app.route('/perfil')
def perfil():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('perfil.html', usuario=session['usuario'])


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ───────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    app.run(debug=True)