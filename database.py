from flask import Flask
import mysql.connector

app = Flask(__name__)

cnx = mysql.connector.connect(user='root', password='gomya', database ='Petrol')
cursor = cnx.cursor(buffered = True)

@app.route('/')
def index():
	return render_template('add_num.html')

@app.route("/post_num", methods = ['POST'])
def post_user():
	num1 = request.form['num']
	add = ("insert into test" 
			"(num)"
			"values (num1)")
	cursor.execute(add)
	cnx.commit()
return redirect(url_for('index'))

cursor.close()
cnx.close()

if __name__=="__main__":
	app.run()


