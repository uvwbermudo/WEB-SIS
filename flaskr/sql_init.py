from config import DB_HOST, DB_PASSWORD,DB_USERNAME, DB_NAME

import mysql.connector



mydb = mysql.connector.connect(
  host=DB_HOST,
  user=DB_USERNAME,
  password=DB_PASSWORD
)

mycursor = mydb.cursor()

def create_db():
    mycursor.execute(f"""
    CREATE DATABASE IF NOT EXISTS {DB_NAME};
    USE {DB_NAME};
    
    CREATE TABLE users (
	email VARCHAR(150) NOT NULL,
	user_password VARCHAR(150) NOT NULL,
	PRIMARY KEY(email)
    );

    CREATE TABLE colleges (
	college_code 		VARCHAR(20) NOT NULL,
	college_name 		VARCHAR(100) NOT NULL,
	PRIMARY KEY(college_code),
	UNIQUE(college_name)
    );

    CREATE TABLE courses (
	course_code 		VARCHAR(20) NOT NULL,
	course_name		 	VARCHAR(100) NOT NULL,
	college_code		VARCHAR(20),
	PRIMARY KEY(course_code),
	UNIQUE(course_name),
	FOREIGN KEY(college_code) REFERENCES colleges(college_code) ON DELETE SET NULL ON UPDATE CASCADE
    );

    CREATE TABLE students (
	id 				CHAR(10) NOT NULL,
	first_name 		VARCHAR(50) NOT NULL,
	last_name 		VARCHAR(50) NOT NULL,
	year_level 		INT NOT NULL,
	gender 			CHAR(6) NOT NULL,
	profile_pic 	VARCHAR(240),
	course_code 	VARCHAR(20),
	PRIMARY KEY(id),
	FOREIGN KEY(course_code) REFERENCES courses(course_code) ON DELETE SET NULL ON UPDATE CASCADE,
    FULLTEXT(first_name,last_name)
    );


    """
    )