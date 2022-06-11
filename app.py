from flask import Flask, render_template, request, redirect, url_for, session, flash
from configparser import ConfigParser
import dbquery

config_file  = 'config.ini'
config = ConfigParser()
config.read(config_file)

app = Flask(__name__)
app.secret_key = config.get('config','app.secret_key')
medium_list=['Tamil','English']

@app.route('/')
@app.route('/login',  methods=['POST', 'GET'])
def login():
    userbase = dbquery.update_userbase()
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        user = request.form['username']
        pwd = request.form['password']
        if user in userbase:
            if userbase[user]==pwd:
                session["user"] = user
                return redirect(url_for('students'))
            else:
                flash('Invalid Password', "error")
                return render_template('login.html')
        else:
            flash('Invalid User', "error")
            return render_template('login.html')
    return render_template('login.html')

@app.route('/changepass',  methods=['POST', 'GET'])
def changepass():
    if request.method == 'POST' and 'user' in request.form and 'password' in request.form:
        email = request.form['user']
        password = request.form['password']
        dbquery.update_password(email, password)
        flash("Updated Password","success")
        return redirect(url_for('students'))

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect(url_for('login'))

@app.route('/register',  methods=['POST', 'GET'])
def register():
    userbase = dbquery.update_userbase()
    if request.method == 'POST' and 'FullName' in request.form and 'Mobile' in request.form and 'InputEmail' in request.form and 'InputPassword' in request.form and 'RepeatPassword' in request.form:
        fullname = request.form['FullName']
        mobile = request.form['Mobile']
        email = request.form['InputEmail']
        password = request.form['InputPassword']
        if email in userbase:
            flash("User Email Already Exists", "warning")
            return render_template('register.html')
        else:
            dbquery.register_appuser(fullname, mobile, email, password)
            session["user"] = email
            flash("User Registred!", "success")
            return redirect(url_for('students'))
    return render_template('register.html')

@app.route('/students',  methods=['POST', 'GET'])
def students():
    username = session["user"]
    if "user" in session:
        department_list = dbquery.department_dash()
        if request.method == 'POST' and request.form['reg_num'] != '' and 'search' in request.form:
            reg_num = request.form['reg_num']
            student_list = dbquery.student_dash(reg_num, None)
            return render_template('students.html', username=username, student_list=student_list, department_list=department_list, medium_list =medium_list, def_dept = '')
        elif request.method == 'POST' and 'dept_name' in request.form and 'search' in request.form:
            dept_name = request.form['dept_name']
            student_list = dbquery.student_dash(None, dept_name)
            return render_template('students.html', username=username, student_list=student_list, department_list=department_list, medium_list =medium_list, def_dept = dept_name)
        else:
            return render_template('students.html', username=username, student_list=[], department_list=department_list, medium_list =medium_list, def_dept = '')
    else:
        return render_template("login.html")
    
@app.route('/deletestudent',  methods=['POST', 'GET'])
def deletestudent():
    if request.method == 'POST' and 'reg_num' in request.form and 'delete' in request.form:
        reg_num = request.form['reg_num']
        dbquery.delete_student(reg_num)
        return redirect(url_for('students'))

@app.route('/editstudent',  methods=['POST', 'GET'])
def editstudent():
    if request.method == 'POST' and 'reg_num' in request.form and 'edit' in request.form:
        student_name = request.form['student_name']
        reg_num = request.form['reg_num']
        dob = request.form['dob']
        mobile_num = request.form['mobile_num']
        dept_name = request.form['dept_name']
        sems = request.form['sems']
        medium = request.form['medium']
        book_fee = request.form['book_fee']
        fee_paid = request.form['fee_paid']
        student_edit_detail = [student_name, dob, mobile_num, dept_name, sems, medium, book_fee, fee_paid, reg_num]
        dbquery.edit_student(student_edit_detail)
        return redirect(url_for('students'))

@app.route('/createstudent',  methods=['POST', 'GET'])
def createstudent():
    if request.method == 'POST' and 'student_new' in request.form:
        student_name = request.form['student_name']
        reg_num = request.form['reg_num']
        dob = request.form['dob']
        mobile_num = request.form['mobile_num']
        dept_name = request.form['dept_name']
        sems = request.form['sems']
        medium = request.form['medium']
        book_fee = request.form['book_fee']
        fee_paid = request.form['fee_paid']
        student_detail = [student_name, reg_num, dob, mobile_num, dept_name, sems, medium, book_fee, fee_paid]
        try:
            dbquery.create_student(student_detail)
            return redirect(url_for('students'))
        except:
            flash("student already exist or creation Failed, Try Again!", "warning")
            return redirect(url_for('students'))
    return redirect(url_for('students'))

@app.route('/createdepartment',  methods=['POST', 'GET'])
def createdepartment():
    if request.method == 'POST' and 'dept_name' in request.form and 'dept_id' in request.form:
        department_name = request.form['dept_name']
        department_id = request.form['dept_id']
        try:
            department_details = [department_name, department_id]
            dbquery.create_department(department_details)
            return redirect(url_for('departments'))
        except:
            flash("Creation Failed or department already exist, Try Again!", "warning")
            return redirect(url_for('departments'))
    flash("Oops something went wrong, Try Again!", "warning") #useless warning
    return redirect(url_for('departments'))
    
