from flask import Flask, render_template, redirect, request
import mysql.connector

app=Flask(__name__)

# connection to MySQL
con=mysql.connector.connect(
    host='localhost',
    user='root',
    password='ROOT',
    database='tr'
)
cursor=con.cursor()

# Home Page
@app.route("/")
def home():
    return render_template("home.html")

# Characters List 
@app.route("/characters")
def characters():
    cursor.execute("""
        SELECT 
            c.id, 
            c.name, 
            c.image_url, 
            c.description, 
            GROUP_CONCAT(g.name SEPARATOR ', ') as gangs
        FROM characters c
        LEFT JOIN character_gangs cg ON c.id = cg.character_id 
        LEFT JOIN gangs g ON cg.gang_id = g.id 
        GROUP BY c.id
    """)
    characters = cursor.fetchall()
    cursor.execute("SELECT name FROM gangs ORDER BY name")
    all_gangs = [row[0] for row in cursor.fetchall()]
    
    has_unaffiliated = any(char[4] is None or char[4].strip() == "" for char in characters)
    if has_unaffiliated and "Unaffiliated" not in all_gangs:
        all_gangs.append("Unaffiliated")

    return render_template("characters.html", characters=characters, gangs=all_gangs)


# Episodes
@app.route("/episodes")
def episodes():
    cursor.execute("SELECT title, description, arc, releaseddate, rating, thumbnail  FROM episodes")
    episodes=cursor.fetchall()
    return render_template("episodes.html",episodes=episodes)

# Gang Details
@app.route("/gang",methods=['GET','POST'])
def gang():
    if request.method == "POST":
        name=request.form['name']
        email=request.form['email']
        fav=request.form['fav_characters']
        gang=request.form['gang']
        cursor.execute("INSERT INTO gang_members (name,email,fav_characters,gang)VALUES(%s,%s,%s,%s)",(name,email,fav,gang))
        con.commit()
        return redirect("/")
    return render_template("gang.html")

if __name__ == '__main__':
    app.run(debug=True)