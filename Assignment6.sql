ALTER TABLE takes
DROP FOREIGN KEY fk_takes_grade;
DROP TABLE IF EXISTS grade_points;
/* [4a]: Create a table grade_points (grade, points) that maps letter grades to number grades. */
CREATE TABLE grade_points (
    letter_grade VARCHAR(5) NOT NULL,
    number_grade FLOAT,
    PRIMARY KEY (letter_grade),
    CONSTRAINT check_number_grade CHECK (number_grade >= 0 AND number_grade <= 4)
);

/* [4b]: The highest grade is A (=4.0), the lowest is F (=0.0), and a + and - respectively increase / decrease the value by 0.3 (i.e. B+ = 3.3 and B- = 2.7). There is no grade A+ or F-.  */
REPLACE INTO grade_points (letter_grade, number_grade)
    VALUES
        ('A', 4.0),
        ('A-', 3.7),
        ('B+', 3.3),
        ('B', 3.0),
        ('B-', 2.7),
        ('C+', 2.3),
        ('C', 2.0),
        ('C-', 1.7),
        ('D+', 1.3),
        ('D', 1.0),
        ('F', 0.0);

/* [4]: Create a table grade_points (grade, points) that maps letter grades to number grades. */
SELECT * FROM grade_points;

/* [5]: Add a foreign key from the grade column in the existing takes table to the new grade_points table. */
ALTER TABLE takes
ADD CONSTRAINT fk_takes_grade
FOREIGN KEY (grade)
REFERENCES grade_points(letter_grade);

/* [6]: Create a view v_takes_points that returns the data in takes table along with the numeric equivalent of the grade. */
CREATE OR REPLACE VIEW v_takes_points AS
SELECT t.*, gp.number_grade AS numeric_grade
FROM takes t
LEFT JOIN grade_points gp ON t.grade = gp.letter_grade;

/* [6]: Create a view v_takes_points that returns the data in takes table along with the numeric equivalent of the grade. */
SELECT * FROM v_takes_points;

/* [7]: Compute the total number of grade points (credits * grade points) earned by student X (pick a student id from the DB). */
SELECT '12345' AS student_id, COALESCE(SUM(c.credits * gp.number_grade), 0) AS total_grade_points
FROM takes t
JOIN course c ON t.course_id = c.course_id
LEFT JOIN grade_points gp ON t.grade = gp.letter_grade
WHERE t.ID = '12345';

/* [8] Compute the GPA - i.e. total grade points / total credits -  for the same student in the previous question. */
SELECT '12345' AS student_id, ROUND(COALESCE(SUM(c.credits * gp.number_grade) / NULLIF(SUM(c.credits), 0), 0), 2) AS gpa
FROM takes t
JOIN course c ON t.course_id = c.course_id
LEFT JOIN grade_points gp ON t.grade = gp.letter_grade
WHERE t.ID = '12345';

/* [9/10]: Find the GPA of all students and create a view v_student_gpa (id, gpa) that gives a dynamic version of the information in the previous question. */
CREATE OR REPLACE VIEW v_student_gpa AS
SELECT s.ID AS student_id,
       ROUND(COALESCE(SUM(c.credits * gp.number_grade), 0), 1) AS total_grade_points,
        COALESCE(SUM(c.credits), 0) AS total_credits,
        ROUND(COALESCE(SUM(c.credits * gp.number_grade) / NULLIF(SUM(c.credits), 0), 0), 2) AS gpa
FROM student s
LEFT JOIN takes t ON s.ID = t.ID
LEFT JOIN course c ON t.course_id = c.course_id
LEFT JOIN grade_points gp ON t.grade = gp.letter_grade
GROUP BY s.ID;

/* [9/10]: Find the GPA of all students and create a view v_student_gpa (id, gpa) that gives a dynamic version of the information in the previous question. */
SELECT * FROM v_student_gpa;