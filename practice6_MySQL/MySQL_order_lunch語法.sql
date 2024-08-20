#建立TABLE 員工編號-餐廳-品項-價格-訂購日期
	CREATE TABLE TodayOrder (
	EmployeeID VARCHAR(10),
	Restaurant VARCHAR(10),
	Item VARCHAR(10),
	Price int(3),
	OrderDate DATE
	);

#讀取csv檔，匯入database中的table


#建立TABLE 員工編號-姓名-部門
	CREATE TABLE EmployeeList (
	EmployeeID VARCHAR(10),
	Name VARCHAR(10),
	Department VARCHAR(10)
	);

#讀取csv檔，匯入database中的table


#每一位員工的6月餐費
    SELECT EmployeeID, sum(Price) as Price_thisMonth
    FROM TodayOrder
    WHERE Month(OrderDate)=6
    GROUP BY EmployeeID;

#每一位員工的6月餐費;合併另一個table的information
    SELECT TA.EmployeeID, Name, Department, sum(Price) as MonthlyPrice
    FROM TodayOrder TA LEFT JOIN EmployeeList TB
    ON TA.EmployeeID=TB.EmployeeID
    WHERE Month(OrderDate)=6 
    GROUP BY TA.EmployeeID, Name, Department;
	
#受歡迎的餐點排行
    SELECT Item, Restaurant, COUNT(Item)
    FROM TodayOrder
    GROUP BY Restaurant, Item
    ORDER BY COUNT(Item) DESC;
	
	
#受歡迎的餐聽排行
    SELECT Restaurant, COUNT(Restaurant)
    FROM TodayOrder
    GROUP BY Restaurant
    ORDER BY COUNT(Restaurant) DESC;
	
