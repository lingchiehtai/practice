
#https://leetcode.com/studyplan/top-sql-50/

#[Select]

#1757. Recyclable and Low Fat Products
select product_id 
from Products 
where low_fats='Y' and recyclable='Y'

#584. Find Customer Referee
select name 
from Customer 
where referee_id!=2 or referee_id is null

#595. Big Countries
select name,  population, area 
from World 
where area>=3000000 or population>=25000000

#1148. Article Views I
SELECT DISTINCT author_id as id
FROM Views
WHERE author_id = viewer_id
ORDER BY id;

#1683. Invalid Tweets
select tweet_id 
from Tweets 
where length(content)>15


#[Basic Joins]
#1378. Replace Employee ID With The Unique Identifier
select unique_id, name 
from Employees 
left join EmployeeUNI on Employees.id=EmployeeUNI.id

#1068. Product Sales Analysis I
select product_name, year, price 
from Sales left join Product 
on Sales.product_id=Product.product_id 

#197. Rising Temperature
SELECT w1.id
FROM Weather w1 
JOIN Weather w2
ON w1.recordDate = DATE_ADD(w2.recordDate,INTERVAL 1 DAY)
WHERE w1.temperature > w2.temperature

#1661. Average Time of Process per Machine
select machine_id, round(avg(diff), 3) as processing_time
from ( 
select machine_id, process_id, Max(timestamp)-Min(timestamp) as diff
from Activity
group by machine_id, process_id) as table_diff
group by machine_id

#577. Employee Bonus
select name, bonus
from Employee EE left join Bonus BB
on EE.empId = BB.empId
where BB.bonus<1000 or BB.bonus is NULL

#1280. Students and Examinations
select S1.student_id, S1.student_name, S2.subject_name, count(EE.subject_name) as attended_exams
from (Students S1 cross join Subjects S2)
left join Examinations EE
on S1.student_id = EE.student_id
and S2.subject_name = EE.subject_name
group by S1.student_id, S2.subject_name
order by S1.student_id, S2.subject_name

#620. Not Boring Movies
select id , movie, description, rating
from Cinema
where id % 2 !=0 and description !='boring'
order by rating desc

#1251. Average Selling Price
select p.product_id, ifnull(round(sum(p.price*u.units)/sum(u.units),2),0) as average_price
from Prices p left join UnitsSold u 
on p.product_id=u.product_id and (u.purchase_date between p.start_date and p.end_date)
group by p.product_id


#1075. Project Employees I
select project_id, round(avg(experience_years),2) as average_years
from Project P left join Employee E
on P.employee_id=E.employee_id
group by project_id

#1633. Percentage of Users Attended a Contest
select contest_id, round(100*count(contest_id)/(select count(user_id) from Users),2) as percentage
from Register 
group by contest_id
order by percentage DESC, contest_id

#2356. Number of Unique Subjects Taught by Each Teacher
select teacher_id, count(distinct subject_id) as cnt 
from Teacher 
group by teacher_id
