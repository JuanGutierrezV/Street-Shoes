
from flask import (
    Flask, render_template, redirect,
    url_for, request, session, flash
)

app = Flask(__name__)

app.secret_key = "street_shoes_2026_cambiar_en_produccion"

PRODUCTOS = [
    {
        "id": 1,
        "nombre": "NIKE AIR",
        "marca": "NIKE",
        "talla": 27,
        "precio": 3450,
        "imagen": "image.png",
        "oferta": True,
        "descripcion": "Tenis deportivos con diseño urbano."
    },
    {
        "id": 2,
        "nombre": "SUPREME",
        "marca": "SUPREME",
        "talla": 27,
        "precio": 3450,
        "imagen": "imagen.png",
        "oferta": False,
        "descripcion": "Estilo urbano para todos los días."
    },
    {
        "id": 3,
        "nombre": "NEW BALANCE",
        "marca": "NEW BALANCE",
        "talla": 28,
        "precio": 2354,
        "imagen": "New.png",
        "oferta": True,
        "descripcion": "Comodidad y estilo deportivo."
    }
]

@app.context_processor
def datos_globales():
    carrito = session.get("carrito", {})
    cantidad = sum(carrito.values())

    return {
        "cantidad_carrito": cantidad
    }

def obtener_carrito():

    carrito = session.get("carrito", {})
    productos_carrito = []

    for id_producto, cantidad in carrito.items():

        producto = next(
            (p for p in PRODUCTOS
             if p["id"] == int(id_producto)),
            None
        )

        if producto:
            item = producto.copy()
            item["cantidad"] = cantidad
            item["subtotal"] = item["precio"] * cantidad
            productos_carrito.append(item)

    return productos_carrito


@app.route("/")
def inicio():

    return render_template(
        "index.html",
        productos=PRODUCTOS,
        titulo="STREET SHOES",
        subtitulo="Descubre nuestra colección"
    )


@app.route("/tenis")
def todos_los_tenis():

    return render_template(
        "index.html",
        productos=PRODUCTOS,
        titulo="TODOS LOS TENIS",
        subtitulo="Explora todos nuestros modelos"
    )


@app.route("/ofertas")
def ofertas():

    productos_oferta = [
        p for p in PRODUCTOS if p["oferta"]
    ]

    return render_template(
        "index.html",
        productos=productos_oferta,
        titulo="OFERTAS",
        subtitulo="Encuentra tus modelos favoritos"
    )


@app.route("/marcas")
def marcas():

    lista_marcas = sorted(set(
        p["marca"] for p in PRODUCTOS
    ))

    return render_template(
        "marcas.html",
        marcas=lista_marcas
    )

@app.route("/marca/<nombre>")
def filtrar_marca(nombre):

    productos_marca = [
        p for p in PRODUCTOS
        if p["marca"].lower() == nombre.lower()
    ]

    return render_template(
        "index.html",
        productos=productos_marca,
        titulo=nombre.upper(),
        subtitulo="Modelos disponibles de esta marca"
    )

@app.route("/agregar/<int:id_producto>", methods=["POST"])
def agregar_carrito(id_producto):

    producto = next(
        (p for p in PRODUCTOS if p["id"] == id_producto),
        None
    )

    if producto:

        carrito = session.get("carrito", {})
        id_texto = str(id_producto)

        carrito[id_texto] = min(
            carrito.get(id_texto, 0) + 1,
            99
        )

        session["carrito"] = carrito

        flash("Producto agregado al carrito.")

    else:
        flash("Producto no encontrado.")

    return redirect(request.referrer or url_for("inicio"))

@app.route("/carrito")
def ver_carrito():

    productos = obtener_carrito()

    total = sum(
        p["subtotal"] for p in productos
    )

    cantidad_total = sum(
        p["cantidad"] for p in productos
    )

    return render_template(
        "carrito.html",
        productos=productos,
        total=total,
        cantidad_total=cantidad_total
    )

@app.route("/actualizar/<int:id_producto>", methods=["POST"])
def actualizar_carrito(id_producto):

    carrito = session.get("carrito", {})

    cantidad = request.form.get("cantidad", type=int)

    if str(id_producto) in carrito:

        if cantidad is not None and cantidad > 0:
            carrito[str(id_producto)] = min(cantidad, 99)
        else:
            carrito.pop(str(id_producto))

    session["carrito"] = carrito

    return redirect(url_for("ver_carrito"))

@app.route("/eliminar/<int:id_producto>", methods=["POST"])
def eliminar_carrito(id_producto):

    carrito = session.get("carrito", {})

    carrito.pop(str(id_producto), None)

    session["carrito"] = carrito

    flash("Producto eliminado.")

    return redirect(url_for("ver_carrito"))

@app.route("/contacto")
def contacto():

    return render_template("contacto.html")

if __name__ == "__main__":
    app.run(debug=True)
