# Intermediate Level SQL Questions
The questions in this section prepares you with the skills of querying the database at the intermediate level, including joining and appending tables, writing conditional statements, and using subqueries. The CRM datasets are very likely to be the ones you will encounter in business, such as retailing. Being able to ask relevant questions is critical for business analyst or data scientist. These questions are designed along that.

## Key knowledge to be learned: 
+ Case statements
+ Left, right, inner, outer, cross, and self joins
+ Union 
+ Subqueries (1 layer to 2 layers) 

### Q1a: Output a list that contains customer_id, company_name, and the total number of orders they have placed. For those who have not placed an order, do not include them in the list. Rank the results by total number of orders in descending order.

```sql
SELECT c.customer_id, c.company_name, count(o.order_id) Total_Order_Count
FROM customers c
INNER JOIN orders o
ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.company_name
ORDER BY Total_Order_Count DESC
```

### Q1b: Output a list that has customer_id, company_name, and the total number of orders they have placed. Now include those who have not placed any order and return 0 as the number of orders. Rank the results by total number of orders in descending order.

```sql
SELECT a.customer_id, a.company_name,
	sum(case when order_id is NULL then 0 else 1 end) as totalorder
FROM customers a
LEFT JOIN orders b on a.customer_id = b.customer_id
GROUP BY a.customer_id, a.company_name
ORDER BY totalorder desc;
```

### Q2a: We want to know how the business was doing every month by looking at the total order amount. Please return the total order amount (unit_price x quantity) group by and order by year and month of the order_date. For the total order amount, keep 2 decimals. 

```sql
SELECT  EXTRACT(MONTH FROM order_date) AS month, EXTRACT(YEAR FROM order_date) AS year,  ROUND(SUM(unit_price*quantity)::numeric, 2) AS total_order_amount
FROM order_details AS d
LEFT JOIN orders AS o
ON d.order_id = o.order_id
GROUP BY year, month
ORDER BY year, month
```

### Q2b: For every ship_country, return the total order amount group by year of order_date; order the result by ship_country, and year of order.

```sql
SELECT  ship_country, EXTRACT(YEAR FROM order_date) AS year,  
                ROUND(SUM(unit_price*quantity)::numeric, 2) AS total_order_amount
FROM order_details AS d
LEFT JOIN orders AS o
ON d.order_id = o.order_id
GROUP BY ship_country, year
ORDER BY ship_country, year
```

### Q3a: Return the top 10 customer_id, company_name of the customers based on their total order amount (not including discount). 

```sql
SELECT  c.customer_id, c.company_name, ROUND(SUM(unit_price*quantity)::numeric,2) Total_order_amount
FROM customers c
LEFT JOIN orders o
ON c.customer_id = o. customer_id
INNER JOIN order_details od
ON o.order_id = od.order_id
GROUP BY c.customer_id, c.company_name
ORDER BY Total_order_amount DESC LIMIT 10
```

### Q3b: Return the bottom 10 customer_id, company_name of the customers based on their total order amount (not including discount). Return 0 if the customer has not placed any order.

```sql
SELECT customer_id, company_name,
               CASE WHEN Total_order_amount IS NULL THEN 0
                          ELSE Total_order_amount END AS Total_order_amount
FROM (SELECT  c.customer_id, c.company_name, ROUND(SUM(unit_price*quantity)::numeric,2) Total_order_amount
             FROM customers c
             LEFT JOIN orders o
             ON c.customer_id = o. customer_id
             INNER JOIN order_details od
             ON o.order_id = od.order_id
             GROUP BY c.customer_id, c.company_name) derivedTable
ORDER BY Total_order_amount LIMIT 10
```

### Q4a: Selects all the cities (only distinct values) from "Customers" and "Suppliers", order by city. If a city came from both "customers" and "suppliers", keep only one record.

```sql
SELECT city FROM customers
UNION
SELECT city FROM suppliers
ORDER BY city
```

### Q4b: Selects all the distinct cities from "Customers" and "Suppliers". If a city came from both "customers" and "suppliers", keep both records. Create a label to indicate if the city came from "customers" or "suppliers".

```sql
SELECT city,'customers' AS "label" FROM customers
UNION 
SELECT city,'suppliers' AS "label" FROM suppliers
ORDER BY city
```

### Q5a: Return the total order amount of product "Chef Anton's Cajun Seasoning" and "Chef Anton's Gumbo Mix" group by year of order_date. Order the result by product_name, year of order_date.

```sql
SELECT product_name, EXTRACT(YEAR FROM order_date) AS year,
              ROUND(SUM(d.unit_price * d.quantity)::numeric, 2) order_amount
FROM products p
LEFT JOIN order_details d
ON p.product_id = d.product_id
LEFT JOIN orders o
ON d.order_id = o.order_id 
WHERE p.product_name IN ('Chef Anton''s Cajun Seasoning', 'Chef Anton''s Gumbo Mix')
GROUP BY product_name, year
ORDER BY product_name, year
```

### Q5b: Select the top 5 purchased product_name in year 1996 of order_date based on total order amount (not including discount). 

```sql
SELECT p.product_name, round(sum(od.unit_price * od.quantity)::numeric,2) as sum
FROM orders o 
INNER JOIN order_details od
ON o.order_id = od.order_id
INNER JOIN products p
ON od.product_id = p.product_id
WHERE date_part('Year', o.order_date) = 1996
GROUP BY p.product_name
ORDER BY sum DESC
LIMIT 5;
```

### Q6a: Return a list that has employee_id, first_name, last_name, and total number of late orders of the employees with late orders, and order the result descending by total number of late orders. Let’s define late orders as those with shipped_date later or equal to required_date (meaning there isn't enough time to get the product to customers by required date. You can ignore the cases when shipped_date is missing.

```sql
SELECT e.employee_id, first_name, last_name, COUNT(Distinct order_id) Late_order 
FROM employees e
LEFT JOIN orders o
ON e.employee_id = o.employee_id
WHERE shipped_date >= required_date
GROUP BY e.employee_id , e.first_name, e.last_name
ORDER BY Late_order DESC
```

### Q6b: For every employee in the employee table, return employee_id, first_name, last_name, total number of orders (0 if not any order), total number of late orders (0 if not any late order), and % of late orders of total orders (0 if total order count is 0 and use 0.xxxx). Order the result by employee_id.

```sql
SELECT e.employee_id, e.first_name, e.last_name,
SUM(CASE WHEN o.order_id IS Null THEN 0 ELSE 1 END) as total_order,
SUM(CASE WHEN o.shipped_date >= o.required_date THEN 1 ELSE 0 END) as total_late_order,
round(SUM(CASE WHEN o.shipped_date >= o.required_date THEN 1 ELSE 0 END)/
	  SUM(CASE WHEN o.order_id IS Null THEN 0 ELSE 1 END)::numeric,4) as percent
FROM employees e
LEFT JOIN orders o
ON e.employee_id = o.employee_id
GROUP BY e.employee_id, e.first_name, e.last_name
ORDER BY e.employee_id;
```
