from flask import Flask, render_template, request, redirect, jsonify
import mysql.connector
from datetime import date

app = Flask(__name__)
print("started")
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="af330060",
        database="attendance_db"
    )

@app.route('/')
def index():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return render_template("index.html", students=students)

@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    data = request.get_json()
    conn = get_connection()
    cursor = conn.cursor()
    for entry in data['attendance']:
        roll_no = entry['roll_no']
        status = entry['status']
        cursor.execute("SELECT student_id FROM students WHERE roll_no = %s", (roll_no,))
        student = cursor.fetchone()
        if student:
            student_id = student[0]
            cursor.execute(
                "INSERT INTO attendance (student_id, date, status) VALUES (%s, %s, %s)",
                (student_id, date.today(), status)
            )
    conn.commit()
    conn.close()
    return jsonify({'message': 'Attendance marked successfully'}), 200


@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        roll_no = request.form['roll_no']
        student_class = request.form['class']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, roll_no, class) VALUES (%s, %s, %s)", 
                       (name, roll_no, student_class))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template("add_student.html")

@app.route('/report')
def report():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT s.name, s.roll_no, s.class, a.date, a.status
        FROM attendance a
        JOIN students s ON a.student_id = s.student_id
        ORDER BY a.date DESC
    """
    cursor.execute(query)
    records = cursor.fetchall()
    conn.close()
    return render_template("report.html", records=records)

if __name__ == '__main__':
    app.run(debug=True)