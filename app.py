from datetime import datetime
import sqlite3
from flask import Flask, jsonify, redirect, render_template, request, url_for

app = Flask(__name__)
DB_PATH = "hospital.db"



def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.executescript(
        """
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialization TEXT NOT NULL,
            availability TEXT NOT NULL,
            phone TEXT,
            email TEXT
        );

        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            doctor_id INTEGER NOT NULL,
            preferred_date TEXT NOT NULL,
            reason TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (doctor_id) REFERENCES doctors(id)
        );

        CREATE TABLE IF NOT EXISTS careers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            role TEXT NOT NULL,
            experience INTEGER,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS bill_payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            invoice_no TEXT NOT NULL,
            amount REAL NOT NULL,
            payment_mode TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        """
    )

    doctor_count = cur.execute("SELECT COUNT(*) as c FROM doctors").fetchone()["c"]
    if doctor_count == 0:
        cur.executemany(
            "INSERT INTO doctors (name, specialization, availability, phone, email) VALUES (?, ?, ?, ?, ?)",
            [
                ("Dr. Asha Rao", "Cardiology", "Mon-Fri 10:00-16:00", "+91 90000 10001", "asha@ths.example"),
                ("Dr. Kiran M", "Orthopedics", "Mon-Sat 09:00-14:00", "+91 90000 10002", "kiran@ths.example"),
                ("Dr. Nivedita S", "Pediatrics", "Mon-Fri 11:00-18:00", "+91 90000 10003", "nivedita@ths.example"),
            ],
        )
    conn.commit()
    conn.close()


@app.route("/")
def home():
    conn = get_db()
    doctors = conn.execute("SELECT * FROM doctors ORDER BY name").fetchall()
    conn.close()
    return render_template("index.html", doctors=doctors)


@app.route("/appointments", methods=["POST"])
def book_appointment():
    data = request.form
    conn = get_db()
    conn.execute(
        """
        INSERT INTO appointments (patient_name, phone, email, doctor_id, preferred_date, reason, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data.get("patient_name"),
            data.get("phone"),
            data.get("email"),
            data.get("doctor_id"),
            data.get("preferred_date"),
            data.get("reason"),
            datetime.utcnow().isoformat(),
        ),
    )
    conn.commit()
    conn.close()
    return redirect(url_for("home") + "#book")


@app.route("/careers", methods=["POST"])
def apply_career():
    data = request.form
    conn = get_db()
    conn.execute(
        "INSERT INTO careers (full_name, email, role, experience, created_at) VALUES (?, ?, ?, ?, ?)",
        (data.get("full_name"), data.get("email"), data.get("role"), data.get("experience", 0), datetime.utcnow().isoformat()),
    )
    conn.commit()
    conn.close()
    return redirect(url_for("home") + "#careers")


@app.route("/payments", methods=["POST"])
def pay_bill():
    data = request.form
    conn = get_db()
    conn.execute(
        "INSERT INTO bill_payments (patient_name, invoice_no, amount, payment_mode, created_at) VALUES (?, ?, ?, ?, ?)",
        (data.get("patient_name"), data.get("invoice_no"), data.get("amount"), data.get("payment_mode"), datetime.utcnow().isoformat()),
    )
    conn.commit()
    conn.close()
    return redirect(url_for("home") + "#billing")


@app.route("/api/doctors")
def doctors_api():
    conn = get_db()
    doctors = [dict(row) for row in conn.execute("SELECT * FROM doctors ORDER BY id").fetchall()]
    conn.close()
    return jsonify(doctors)


@app.route("/api/appointments")
def appointments_api():
    conn = get_db()
    rows = conn.execute(
        """
        SELECT a.id, a.patient_name, a.phone, a.preferred_date, a.reason, a.created_at, d.name AS doctor_name
        FROM appointments a
        JOIN doctors d ON d.id = a.doctor_id
        ORDER BY a.id DESC
        """
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