@app.route('/departments')
def departments():
    email = session["user"]
    if "user" in session:
        department_list = dbquery.department_dash()
        return render_template('departments.html', user_email=email, department_list=department_list)
    else:
        return render_template("login.html")

@app.route('/deletedepartment',  methods=['POST', 'GET'])
def deletedepartment():
    if request.method == 'POST' and 'del_dept_id' in request.form and 'delete' in request.form:
        department_id = request.form['del_dept_id']
        dbquery.delete_department(department_id)
        return redirect(url_for('departments'))

@app.route('/books',  methods=['POST', 'GET'])
def books():
    username = session["user"]
    if "user" in session:
        book_list = dbquery.book_dash()
        department_list = dbquery.department_dash()
        return render_template('books.html', username=username, book_list=book_list, department_list=department_list, medium_list =medium_list)
    else:
        return render_template("login.html")

@app.route('/createbook',  methods=['POST', 'GET'])
def createbook():
    if request.method == 'POST' and 'book_new' in request.form:
        book_name = request.form['book_name']
        book_code = request.form['book_code']
        dept_name = request.form['dept_name']
        sems = request.form['sems']
        subject = request.form['subject']
        sub_code = request.form['sub_code']
        medium = request.form['medium']
        paper = request.form['paper']
        price = request.form['price']
        book_detail = [book_name, book_code, dept_name, sems, subject, sub_code, medium, paper, price]
        try:
            dbquery.create_book(book_detail)
            return redirect(url_for('books'))
        except:
            flash("Book already exist or creation Failed, Try Again!", "warning")
            return redirect(url_for('books'))
    return redirect(url_for('books'))

@app.route('/editbook',  methods=['POST', 'GET'])
def editbook():
    if request.method == 'POST' and 'book_code' in request.form and 'edit' in request.form:
        book_name = request.form['book_name']
        book_code = request.form['book_code']
        dept_name = request.form['dept_name']
        sems = request.form['sems']
        subject = request.form['subject']
        sub_code = request.form['sub_code']
        medium = request.form['medium']
        paper = request.form['paper']
        price = request.form['price']
        book_detail = [book_name, dept_name, sems, subject, sub_code, medium, paper, price, book_code]
        dbquery.edit_book(book_detail)
        return redirect(url_for('books'))

@app.route('/deletebook',  methods=['POST', 'GET'])
def deletebook():
    if request.method == 'POST' and 'book_code' in request.form and 'delete' in request.form:
        reg_num = request.form['book_code']
        dbquery.delete_book(reg_num)
        return redirect(url_for('books'))
    
@app.route('/booksassign')
def booksassign():
    username = session["user"]
    if "user" in session:
        student_list = dbquery.student_list()
        all_book_list = dbquery.book_dash()
        department_list = dbquery.department_dash()
        return render_template('booksassign.html', username=username, reg_num='', student_detail=None, student_list = student_list, all_book_list=all_book_list, department_list=department_list)
    else:
        return render_template("login.html")
    
@app.route('/searchstudent',  methods=['POST', 'GET'])
def searchstudent():
    username = session["user"]
    if request.method == 'POST' and 'reg_num' in request.form and 'search' in request.form:
        reg_num = request.form['reg_num']
        student_detail = dbquery.student_detail(reg_num)
        have_book_list = dbquery.student_have_books(reg_num)
        all_book_list = dbquery.book_dash()
        return render_template('booksassign.html', username=username, reg_num=reg_num, student_detail=student_detail,have_book_list=have_book_list,all_book_list=all_book_list)
    else:
        return render_template("login.html")    
    
@app.route('/oneassign',  methods=['POST', 'GET'])
def oneassign():
    username = session["user"]
    if request.method == 'POST' and 'assign_book_code' in request.form and 'assign_reg_num' in request.form:
        reg_num = request.form['assign_reg_num']
        book_code = request.form['assign_book_code']
        dbquery.update_student_book(book_code, reg_num)
        student_detail = dbquery.student_detail(reg_num)
        have_book_list = dbquery.student_have_books(reg_num)
        all_book_list = dbquery.book_dash()
        return render_template('booksassign.html', username=username, reg_num=reg_num, student_detail=student_detail,have_book_list=have_book_list,all_book_list=all_book_list)
    else:
        return render_template("login.html") 
    
@app.route('/removebook',  methods=['POST', 'GET'])
def removebook():
    username = session["user"]
    if request.method == 'POST' and 'del_book_code' in request.form and 'delete' in request.form:
        book_code = request.form['del_book_code']
        reg_num = request.form['del_reg_num']
        dbquery.remove_student_book(book_code, reg_num)
        student_detail = dbquery.student_detail(reg_num)
        have_book_list = dbquery.student_have_books(reg_num)
        all_book_list = dbquery.book_dash()
        return render_template('booksassign.html', username=username, reg_num=reg_num, student_detail=student_detail,have_book_list=have_book_list,all_book_list=all_book_list)
    else:
        return render_template("login.html")     
    
if __name__ == '__main__':
    app.run(debug=True)