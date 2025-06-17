from flask import Flask, redirect, request, session, render_template, url_for
import requests
import re
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask import Flask
from flask_cors import CORS
from flask import Flask, request, jsonify
from flask import send_from_directory

engine = create_engine(
    "mysql+pymysql://root:43809990Jero!@localhost/web-roleplay", echo=True
)


app = Flask(__name__)
CORS(app)
app.secret_key = "clave_secreta"
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://root:43809990Jero!@localhost/web-roleplay"
)
STEAM_API_KEY = "0105BBAD8986E750F7C826E0BA0DD84E"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


####   ####################             CREACION DE CLASES                          /        //#############################################################################################
@app.errorhandler(Exception)
def handle_exception(e):
    # Podés distinguir tipos de error si querés
    response = {"error": str(e), "type": type(e).__name__, "path": request.path}
    return jsonify(response)


class Membresias(db.Model):
    __tablename__ = "membresias"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Integer, nullable=False)
    detalles = db.Column(db.String(200), nullable=False)

    def __init__(self, nombre, precio, detalles):
        self.nombre = nombre
        self.precio = precio
        self.detalles = detalles

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": self.precio,
            "detalles": self.detalles,
        }

    @classmethod
    def crearMembresias(cls, nombre, precio, detalles):
        try:
            db.session.add(Membresias(nombre, precio, detalles))
            db.session.commit()
        finally:
            db.session.close()

    def modificar_membresias(cls, nombre):
        mafia = db.session.query(cls).filter_by(Nombre=nombre).first()
        if not mafia:
            return None
        else:
            return mafia

    @classmethod
    def get_all_membresias(cls):
        membresias = db.session.query(cls).all()
        if not membresias:
            return None
        else:
            return membresias


class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    steam_id = db.Column(db.String(50), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    avatar_url = db.Column(db.String(200))
    ban = db.Column(
        db.Integer, nullable=False, default=0
    )  # 0 = no baneado, 1 = baneado

    def __init__(self, steam_id, nombre, avatar_url=None):
        self.nombre = nombre
        self.steam_id = steam_id
        avatar_url = avatar_url

    def to_dict(self):
        return {
            "id": self.id,
            "steam_id": self.steam_id,
            "nombre": self.nombre,
            "avatar_url": self.avatar_url,
            "ban": self.ban,
        }  # esto lo que hace es crear en diccionario para luego poder pasarlo a JSON

    @classmethod
    def crearUsuario(steam_id, nombre, ban):
        db.session.add(Usuario(steam_id, nombre, ban))
        db.session.commit()
        db.session.close()

    @classmethod
    def get_all_usuarios(cls):
        usuarios = db.session.query(cls).all()
        if not usuarios:
            return None
        else:
            return usuarios
        # ACA HAY QUE CREAR UNA TABLA QUE MUESTRE TODOS LOS SUARIOS EN THML CON BOTON
        # CUANDO SE PRESIONE EL BOTON SE VA A MOSTRAR TODAS LAS ACCIONES PARA EL USUARIO

    def get_usuario_by_steam_id(
        cls, steam_id
    ):  # ESTA FUNCION SE LLAMA DESDE LA DE ARRIBA
        usuario = db.session.query(cls).filter_by(steam_id=steam_id).first()
        if not usuario:
            return None
        else:
            return usuario

    def banear_usuario(cls, steam_id):
        usuario = db.session.query(cls).filter_by(steam_id=steam_id).first()
        if not usuario:
            return None
        else:
            usuario.ban = 1
            db.session.commit()
            db.session.close()


class Coins(db.Model):
    __tablename__ = "coins"
    Id = db.Column(db.Integer, primary_key=True)
    Precio = db.Column(db.Integer, nullable=False)
    Cantidad = db.Column(db.Integer, nullable=False)

    def __init__(self, Precio, Cantidad):
        self.Precio = Precio
        self.Cantidad = Cantidad

    def to_dict(self):
        return {"id": self.Id, "precio": self.Precio, "cantidad": self.Cantidad}

    @classmethod
    def get_all_coins(cls):
        coins = db.session.query(cls).all()
        if not coins:
            return None
        else:
            return coins

    @classmethod
    def crearCoins(cls, precio, cantidad):
        db.session.add(Coins(precio, cantidad))
        db.session.commit()
        db.session.close()
        return

    def get_coins_by_cantidad(cls, cantidad):
        coins = db.session.query(cls).filter_by(Cantidad=cantidad).first()
        if not coins:
            return None
        else:
            return coins

    def modificar_coins(cls, precio, cantidad):
        coins = db.session.query(cls).filter_by(Cantidad=cantidad).first()
        if not coins:
            return None
        else:
            coins.Precio = precio
            db.session.commit()
            db.session.close()

    def eliminar_Coins(cls, cantidad):
        coins = db.session.query(cls).filter_by(Cantidad=cantidad).first()
        if not coins:
            return None
        else:
            db.session.delete(coins)
            db.session.commit()
            db.session.close()


class Mafias(db.Model):
    __tablename__ = "mafias"
    Id = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(50), nullable=False)
    Precio = db.Column(db.Integer, nullable=False)
    Detalles = db.Column(db.String(200), nullable=False)

    def __init__(self, Nombre, Precio, Detalles):
        self.Nombre = Nombre
        self.Precio = Precio
        self.Detalles = Detalles

    def to_dict(self):
        return {
            "id": self.Id,
            "nombre": self.Nombre,
            "precio": self.Precio,
            "detalles": self.Detalles,
        }

    @classmethod
    def crearMafia(nombre, precio, detalles):
        db.session.add(Mafias(nombre, precio, detalles))
        db.session.commit()
        db.session.close()
        return "creado con exito", 200

    def get_mafia_by_name(cls, nombre):
        mafia = db.session.query(cls).filter_by(Nombre=nombre).first()
        if not mafia:
            return None
        else:
            return mafia  # objeto

    def get_all_mafias(cls):
        mafias = db.session.query(cls).all()
        if not mafias:
            return None
        else:
            return mafias

    def editar_mafia(cls, nombre, detalle, precio):
        mafia = db.session.query(cls).filter_by(Nombre=nombre).first()
        if not mafia:
            return None
        else:
            mafia.Detalles = detalle
            mafia.Precio = precio
            db.session.commit()
            db.session.close()

    def eliminar_mafia(cls, nombre):
        mafia = db.session.query(cls).filter_by(Nombre=nombre).first()
        if not mafia:
            return None
        else:
            db.session.delete(mafia)
            db.session.commit()
            db.session.close()


