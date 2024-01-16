/* Chapter 3, Slide 53: List all departments along with the number of instructors in each department */
select dept_name,
             ( select count(*)
                from instructor
                where department.dept_name = instructor.dept_name)
             as num_instructors
from department;

/* Sample Query for Testing */
SELECT * FROM instructor;

/* Chapter 3, Slide 14: Find the department names of all instructors, and remove duplicates */
select distinct dept_name
from instructor;

/* Chapter 3, Slide 17: Find all instructors in Comp. Sci. dept with salary > 70000 */
select name
from instructor
where dept_name = 'Comp. Sci.'  and salary > 70000;

/* Chapter 3, Slide 19: Find the names of all instructors who have taught some course and the course_id */
select name, course_id
from instructor, teaches
where instructor.ID = teaches.ID;

/* Chapter 3, Slide 20: Find the names of all instructors who have a higher salary than some instructor in 'Comp. Sci'.*/
select distinct T.name
from instructor as T, instructor as S
where T.salary > S.salary and S.dept_name = 'Comp. Sci.';

/* Chapter 3, Slide 24: List in alphabetic ascending order the names of all instructors */
select distinct name
from instructor
order by name;

/* Chapter 3, Slide 24: List in alphabetic descending order the names of all instructors */
select distinct name
from instructor
order by name desc;

/* Chapter 3, Slide 25: Find the names of all instructors with salary between $90,000 and $100,000 */
select name
from instructor
where salary between 90000 and 100000;

/* Chapter 3, Slide 25: Select the name and course_id for instructors teaching 'Biology' */
select name, course_id
from instructor, teaches
where (instructor.ID, dept_name) = (teaches.ID, 'Biology');

/* Chapter 3, Slide 26: Find courses that ran in Fall 2017 or in Spring 2018 */
(select course_id from section where semester = 'Fall' and year = 2017)
union
(select course_id from section where semester = 'Spring' and year = 2018);

/* Chapter 3, Slide 31: Find the average salary of instructors in the Computer Science department */
select avg (salary)
from instructor
where dept_name= 'Comp. Sci.';

/* Chapter 3, Slide 32: Find the average salary of instructors in each department */
select dept_name, avg (salary) as avg_salary
from instructor
group by dept_name;

/* Homework Query 1: Retrieve all courses that have the letters a, e, i in THAT order in their names */
SELECT * FROM course
where lower(title) like '%a%e%i%';

/* Homework Query 2: Retrieve all courses that have the letters a, e, i in ANY order in their names */
select * from course
where title like '%a%' and title like '%e%' and title like '%i%';

/* Homework Query 3: Retrieve the names of all students who failed a course (grade of F) along with the name of the course that they failed */
select student.name, course.title
from student
join takes on student.ID = takes.ID
join course on takes.course_ID = course.course_ID
where takes.grade = 'F';

/* Homework Query 4: Retrieve the percentage of solid A grades compared to all courses, and rename that column "Percent_A" */
select avg(case when grade = 'A' then 100 else 0 end) as Percent_A
from takes;

/* Homework Query 5: Retrieve the names and numbers of all courses that do not have prerequisites. */
select title, course_id
from course c
where not exists (
    select 1
    from prereq p
    where p.course_id = c.course_id
);

/* Homework Query 6: Retrieves the names of all students and their advisors if they have one. */
select s.name, i.name as advisor_name
from student s
inner join advisor a on s.ID = a.s_ID
inner join instructor i on a.i_ID = i.ID;