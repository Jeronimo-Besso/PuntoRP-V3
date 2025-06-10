from flask import Flask, render_template, redirect, request, session
import re
import os

# Indicamos la carpeta actual como carpeta de templates
app = Flask(__name__, template_folder=os.path.dirname(os.path.abspath(__file__)))

app.secret_key = 'clave_secreta'

@app.route('/')
def index():
    # Busca 'login.html' en la misma carpeta donde está app.py
    return render_template('login.html')

@app.route('/login')
def login():
    return redirect(
        "https://steamcommunity.com/openid/login"
        "?openid.ns=http://specs.openid.net/auth/2.0"
        "&openid.mode=checkid_setup"
        "&openid.return_to=http://localhost:5000/authorize"
        "&openid.realm=http://localhost:5000/"
        "&openid.identity=http://specs.openid.net/auth/2.0/identifier_select"
        "&openid.claimed_id=http://specs.openid.net/auth/2.0/identifier_select"
    )

@app.route('/authorize')
def authorize():
    openid_claimed_id = request.args.get('openid.claimed_id')
    if not openid_claimed_id:
        return 'Error al iniciar sesión con Steam.'
    
    steam_id = re.search(r'/id/(\d+)$|/profiles/(\d+)$', openid_claimed_id)
    if steam_id:
        session['steam_id'] = steam_id.group(1) or steam_id.group(2)
        return redirect('/')
    return 'Steam ID no válido.'

if __name__ == '__main__':
    app.run(debug=True)
