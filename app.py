@app.route("/add", methods=["POST"])
def add_product():
    if not is_logged_in():
        return "Unauthorized", 403

    data = request.json

    try:
        price = float(data.get("price", 0))
        stock = int(data.get("stock", 0))
    except:
        return jsonify({"error": "price or stock invalid"}), 400

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    INSERT INTO products (name_fr, name_ar, ref, price, stock)
    VALUES (?, ?, ?, ?, ?)
    """, (
        data.get("name_fr", ""),
        data.get("name_ar", ""),
        data.get("ref", ""),
        price,
        stock
    ))

    conn.commit()
    conn.close()

    return jsonify({"status": "ok"})
