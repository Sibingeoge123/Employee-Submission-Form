from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('submissions.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY,
            name TEXT,
            employee_id TEXT,
            department TEXT,
            employment_status TEXT,
            email TEXT,
            accommodation_requests TEXT,
            file_path TEXT
        )
    ''')
    conn.commit()
    conn.close()

create_table()

@app.route('/submit', methods=['GET', 'POST'])
def submit_form():
    if request.method == 'POST':
        name = request.form['name']
        employee_id = request.form['employee_id']
        department = request.form['department']
        employment_status = request.form['employment_status']
        email = request.form['email']
        accommodation_requests = request.form['accommodation_requests']
        print(request.files)
        
        file = request.files['file']
        file_path = f'uploads/{file.filename}'
        file.save(file_path)

        conn = get_db_connection()
        conn.execute('INSERT INTO submissions (name, employee_id, department, employment_status, email, accommodation_requests, file_path) VALUES (?, ?, ?, ?, ?, ?, ?)',
                     (name, employee_id, department, employment_status, email, accommodation_requests, file_path))
        conn.commit()
        conn.close()

        return redirect(url_for('submit_form'))

    return render_template('submit_form.html')

@app.route('/lookup', methods=['GET', 'POST'])
def lookup_form():
    conn = get_db_connection()
    submissions = conn.execute('SELECT * FROM submissions').fetchall()
    conn.close()

    if request.method == 'POST':
        # Implement filtering logic here
        pass

    return render_template('lookup_form.html', submissions=submissions)

if __name__ == '__main__':
    app.run(debug=True)
