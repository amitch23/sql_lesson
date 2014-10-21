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


	#render template, output data into browser
	html = render_template("student_info.html", first_name=row[0],
                                                last_name=row[1],
                                                github=row[2],
                                                grades = row_grades)

	#fetch method in hackbright_app and pass github name
	return html

@app.route("/project")
def get_project():
    hackbright_app.connect_to_db()
    title = request.args.get("project")
    project_description = hackbright_app.get_projects_by_title(title)
    student_grades = hackbright_app.get_student_info_by_project(title)
    html = render_template("project_info.html", id = project_description[0],
                                                title = project_description[1],
                                                 description = project_description[2],
                                                max_grade = project_description[3],
                                                student_grades = student_grades
                                                )
    return html

@app.route("/newstudentform")
def new_student_form():
    return render_template("new_student_form.html")

@app.route("/newstudent")
def new_student():
    hackbright_app.connect_to_db()
    #flask request to collect info from form
    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    github = request.args.get("github")
    #call function to input new data into db
    new_student_info = hackbright_app.make_new_student(first_name, last_name, github)
    #output to browser window via values obtained from processed function...
    html = render_template("student_info.html", first_name=new_student_info[0],
                                                last_name= new_student_info[1],
                                                github = new_student_info[2],
                                                grades = '')
    return html


@app.route("/newprojectform")
def new_project_form():
    return render_template("new_project_form.html")


@app.route("/newproject")
def new_project():
    hackbright_app.connect_to_db()
    
    #flask request to collect info from html form @ new_project_form.html
    title = request.args.get("title")
    description = request.args.get("description")
    max_grade = request.args.get("max_grade")

    #call function in hackbright_app.py to input new data into db
    new_project_info = hackbright_app.add_projects_by_title(title, description, max_grade)
    #output to browser window via values obtained from processed function...
    html = render_template("project_info.html", title=new_project_info[0],
                                                description= new_project_info[1],
                                                max_grade = new_project_info[2],
                                                student_grades='')
    return html

# Make a handler that allows a user to grade a student on a given project.
@app.route("/gradestudentform")
def grade_student_form():
    return render_template("give_grade.html")
    
@app.route("/give_grade")
def grade_student():
    hackbright_app.connect_to_db()
    github = request.args.get("student_github")
    title = request.args.get("project_title")
    grade = request.args.get("grade")

    new_grade_info = hackbright_app.give_grade(github, title, grade)
    html = render_template("student_grade_info.html", github = new_grade_info[0],
                                            title = new_grade_info[1],
                                            grade = new_grade_info[2])
    return html



#On the same page, when you click on a project name,
#it brings you to a page listing all students and their grades 
# for that particular project. You will need a new handler for this page.

if __name__ == "__main__":
    app.run(debug=True)



