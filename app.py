from flask import Flask,render_template,request,redirect,flash,url_for
from flask_mysqldb import MySQL

app= Flask(__name__)
app.config["MYSQL_HOST"]='localhost'
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]="5154"
app.config["MYSQL_DB"]="school"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql=MySQL(app)

@app.route("/")
def home():
    con=mysql.connection.cursor()
    qur="select * from student"
    con.execute(qur)
    re=con.fetchall()
    return render_template("home.html",datas=re)

@app.route("/Add",methods=["GET","POST"])
def add():
    if request.method=="POST":
        name=request.form["name"]
        age = request.form["age"]
        city = request.form["city"]
        con = mysql.connection.cursor()
        qur="insert into student (name,age,city) values (%s,%s,%s);"
        con.execute(qur,[name,age,city])
        mysql.connection.commit()
        con.close()
        flash("User data Added")
        return redirect(url_for("home"))
    return render_template("Add.html")
@app.route("/Edit/<id>",methods=["GET","POST"])
def edit(id):
    if request.method=="POST":
        name=request.form["name"]
        age = request.form["age"]
        city = request.form["city"]
        con = mysql.connection.cursor()
        qur="update student set name=%s,age=%s,city=%s where id=%s;"
        con.execute(qur,[name,age,city,id])
        mysql.connection.commit()
        con.close()
        flash("User data Updated")
        return redirect(url_for("home"))
    con = mysql.connection.cursor()
    qur = "select * from student"
    con.execute(qur)
    re = con.fetchone()
    return render_template("Edit.html",data=re)
@app.route("/Delete/<id>",methods=["GET","POST"])
def delete(id):
    con = mysql.connection.cursor()
    qur = "delete from student where id=%s;"
    con.execute(qur,[id])
    mysql.connection.commit()
    con.close()
    flash("User data Deleted")
    return redirect(url_for("home"))


app.secret_key="abc123"
app.run(debug=True)