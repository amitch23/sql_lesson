from flask import Flask, render_template, request 
import hackbright_app #import py file that interacts with db


app = Flask(__name__) #create an instance of the flask class

@app.route("/")
def get_github():
	return render_template("get_github.html")


#url pattern decorator  that sets up the connection to url
@app.route("/student") #also, url handler?

#event handler, get_student = "handler name" (function rename?)
def get_student():
	#call the function in hackbright_app to connect to db file in dir
	hackbright_app.connect_to_db()
	
	#request.args variable is a dict (?) - this is the line that's connected to
	# how info is input into the URL after the '?'
	student_github = request.args.get("github")
	#fetch all the information from the row about one student 
	row = hackbright_app.get_student_by_github(student_github)
	row_grades = hackbright_app.get_all_grades(student_github)

#On the get_student handler, display a user's 
#grades for all of their projects they've completed. # Jinja documentation
#questions:
# Shouldn't I be getting ALL their grades for multiple projects? 
#how do I output more than one row ?

	#render template, output data into browser
	html = render_template("student_info.html", first_name=row[0],
                                                last_name=row[1],
                                                github=row[2],
                                                grades = row_grades[2])



	#fetch method in hackbright_app and pass github name
	return html



if __name__ == "__main__":
    app.run(debug=True)