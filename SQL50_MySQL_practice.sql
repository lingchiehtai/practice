#[Select]
#https://leetcode.com/studyplan/top-sql-50/


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