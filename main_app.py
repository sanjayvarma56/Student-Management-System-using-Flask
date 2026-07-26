from flask import Flask, render_template, request, redirect, url_for
import sqlite3 as sql
app = Flask(__name__)
def init_db():
    with sql.connect("database.db") as con:
        cur = con.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            addr TEXT NOT NULL,
            city TEXT NOT NULL,
            pin TEXT NOT NULL
        )
        """)
        con.commit()
init_db()
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/enternew')
def new_student():
    return render_template('student.html')
@app.route('/addrec',methods = ['POST','GET'])
def addrec():
    if request.method == 'POST':
        try:
            nm = request.form['nm']
            addr = request.form['add']
            city = request.form['city']
            pin = request.form['pin']
            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO students (name,addr,city,pin) VALUES (?,?,?,?)",(nm,addr,city,pin) )
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"
        finally:
            return render_template("result.html",msg = msg)
@app.route('/delete/<int:id>')
def delete(id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("DELETE FROM students WHERE id = ?", (id,))
        con.commit()
    return redirect(url_for('list'))
@app.route('/edit/<int:id>')
def edit(id):
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM students WHERE id=?", (id,))
    row = cur.fetchone()
    con.close()
    return render_template("edit.html", row=row)
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    nm = request.form['nm']
    addr = request.form['add']
    city = request.form['city']
    pin = request.form['pin']
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("""
        UPDATE students
        SET
            name=?,
            addr=?,
            city=?,
            pin=?
        WHERE id=?
        """, (nm, addr, city, pin, id))
        con.commit()
    return redirect(url_for('list'))
@app.route('/list')
def list():
    search = request.args.get("search")
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    if search:
        cur.execute(
            "SELECT * FROM students WHERE name LIKE ?",
            ('%' + search + '%',)
        )
    else:
        cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    con.close()
    return render_template("list.html", rows=rows)
if __name__ == '__main__':
    app.run(debug = True)