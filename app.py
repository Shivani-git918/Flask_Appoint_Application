from flask import Flask, request, render_template, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Loveulife@12",
            database="py_pro"
        )
        if connection.is_connected():
            print("Connected to MySQL database")
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

@app.route('/', methods=['GET'])
def main():
    return render_template('main.html')

@app.route('/book_appointment', methods=['GET'])
def book_appointment():
    return redirect(url_for('index'))

@app.route('/view_appointments', methods=['GET'])
def view_appointments():
    return redirect(url_for('login'))

@app.route('/appointments', methods=['GET'])
def appointments():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM Form"  # Adjust the query as needed
            cursor.execute(query)
            appointments = cursor.fetchall()
            return render_template('appoint.html', appointments=appointments)
        except Error as e:
            print(f"Error fetching appointments: {e}")
            return render_template('appoint.html', message="Failed to retrieve appointments.")
        finally:
            cursor.close()
            connection.close()
    else:
        return render_template('appoint.html', message="Failed to connect to the database.")

@app.route('/mypage', methods=['GET'])
def index():
    return render_template("Form.html")

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    age = request.form['age']
    contact_number = request.form['contact_number']
    date = request.form['date']
    specialist = request.form['specialist']
    username= request.form['username']
    password = request.form['password']

    insert_query = "INSERT INTO Form (name, age, contact_number, date, specialist,username, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    data = (name, age, contact_number, date, specialist, username,password)

    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(insert_query, data)
            connection.commit()
            print("Data inserted successfully")
            message = "Data submitted successfully!"
        except Error as e:
            print(f"Error inserting data: {e}")
            connection.rollback()
            message = "Failed to submit data."
        finally:
            cursor.close()
            connection.close()
    else:
        message = "Failed to connect to the database."

    return render_template('Form.html', message=message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                query = "SELECT * FROM Form WHERE name = %s AND password = %s"
                cursor.execute(query, (username, password))
                user = cursor.fetchone()
                if user:
                    return redirect(url_for('appointments'))
                else:
                    message = "Invalid credentials. Please try again."
                    return render_template('Login.html', message=message)
            except Error as e:
                print(f"Error during login: {e}")
                message = "Error during login."
                return render_template('Login.html', message=message)
            finally:
                cursor.close()
                connection.close()
        else:
            return render_template('Login.html', message="Failed to connect to the database.")
    else:
        return render_template('Login.html')

@app.route('/appoint', methods=['GET'])
def appoint():
    return render_template('appoint.html')  # Ensure you have an `appoint.html` file

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