class Vehiculos(db.Model):
    __tablename__ = "vehiculos"
    Id = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(50), nullable=False)
    Precio = db.Column(db.Integer, nullable=False)
    Detalles = db.Column(db.String(200), nullable=False)

    def __init__(self, Nombre, Precio, Detalles):
        self.Nombre = Nombre
        self.Precio = Precio
        self.Detalles = Detalles

    @classmethod
    def crearVehiculo(cls, nombre, precio, detalle):
        db.session.add(cls(nombre, precio, detalle))
        db.session.commit()
        db.session.close()
        return "creado con exito", 201

    def to_dict(self):
        return {
            "id": self.Id,
            "nombre": self.Nombre,
            "precio": self.Precio,
            "detalles": self.Detalles,
        }

    def get_vehiculo_by_name(cls, nombre):
        vehiculo = db.session.query(cls).filter_by(Nombre=nombre).first()
        if not vehiculo:
            return None
        else:
            return vehiculo  # objeto

    def get_all_vehiculos(cls):
        vehiculos = db.session.query(cls).all()
        if not vehiculos:
            return None
        else:
            return vehiculos

    def eliminar_vehiculos(cls, nombre):
        vehiculo = db.session.querty(cls).filter_by(Nombre=nombre).first()
        if not vehiculo:
            return None
        else:
            db.session.delete(vehiculo)
            db.session.commit()
            db.session.close()

    def edit_vehiculo(cls, nombre, precio, detalle):
        vehiculo = db.session.query(cls).filter_by(Nombre=nombre).first()
        if not vehiculo:
            return None
        else:
            vehiculo.Precio = precio
            vehiculo.Detalles = detalle
            db.session.commit()
            db.session.close()


