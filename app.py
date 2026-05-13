from flask import Flask, request, jsonify, render_template_string
import sqlite3
import os

app = Flask(__name__)

DB_PATH = "database.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name_fr TEXT,
        name_ar TEXT,
        ref TEXT,
        price REAL,
        stock INTEGER
    )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return render_template_string("""
    <h2>SMAILI POS 🚀</h2>

    <h3>Ajouter Produit</h3>
    <input id="name_fr" placeholder="Nom FR"><br>
    <input id="name_ar" placeholder="Nom AR"><br>
    <input id="ref" placeholder="Reference"><br>
    <input id="price" placeholder="Prix"><br>
    <input id="stock" placeholder="Stock"><br>
    <button onclick="add()">Ajouter</button>

    <h3>Produits</h3>
    <button onclick="load()">Afficher</button>

    <table border="1" width="100%">
        <thead>
            <tr>
                <th>ID</th>
                <th>Nom FR</th>
                <th>Nom AR</th>
                <th>Ref</th>
                <th>Prix</th>
                <th>Stock</th>
            </tr>
        </thead>
        <tbody id="data"></tbody>
    </table>

    <script>
    function add(){
        fetch('/add', {
            method: 'POST',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({
                name_fr: document.getElementById('name_fr').value,
                name_ar: document.getElementById('name_ar').value,
                ref: document.getElementById('ref').value,
                price: document.getElementById('price').value,
                stock: document.getElementById('stock').value
            })
        }).then(()=> load())
    }

    function load(){
        fetch('/products')
        .then(res => res.json())
        .then(data => {
            let rows = "";
            data.forEach(p => {
                rows += `
                <tr>
                    <td>${p.id}</td>
                    <td>${p.name_fr}</td>
                    <td>${p.name_ar}</td>
                    <td>${p.ref}</td>
                    <td>${p.price}</td>
                    <td>${p.stock}</td>
                </tr>`;
            });
            document.getElementById('data').innerHTML = rows;
        });
    }
    </script>
    """)

@app.route("/add", methods=["POST"])
def add_product():
    data = request.json
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO products VALUES (NULL,?,?,?,?,?)",
              (data["name_fr"], data["name_ar"], data["ref"], data["price"], data["stock"]))
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})

@app.route("/products")
def get_products():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    rows = c.fetchall()
    conn.close()

    return jsonify([
        {
            "id": r[0],
            "name_fr": r[1],
            "name_ar": r[2],
            "ref": r[3],
            "price": r[4],
            "stock": r[5]
        } for r in rows
    ])
