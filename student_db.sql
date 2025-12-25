CREATE DATABASE student_db;

USE student_db;

CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    phone VARCHAR(15) UNIQUE,
    course VARCHAR(50),
    email VARCHAR(100)
);
