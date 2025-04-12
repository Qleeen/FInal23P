from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)
API_URL = "http://127.0.0.1:5555/peliculas"


@app.route('/')
def index():
    response = requests.get(API_URL)
    peliculas = response.json()
    return render_template("index.html", peliculas=peliculas)


@app.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        nueva = {
            "titulo": request.form['titulo'],
            "genero": request.form['genero'],
            "anio": int(request.form['anio']),
            "clasificacion": request.form['clasificacion'].upper()
        }
        requests.post(API_URL, json=nueva)
        return redirect(url_for('index'))
    return render_template("crear.html")


@app.route('/detalle/<int:id>')
def detalle(id):
    response = requests.get(f"{API_URL}/{id}")
    if response.status_code == 200:
        pelicula = response.json()
        return render_template("detalle.html", pelicula=pelicula)
    return "Película no encontrada", 404


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if request.method == 'POST':
        actualizada = {
            "titulo": request.form['titulo'],
            "genero": request.form['genero'],
            "anio": int(request.form['anio']),
            "clasificacion": request.form['clasificacion'].upper()
        }
        requests.put(f"{API_URL}/{id}", json=actualizada)
        return redirect(url_for('index'))

    response = requests.get(f"{API_URL}/{id}")
    if response.status_code == 200:
        pelicula = response.json()
        return render_template("editar.html", pelicula=pelicula)
    return "Película no encontrada", 404


@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    requests.delete(f"{API_URL}/{id}")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
