
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

