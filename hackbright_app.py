import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    #output all the info from a student by their user-provided github name
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    return row

def make_new_student(first_name, last_name, github):
    query = """INSERT into Students values (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    return "Successfully added student: %s %s"%(first_name, last_name)

def get_projects_by_title(title):
    query = """SELECT * FROM Projects WHERE title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    return """\
ID number: %s
title: %s
Description: %s
Grade: %s 
"""%(row[0], row[1], row[2], row[3])


def add_projects_by_title(id, title, description, max_grade):
    query = """INSERT into Projects values (?, ?, ?, ?)"""
    DB.execute(query, (id, title, description, max_grade))
    CONN.commit()
    return "Successfully added project: %s %s %s %s"%(id, title, description, max_grade)

def get_grade_by_project(title):
    query = """SELECT max_grade FROM Projects WHERE title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    return row 


def give_grade(student_github, project_title, grade):
    query = """INSERT into Grades values (?, ?, ?)"""
    DB.execute(query, (student_github, project_title, grade))
    CONN.commit()
    return "Successfully added grade: %s %s %s"%(student_github, project_title, grade)

def get_all_grades(student_github):
    query = """SELECT student_github, project_title, grade FROM grades WHERE student_github=?"""
    DB.execute(query,(student_github,))
    row = DB.fetchone()
    return row



def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "title":
            get_projects_by_title(*args)
        elif command == "add_project":
            add_projects_by_title(*args)
        elif command == "get_grade":
            get_grade_by_project(*args)
        elif command == "give_grade":
            give_grade(*args)
        elif command == "all_grades":
            get_all_grades(*args)
    

    CONN.close()

if __name__ == "__main__":
    main()