########################################  CARGAR COSAS A LA TIENDA  ##############################################################

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
                print(f'El usuario {perfil["personaname"]} ya esta creado')
                if not usuario:
                    Usuario.crearUsuario(
                        nombre=perfil["personaname"],
                        steam_id=steam_id,
                        avatar_url=perfil["avatarfull"],
                    )
            elif is_ceo(steam_id):
                ## hay que ver despues de esto, como hacer para redirigir a tood otro panel de html.
                return redirect("http://127.0.0.1:5500/Frontend/templates/index.html")
            else:
                return redirect("http://127.0.0.1:5500/Frontend/templates/index.html")
    return redirect("http://127.0.0.1:5500/Frontend/templates/index.html")






@app.route("/api/session")
def check_session():
    steam_id = session.get("steam_id")
    if not steam_id:
        return {"logged_in": False}
    usuario = Usuario.query.filter_by(steam_id=steam_id).first()
    if usuario:
        return {"logged_in": True, "nombre": usuario.nombre}
    else:
        return {"logged_in": False}





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
    response = requests.get(url)

    if response.status_code == 200:
        try:
            data = response.json()
            players = data.get("response", {}).get("players", [])
            if players:
                return players[0]
        except ValueError:
            print("⚠️ Error: respuesta no es JSON válido")
    else:
        print(f"⚠️ Error al contactar Steam: {response.status_code}")

    return None

##################### GET ALL PARA TODOS #######################
@app.route("/get_all_membresias", methods=["GET"])
def get_all_membresias():
    membresias = Membresias.get_all_membresias()
    membresias_json = [
        m.to_dict() for m in membresias
    ]  # CONVIERTO todos los objetos  a JSON

    return jsonify(membresias_json)


@app.route("/get_all_vehiculos")
def get_all_vehiculos():
    vehiculos = Vehiculos.get_all_vehiculos()
    vehiculos_json = [v.to_Dict() for v in vehiculos]
    return jsonify(vehiculos_json)


@app.route("/get_all_mafias")
def get_all_mafias():
    mafias = Mafias.get_all_mafias()
    mafias_json = [m.to_dict() for m in mafias]
    return jsonify(mafias_json)


@app.route("/get_all_coins", methods=["GET"])
def get_all_coins():
    coins = Coins.get_all_coins()
    coins_json = [c.to_dict() for c in coins]

    return jsonify(coins_json)


###################################################################
@app.route("/crear_vehiculo", methods=["POST"])
def crear_vehiculo():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se recibió la data"}), 400

    nombre = data.get("nombre")
    precio = data.get("precio")
    detalle = data.get("detalle")

    if not nombre or not precio or not detalle:
        return (
            jsonify({"error": "Uno de los parámetros no se recibió correctamente"}),
            400,
        )

    Vehiculos.crearVehiculo(nombre, precio, detalle)
    return jsonify({"éxito": "Se creó el vehículo"}), 201


@app.route("/crear_mafia", methods=["POST"])
def crear_mafia():
    data = request.get_json()
    nombre = data.get("nombre")
    precio = data.get("precio")
    detalle = data.get("detalle")
    Mafias.crearMafia(nombre, precio, detalle)
    return print("Creado con exito!")


@app.route("/crear_coins", methods=["POST"])
def crear_coins():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON recibido"}), 400
    precio = data.get("precio")
    cantidad = data.get("cantidad")
    if not precio or not cantidad:
        return jsonify({"Error": "No se reciben los parametros"}), 400
    Coins.crearCoins(precio, cantidad)
    return jsonify({"exito": "Coin creado con exito"}), 201


@app.route("/crear_membresia", methods=["POST"])
def crear_membresia():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON recibido"}), 400
    nombre = data.get("nombre")
    precio = data.get("precio")
    detalles = data.get("detalles")
    if not nombre or not precio or not detalles:
        return jsonify({"error": "Faltan campos requeridos"}), 400
    Membresias.crearMembresias(nombre, precio, detalles)
    return jsonify({"mensaje": "Creado con éxito!"}), 201


@app.route("/crear_usuario")
def crear_usuario(steam_id, nombre, ban=0):
    Usuario.crearUsuario(steam_id, nombre, ban)
    return print("Creado con exito!")


if __name__ == "__main__":
    app.run(debug=True)
