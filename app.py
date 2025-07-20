
from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('vehicles.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    total = cur.execute("SELECT COUNT(*) FROM vehicles").fetchone()[0]
    checked = cur.execute("SELECT COUNT(*) FROM vehicles WHERE status = 'ตรวจสอบแล้ว'").fetchone()[0]
    remaining = total - checked
    percent = round((checked / total) * 100, 2) if total else 0
    conn.close()
    return render_template('index.html', total=total, checked=checked, remaining=remaining, percent=percent)

@app.route('/search')
def search():
    vehicle_number = request.args.get('vehicle_number')
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM vehicles WHERE vehicle_number = ?", (vehicle_number,))
    row = cur.fetchone()
    conn.close()
    result = dict(row) if row else None
    return render_template('search.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
