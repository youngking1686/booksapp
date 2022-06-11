import mysql.connector
from mysql.connector import IntegrityError
from configparser import ConfigParser

config_file  = 'config.ini'
config = ConfigParser()
config.read(config_file)

class Database:
    def __init__(self):
        self.mydb = mysql.connector.connect(
                      host=config.get('config','host'),
                      user=config.get('config','user'),
                      password=config.get('config','password'),
                      database=config.get('config','database')
                    )
        self.cursor = self.mydb.cursor()
        self.commit = self.mydb.commit()
        
    def commit(self):
        self.mydb.commit()
        
    def fetchall(self,sql, params=None):
        db = self.cursor
        db.execute(sql, params or ())
        return db.fetchall()
    
    def fetchone(self,sql, params=None):
        db = self.cursor
        db.execute(sql, params or ())
        return db.fetchone()
    
    def execute(self,sql, params=None):
        try:
            db = self.cursor
            db.execute(sql, params or ())
            Database.commit(self)
            return "done"
        except IntegrityError as e:
            return e

def update_userbase():
    db = Database()
    userlist = db.fetchall('SELECT username, password FROM accounts')
    userbase={row[0]:row[1] for row in userlist}
    return userbase
        
def register_account(username, email, password):
    db = Database()
    db.execute("""INSERT INTO accounts (username, password, email) VALUES (%s, %s, %s);""", (username, password, email))

def update_password(username, password):
    db = Database()
    db.execute("""UPDATE accounts SET password=%s WHERE username=%s;""", (password, username))
    return { 'status': 'updated'  }

def create_department(dept_detail):
    db = Database()
    db.execute("""INSERT IGNORE INTO departments (dept_name, dept_id) VALUES (%s, %s);""", (dept_detail))
    return { 'status': 'updated'  }

def create_student(student_detail):
    db = Database()
    db.execute("""INSERT IGNORE INTO students  (student_name, reg_num, dob, mobile_num, dept_name, sems, medium, book_fee, fee_paid)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);""", (student_detail))
    return { 'status': 'updated'  }

def create_book(book_detail):
    db = Database()
    db.execute("""INSERT IGNORE INTO books (book_name, book_code, dept_name, sems, subject, sub_code, medium, paper, price) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);""", (book_detail))

def edit_student(student_edit_detail):
    db = Database()
    db.execute("""UPDATE students SET student_name= %s, dob= %s, mobile_num= %s,
                dept_name= %s, sems= %s, medium= %s, book_fee= %s, fee_paid= %s  WHERE reg_num=%s;""", (student_edit_detail))
    return { 'status': 'updated'  }

def edit_department(department_edit_detail):
    db = Database()
    db.execute("""UPDATE departments SET dept_name= %s WHERE dept_id=%s;""", (department_edit_detail))
    return { 'status': 'updated'  }

def edit_book(book_edit_detail):
    db = Database()
    db.execute("""UPDATE books SET book_name= %s, dept_name= %s, sems= %s,
                subject= %s, sub_code= %s, medium= %s, paper= %s, price= %s  WHERE book_code=%s;""", (book_edit_detail))
    return { 'status': 'updated'  }

def update_student_book(book_code, reg_num):
    try:
        db = Database()
        db.execute("""INSERT IGNORE INTO students_books (book_code, reg_num) VALUES (%s, %s);""", (book_code,reg_num,))
        return { 'status': 'updated'  }
    except:
        return { 'status': 'ok'  }

def remove_student_book(book_code, reg_num):
    try:
        db = Database()
        db.execute("""DELETE FROM students_books WHERE book_code=%s AND reg_num=%s;;""", (book_code,reg_num,))
        return { 'status': 'updated'  }
    except:
        return { 'status': 'ok'  }

def delete_student(reg_num):
    db = Database()
    db.execute("""DELETE FROM students WHERE reg_num=%s;""", (reg_num,))
    return { 'status': 'deleted'  }

def delete_department(dept_id):
    db = Database()
    db.execute("""DELETE FROM departments WHERE dept_id=%s;""", (dept_id,))
    return { 'status': 'deleted'  }

def delete_book(book_code):
    db = Database()
    db.execute("""DELETE FROM books WHERE book_code=%s;""", (book_code,))
    return { 'status': 'deleted'  }

def student_list():
    db = Database()
    ans =db.fetchall("SELECT * FROM students;")
    student_list=[]
    for student in ans:
        new ={'reg_num':student[2],'student_name':student[1]}
        student_list.append(new)
    yield student_list

def department_list():
    db = Database()
    ans =db.fetchall("SELECT * FROM group_table;")
    department_list = [dept[1] for dept in ans]
    return department_list

def student_dash(reg_num, dept_name):
    print(reg_num, dept_name)
    db = Database()
    if reg_num is not None:
        ans =db.fetchall("SELECT * FROM students WHERE reg_num =%s;", (reg_num,))
    elif dept_name is not None:
        ans =db.fetchall("SELECT * FROM students WHERE dept_name =%s;", (dept_name,))
    else:
        return []
    student_list = []
    for i in range(len(ans)):
        dict_1 = {'student_name': ans[i][1],
                'reg_num': ans[i][2],
                'dob': ans[i][3],
                'mobile_num': ans[i][4],
                'dept_name': ans[i][5],
                'sems': ans[i][6],
                'medium': ans[i][7],
                'book_fee': ans[i][8],
                'fee_paid': ans[i][9]}
        student_list.append(dict_1)
    return student_list

def department_dash():
    db = Database()
    ans =db.fetchall("SELECT * FROM departments;")
    department_list = []
    for i in range(len(ans)):
        dict_1 = {'dept_name': ans[i][1],
                'dept_id': ans[i][2]}
        department_list.append(dict_1)
    return department_list

def book_dash():
    db = Database()
    ans =db.fetchall("SELECT * FROM books;")
    book_list = []
    for i in range(len(ans)):
        dict_1 = {'book_name': ans[i][1],
                'book_code': ans[i][2],
                'dept_name': ans[i][3],
                'sems': ans[i][4],
                'subject': ans[i][5],
                'sub_code': ans[i][6],
                'medium': ans[i][7],
                'paper': ans[i][8],
                'price': ans[i][9]}
        book_list.append(dict_1)
    return book_list

def student_detail(reg_num):
    db = Database()
    ans =db.fetchone("SELECT * FROM students WHERE reg_num=%s;", (reg_num,))
    student_detail ={'student_name':ans[1],'reg_num':ans[2], 'dept_name': ans[5], 'sems': ans[6], 'medium':ans[7]}
    return student_detail

def student_have_books(reg_num):
    db = Database()    
    ans = db.fetchall("""SELECT * FROM books WHERE book_code IN (SELECT book_code FROM students_books WHERE reg_num=%s);""", (reg_num,))
    book_have = []
    book_fee = []
    for i in range(len(ans)):
        dict_1 = {'book_name': ans[i][1],
                'book_code': ans[i][2],
                'subject': ans[i][5],
                'sub_code': ans[i][6]}
        book_have.append(dict_1)
        book_fee.append(ans[i][9])
    book_fees = sum([float(fee) for fee in book_fee])
    db = Database()
    db.execute("""UPDATE students SET book_fee= %s WHERE reg_num=%s;""", (book_fees, reg_num,))
    return book_have

def update_bookfees(book_fee, reg_num):
    db = Database()
    db.execute("""UPDATE students SET book_fee= %s WHERE reg_num=%s;""", (book_fee, reg_num,))
    return { 'status': 'updated'  }

