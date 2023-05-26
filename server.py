from flask import Flask, redirect, url_for, request
import pypyodbc

app = Flask(__name__)

@app.route('/admin')
def admin():
    return redirect(url_for('home'))


@app.route('/name>')
def user(name):
    return f'hello {name}!'


@app.route('/')
def home():
    return '<h1>This is the home page</h1>'


# Azure SQL Database connection details
server = 'tcp:ass7-sql-server.database.windows.net,1433'
database = 'ass7-sql'
username = 'sqladmin'
password = 'BrianLara@1986'
driver = '{ODBC Driver 18 for SQL Server}'
encrypt = 'yes'
no = 'no'


# Function to add new data
def store_form_data(name, email):
    conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};Encrypt={encrypt};TrustServerCertificate={no};Connection Timeout=30;"
    conn = pypyodbc.connect(conn_str)
    cursor = conn.cursor()

    # SQL statement to insert form data into a table
    sql = "INSERT INTO Table_1 (Name, Email) VALUES (?, ?)"
    values = (name, email)

    cursor.execute(sql, values)
    conn.commit()
    conn.close()


# Function to update existing data
def update_form_data(name, email, new_email):
    conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};Encrypt={encrypt};TrustServerCertificate={no};Connection Timeout=30;"
    conn = pypyodbc.connect(conn_str)
    cursor = conn.cursor()

    # SQL statement to insert form data into a table
    cursor.execute("SELECT * FROM Table_1 WHERE EMAIL = ?", [email])
    row = cursor.fetchone()
    if row:
        cursor.execute('UPDATE Table_1 SET EMAIL = ?', [new_email])
        result = 1
    else:
        result = 0
        
    conn.commit()
    conn.close()
    return result

# Function to delete existing data
def delete_form_data(name, email):
    conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};Encrypt={encrypt};TrustServerCertificate={no};Connection Timeout=30;"
    conn = pypyodbc.connect(conn_str)
    cursor = conn.cursor()

    # SQL statement to insert form data into a table 
    cursor.execute("DELETE FROM Table_1 WHERE EMAIL = ?", [email])

    conn.commit()
    conn.close()


@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        store_form_data(name, email)
        return "Form data stored successfully in Azure SQL Database!"
    return '''
    <h1>Add Info in Database</h1>
    <form method="POST" action="/form">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name"><br><br>
        <label for="email">Email:</label>
        <input type="email" id="email" name="email"><br><br>
        <input type="submit" value="Submit">
    </form>
    '''

@app.route('/edit_form',methods=['GET', 'POST'])
def edit_form():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        new_email = request.form.get('new_email')
        result = update_form_data(name, email, new_email)
        if result:
            return "Information updated successfully in Azure SQL Database!"
        else:
            return 'Update Operation Unsuccessful :('
            
    return '''
    <h1>Update Info in Database</h1>
    <form method="POST" action="/edit_form">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name"><br><br>
        <label for="email">Existing Email:</label>
        <input type="email" id="email" name="email"><br><br>
        <label for="new_email">New Email:</label>
        <input type="email" id="new_email" name="new_email"><br><br>
        <input type="submit" value="Submit">
    </form>
    '''

@app.route('/delete_form',methods=['GET', 'POST'])
def delete_form():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        delete_form_data(name, email)
        return "Information deleted successfully in Azure SQL Database!"     
    
    return '''
    <h1>Delete Info from Database</h1>
    <form method="POST" action="/delete_form">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name"><br><br>
        <label for="email">Email:</label>
        <input type="email" id="email" name="email"><br><br>
        <input type="submit" value="Submit">
    </form>
    '''


if __name__ == '__main__':
    app.run()
