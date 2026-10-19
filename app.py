
import os
import mysql.connector
from flask import Flask, jsonify

app = Flask(__name__)

def koneksi_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "jenkins_app"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "jenkins_praktikum"),
        connection_timeout=5
    )

@app.route("/")
def hello():
    try:
        db = koneksi_db()
        try:
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO kunjungan (sumber) VALUES (%s)",
                ("Flask Docker Jenkins",)
            )
            db.commit()

            cursor.execute("SELECT COUNT(*) FROM kunjungan")
            total = cursor.fetchone()[0]
            cursor.close()
        finally:
            db.close()

        return f"""
        <h1>Halo dari Flask + Docker + Jenkins!</h1>
        <h2>MySQL berhasil terhubung!</h2>
        <p>Database: jenkins_praktikum</p>
        <p>Total kunjungan: {total}</p>
        """

    except mysql.connector.Error:
        app.logger.exception("Koneksi atau query MySQL gagal")
        return "Gagal terhubung ke MySQL. Periksa konfigurasi.", 503

@app.route("/health")
def health():
    try:
        db = koneksi_db()
        try:
            cursor = db.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
        finally:
            db.close()

        return jsonify(status="ok", database="connected")
    except mysql.connector.Error:
        app.logger.exception("Health check MySQL gagal")
        return jsonify(status="error", database="disconnected"), 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
