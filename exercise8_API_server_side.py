# Tehtävä 1
from flask import Flask, request, jsonify   # Flask: web-sovelluskehys, jolla rakennetaan API
                                            # Request: flaskin osa jolla saadaa HTTP-pyynnön sisältö
import sqlite3                              # jsonify: muuntaa python-olion JSON-muotoon HTTP-vastauksessa
import os

os.chdir(r"C:\Users\turpe\OneDrive\Läppäri_Desktop\Koulu\programming_networks\Tehtävä_koodit")  # Vaihdetaan työskentelykansio

app = Flask(__name__)                       # Luo Flask sovelluksen olion, jota käytetään reittien määrittelyyn

# Luo tietokanta ja taulu jos ei ole vielä olemassa 
def create_db():
    conn = sqlite3.connect("verkkokauppa.db")  # Luo tietokannan jos ei ole olemassa
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year_of_publication INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

create_db()  # suoritetaan heti kun ohjelma käynnistyy


# API ROUTES 

@app.route('/')       # Juuriosoite '/'
def root():
    return "Welcome to the Book Store API!"  # Palautetaan tämä arvo kun käyttäjä menee juuriosoitteeseen '/'

@app.route('/sell/', methods=['POST'])  # POST pyyntö
def sell_book():
    data = request.get_json()    # Tallennetaan POST pyynnön palauttama josn-data python objektiksi

    # Tarkistetaan että JSON sisältää tarvittavat kentät. 
    # If not data = data on tyhjä tai None
    # not all = jos yksikin kenttä puuttuu, palauttaa False
    if not data or not all(k in data for k in ("title", "author", "year_of_publication")):
        return jsonify({"error": "Missing fields"}), 400

     # Pomitaan tiedot JSON-datasta ja tallennetaan muuttujiin
    title = data["title"]
    author = data["author"]
    year = data["year_of_publication"]

    # Tallennetaan tiedot tietokantaan
    conn = sqlite3.connect("verkkokauppa.db")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO products (title, author, year_of_publication) VALUES (?, ?, ?)",
        (title, author, year)
    )
    conn.commit()

    # Haetaan lisätyn kirjan id
    book_id = cur.lastrowid   
    conn.close()

    return jsonify({
        "message": "Book added to inventory",
        "id": book_id,
        "title": title,
        "author": author,
        "year_of_publication": year
    }), 201

#################### Tehtävä 2. #########################
# Tämä hakee listan kirjoista jota on tallennettu tietokantaan
# Muodostettua listaa voidaan katsoa selaimella http://127.0.0.1:5000/list/
# GET pyyntö 

@app.route('/list/', methods=['GET']) 
def list_books():
    conn = sqlite3.connect("verkkokauppa.db")
    cur = conn.cursor()
    cur.execute("SELECT id, title, author, year_of_publication FROM products")
    rows = cur.fetchall()   # luo listan johon lisätään data tupleina
    conn.close()

    # Tallennetaan listaan sanakirjamuodossa 
    books = []
    for row in rows:
        books.append({
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "year_of_publication": row[3]
        })
    return jsonify(books)  # muuntaa python-olion JSON-muotoon HTTP-vastauksessa

################# tehtävä 3 ###########################################
# Tätä voidaan testata vaikka selaimella antamalla url http://127.0.0.1:5000/purchase/2 ja muokkaamalla numeroa perässä joka on id numero

@app.route('/purchase/<int:item_id>', methods=['GET'])
def purchase_book(item_id):
    conn = sqlite3.connect("verkkokauppa.db")
    cur = conn.cursor()

    # Tarkistetaan löytyykö kirja
    cur.execute("SELECT * FROM products WHERE id = ?", (item_id,))
    book = cur.fetchone()

    if book:
        # Poistetaan kirja
        cur.execute("DELETE FROM products WHERE id = ?", (item_id,))
        conn.commit()
        conn.close()
        return jsonify({"message": "ok"}), 200
    else:
        conn.close()
        return jsonify({"error": "not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)


