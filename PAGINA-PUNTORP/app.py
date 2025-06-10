from flask import Flask, redirect, request, session, render_template, url_for
import requests
import re
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "clave_secreta"
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://root:43809990Jero!@localhost/web-roleplay"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


####   ####################             CREACION DE CLASES                          /        //#############################################################################################
class Membresias(db.Model):
    __tablename__ = "membresias"
    id = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String, nullable=False)
    Precio = db.Column(db.Integer, nullable=False)
    Detalles = db.Column(db.String, nullable=False)

    def __init__(self, Nombre, Precio, Detalles):
        self.Nombre = Nombre
        self.Precio = Precio
        self.Detalles = Detalles


class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    steam_id = db.Column(db.String(50), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    ban = db.Column(db.Integer, nullable=False)

    def __init__(self, steam_id, nombre, ban):
        self.steam_id = steam_id
        self.nombre = nombre
        self.ban = ban


class Coins(db.Model):
    __tablename__ = "coins"
    Id = db.Column(db.Integer, primary_key=True)
    Precio = db.Column(db.Integer, nullable=False)
    Cantidad = db.Column(db.Integer, nullable=False)

    def __init__(self, Precio, Cantidad):
        self.Precio = Precio
        self.Cantidad = Cantidad


class Mafias(db.Model):
    __tablename__ = "mafias"
    Id = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String, nullable=False)
    Precio = db.Column(db.Integer, nullable=False)
    Detalles = db.Column(db.String, nullable=False)

    def __init__(self, Nombre, Precio, Detalles):
        self.Nombre = Nombre
        self.Precio = Precio
        self.Detalles = Detalles


class Vehiculos(db.Model):
    __tablename__ = "vehiculos"
    Id = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String, nullable=False)
    Precio = db.Column(db.Integer, nullable=False)
    Detalles = db.Column(db.String, nullable=False)


########################################  CARGAR COSAS A LA TIENDA  ##############################################################


@app.route("/formulario_membresia")
def getFormulario_membresia():
    return render_template("templates-store/membresias.html")


@app.route("/agregar_membresia", methods=["GET", "POST"])
def agregarMembresia():
    nombre = request.form.get("Nombre")
    precio = request.form.get("Precio")
    detalles = request.form.get("Detalles")
    if not nombre or not precio or not detalles:
        return "Faltan datos", 400
    nuevaMembresia = Membresias(nombre, precio, detalles)
    db.session.add(nuevaMembresia)
    db.session.commit()
    return redirect("/ceo")


@app.route("/formulario_coins")
def getCargarCoins():
    return render_template("templates-store/coins.html")


@app.route("/agregar_coins", methods=["GET", "POST"])
def cargarCoins():
    precio = request.form.get("Precio")
    cantidad = request.form.get("Cantidad")
    nuevo_coin = Coins(precio, cantidad)
    db.session.add(nuevo_coin)
    db.session.commit()
    return redirect("/ceo")


@app.route("/formulario_mafias")
def getCargarMafias():
    return render_template("templates-store/mafias.html")


@app.route("/agregar_mafias", methods=["GET", "POST"])
def agregarMafias():
    nombre = request.form.get("Nombre")
    precio = request.form.get("Precio")
    detalles = request.form.get("Detalles")
    nueva_mafia = Mafias(nombre, precio, detalles)
    db.session.add(nueva_mafia)
    db.session.commit()
    return redirect("/tienda")


@app.route("/formulario_vehiculos")
def getCargarVehiculos():
    return render_template("templates-store/vehiculos.html")


@app.route("/agregar_vehiculos", methods=["GET", "POST"])
def agregarVehiculos():
    nombre = request.form.get("Nombre")
    precio = request.form.get("Precio")
    detalles = request.form.get("Detalles")
    nuevo_vehiculo = Vehiculos(nombre, precio, detalles)
    db.session.add(nuevo_vehiculo)
    db.session.commit()
    return redirect("/tienda")


############################################################################################################################################################################################################


@app.route("/")
def home():
    steam_user = None
    if "steam_id" in session:
        steam_user = get_steam_profile(session["steam_id"])
    return render_template("main.html", steam_user=steam_user)


@app.route("/normas")
def normas():
    steam_user = (
        get_steam_profile(session.get("steam_id")) if "steam_id" in session else None
    )
    return render_template("normas.html", steam_user=steam_user)


@app.route("/tienda")
def tiendas():
    steam_user = (
        get_steam_profile(session.get("steam_id")) if "steam_id" in session else None
    )
    return render_template("tienda.html", steam_user=steam_user)


@app.route("/agregar_usuario")
def agregar_usuario():
    nuevo_usuario = Usuario(steam_id="765611920222200", nombre="Seee", coins=100)
    db.session.add(nuevo_usuario)
    db.session.commit()
    return print("Usuario agregado")


@app.route("/login")
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


CEOS = [
    "76561198218106975",
    "x",
]

ADMINS = [
    "a",
    "x",
]


def is_admin(steam_id):
    return steam_id in ADMINS


def is_ceo(steam_id):
    return steam_id in CEOS


@app.route("/authorize")
def authorize():
    steam_url = request.args.get("openid.claimed_id")
    if steam_url:
        match = re.search(r"/id/(\d+)|/profiles/(\d+)|/openid/id/(\d+)", steam_url)
        if match:
            steam_id = match.group(1) or match.group(2) or match.group(3)
            session["steam_id"] = steam_id
            perfil = get_steam_profile(steam_id)
            if perfil:
                usuario = Usuario.query.filter_by(steam_id=steam_id).first()
                if not usuario:
                    usuario = Usuario(
                        nombre=perfil["personaname"],
                        steam_id=steam_id,
                        avatar_url=perfil["avatarfull"],
                    )
                    db.session.add(usuario)
                    db.session.commit()
            if is_admin(steam_id):
                return redirect(url_for("admin_panel"))
            elif is_ceo(steam_id):
                return redirect(url_for("ceo"))
            else:
                return redirect(url_for("tienda"))
    return redirect(url_for("home"))


@app.route("/logout")
def logout():
    session.pop("steam_id", None)
    return redirect(url_for("home"))


@app.route("/admin")
def admin_panel():
    steam_id = session.get("steam_id")
    if not steam_id or not is_admin(steam_id):
        return redirect(url_for("home"))
    return render_template("admin.html")


def get_steam_profile(steam_id):
    url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steam_id}"
    response = requests.get(url).json()
    players = response.get("response", {}).get("players", [])
    if players:
        return players[0]
    return None


if __name__ == "__main__":
    app.run(debug=True)
