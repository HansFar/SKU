import os
from flask import Flask, render_template, request, jsonify
from flask import request
from services.excel_service import (
    search_by_sku,
    actualizar_excel_limpio,
    generar_excel_limpio_desde_archivo,
    get_excel_info
)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/estado")
def estado():
    return jsonify({"archivo": get_excel_info()})


@app.route("/actualizar", methods=["POST"])
def actualizar():
    resultado = actualizar_excel_limpio()
    return jsonify(resultado)

@app.route("/subir_excel", methods=["POST"])
def subir_excel():
    if "file" not in request.files:
        return {"status": "error", "mensaje": "No se envió ningún archivo"}

    file = request.files["file"]

    if file.filename == "":
        return {"status": "error", "mensaje": "Archivo sin nombre"}

    os.makedirs("uploads", exist_ok=True)
    ruta = os.path.join("uploads", file.filename)
    file.save(ruta)

    ok, mensaje = generar_excel_limpio_desde_archivo(ruta)

    if ok:
        return {"status": "ok", "mensaje": mensaje}

    return {"status": "error", "mensaje": mensaje}

@app.route("/buscar", methods=["POST"])
def buscar():
    data = request.get_json()
    sku = data.get("sku", "").strip()

    if not sku:
        return jsonify([])

    resultado = search_by_sku(sku)
    print("🧪 Resultado búsqueda:", resultado)

    return jsonify(resultado)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

