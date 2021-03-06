import mysql.connector
from configparser import ConfigParser

config_file  = 'config.ini'
config = ConfigParser()
config.read(config_file)

db = mysql.connector.connect(
                      host=config.get('config','host'),
                      user=config.get('config','user'),
                      password=config.get('config','password'),
                      database=config.get('config','database')
                    )
cursor = db.cursor()

accounts_table = """CREATE TABLE IF NOT EXISTS accounts (
                    id int(11) NOT NULL AUTO_INCREMENT,
                    username varchar(20) UNIQUE NOT NULL,
                    password varchar(20) NOT NULL,
                    email varchar(100) NOT NULL,
                    PRIMARY KEY(id)
                ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;"""
students_table = """CREATE TABLE IF NOT EXISTS students (
                    id int(11) NOT NULL AUTO_INCREMENT,
                    student_name varchar(100) NOT NULL,
                    reg_num varchar(20) UNIQUE NOT NULL,
                    dob varchar(10) NOT NULL,
                    mobile_num varchar(10) NOT NULL,
                    dept_name varchar(100) NOT NULL,
                    sems varchar(20) NOT NULL,
                    medium varchar(50) NOT  NULL,
                    book_fee varchar(50) NOT  NULL,
                    fee_paid varchar(50) NOT  NULL,
                    PRIMARY KEY(id)
                ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;"""
department_table = """CREATE TABLE IF NOT EXISTS departments (
                        id int(11) NOT NULL AUTO_INCREMENT,
                        dept_name varchar(100) NOT NULL,
                        dept_id varchar(20) NOT NULL,
                        PRIMARY KEY(id)
                    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;"""
books_table = """CREATE TABLE IF NOT EXISTS books (
                    id int(11) NOT NULL AUTO_INCREMENT,
                    book_name varchar(100) NOT NULL,
                    book_code UNIQUE varchar(10) NOT NULL,
                    dept_name varchar(100) NOT NULL,
                    sems varchar(20) NOT NULL,
                    subject varchar(20) NOT NULL,
                    sub_code varchar(20) NOT NULL,
                    medium varchar(20) NOT NULL,
                    paper varchar(20) NOT NULL,
                    price varchar(20) NOT NULL,
                    PRIMARY KEY(id)
                ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;"""

students_books = """CREATE TABLE students_books (
                    book_code VARCHAR(10) REFERENCES books (book_code) ON UPDATE CASCADE ON DELETE CASCADE
                    , reg_num VARCHAR(10) REFERENCES students (reg_num) ON UPDATE CASCADE
                    , CONSTRAINT students_books_pkey PRIMARY KEY (reg_num, book_code)  -- explicit pk
                    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;"""

cursor.execute(accounts_table)
cursor.execute(students_table)
cursor.execute(department_table)
cursor.execute(books_table)
cursor.execute(students_books)

db.commit()