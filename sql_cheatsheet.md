# SQL Cheat Sheet

## 1. Basic structure

A table:

```text
users
+----+--------+-----+-------------------+
| id | name   | age | email             |
+----+--------+-----+-------------------+
| 1  | Alice  | 25  | alice@example.com |
| 2  | Bob    | 30  | bob@example.com   |
| 3  | Carol  | 22  | carol@example.com |
+----+--------+-----+-------------------+
```

Basic query:

```sql
SELECT name, age
FROM users;
```

Result:

```text
Alice  25
Bob    30
Carol  22
```

---

# 2. SELECT

### Select everything

```sql
SELECT *
FROM users;
```

### Select specific columns

```sql
SELECT name, email
FROM users;
```

### Rename a column

```sql
SELECT name AS username
FROM users;
```

### Calculated columns

```sql
SELECT name, age + 1 AS next_age
FROM users;
```

---

# 3. WHERE — filtering

```sql
SELECT *
FROM users
WHERE age > 25;
```

### Operators

```sql
=       -- equal
<>      -- not equal
!=      -- not equal
>       -- greater
<       -- smaller
>=      -- greater/equal
<=      -- smaller/equal
```

### AND / OR / NOT

```sql
SELECT *
FROM users
WHERE age >= 18
  AND age < 30;
```

```sql
SELECT *
FROM users
WHERE name = 'Alice'
   OR name = 'Bob';
```

```sql
SELECT *
FROM users
WHERE NOT age = 30;
```

---

# 4. IN

Instead of:

```sql
WHERE name = 'Alice'
   OR name = 'Bob'
   OR name = 'Carol'
```

Use:

```sql
WHERE name IN ('Alice', 'Bob', 'Carol');
```

Also:

```sql
WHERE age IN (20, 25, 30);
```

### NOT IN

```sql
WHERE age NOT IN (20, 25, 30);
```

---

# 5. BETWEEN

```sql
SELECT *
FROM users
WHERE age BETWEEN 20 AND 30;
```

Equivalent to:

```sql
WHERE age >= 20
  AND age <= 30;
```

---

# 6. LIKE — pattern matching

```sql
WHERE name LIKE 'A%'
```

Means:

> starts with A

Examples:

```sql
'A%'     -- starts with A
'%a'     -- ends with a
'%ann%'  -- contains ann
'_lice'  -- exactly one character + lice
```

Example:

```sql
SELECT *
FROM users
WHERE name LIKE 'A%';
```

### Case-insensitive search in PostgreSQL

```sql
WHERE name ILIKE 'alice%';
```

---

# 7. NULL

`NULL` means **missing/unknown value**.

Wrong:

```sql
WHERE email = NULL
```

Correct:

```sql
WHERE email IS NULL;
```

```sql
WHERE email IS NOT NULL;
```

Important:

```sql
NULL = NULL
```

doesn't evaluate to `TRUE`.

---

# 8. ORDER BY

### Ascending

```sql
SELECT *
FROM users
ORDER BY age ASC;
```

### Descending

```sql
SELECT *
FROM users
ORDER BY age DESC;
```

`ASC` is usually the default.

Multiple columns:

```sql
SELECT *
FROM users
ORDER BY age DESC, name ASC;
```

---

# 9. LIMIT

Get the first 10 rows:

```sql
SELECT *
FROM users
LIMIT 10;
```

Pagination:

```sql
SELECT *
FROM users
ORDER BY id
LIMIT 10 OFFSET 20;
```

Meaning:

> skip 20, then take 10.

---

# 10. DISTINCT

Remove duplicates:

```sql
SELECT DISTINCT age
FROM users;
```

Multiple columns:

```sql
SELECT DISTINCT city, country
FROM users;
```

---

# 11. Aggregate functions

Very important.

```sql
COUNT()
SUM()
AVG()
MIN()
MAX()
```

### COUNT

```sql
SELECT COUNT(*)
FROM users;
```

### Average

```sql
SELECT AVG(age)
FROM users;
```

### Minimum / maximum

```sql
SELECT MIN(age), MAX(age)
FROM users;
```

### Sum

```sql
SELECT SUM(price)
FROM products;
```

---

# 12. GROUP BY

Suppose:

```text
orders
+----+---------+--------+
| id | country | price  |
+----+---------+--------+
| 1  | Germany | 100    |
| 2  | Germany | 200    |
| 3  | France  | 150    |
| 4  | France  | 300    |
+----+---------+--------+
```

Total per country:

```sql
SELECT country, SUM(price)
FROM orders
GROUP BY country;
```

Result:

```text
Germany   300
France    450
```

Count per country:

```sql
SELECT country, COUNT(*)
FROM orders
GROUP BY country;
```

---

# 13. HAVING

`WHERE` filters **rows**.

`HAVING` filters **groups**.

Example:

```sql
SELECT country, SUM(price) AS total
FROM orders
GROUP BY country
HAVING SUM(price) > 300;
```

Think:

```text
WHERE  → before GROUP BY
GROUP BY
HAVING → after GROUP BY
```

---

# 14. JOIN — extremely important

Imagine:

```text
users
+----+-------+
| id | name  |
+----+-------+
| 1  | Alice |
| 2  | Bob   |
+----+-------+

orders
+----+---------+--------+
| id | user_id | price  |
+----+---------+--------+
| 1  | 1       | 100    |
| 2  | 1       | 200    |
| 3  | 2       | 150    |
+----+---------+--------+
```

### INNER JOIN

```sql
SELECT users.name, orders.price
FROM users
INNER JOIN orders
    ON users.id = orders.user_id;
```

Result:

```text
Alice  100
Alice  200
Bob    150
```

The relationship is:

```text
users.id
   ↓
orders.user_id
```

---

# 15. LEFT JOIN

Get **all users**, even if they don't have orders:

```sql
SELECT users.name, orders.price
FROM users
LEFT JOIN orders
    ON users.id = orders.user_id;
```

If Carol has no orders:

```text
Alice   100
Alice   200
Bob     150
Carol   NULL
```

This is one of the most useful SQL patterns.

---

# 16. JOIN types

Remember:

```text
INNER JOIN
```

Only matching rows.

```text
LEFT JOIN
```

Everything from the left table + matches.

```text
RIGHT JOIN
```

Everything from the right table + matches.

```text
FULL OUTER JOIN
```

Everything from both sides.

Most of the time you'll use:

```text
INNER JOIN
LEFT JOIN
```

---

# 17. Multiple JOINs

```sql
SELECT
    users.name,
    orders.id,
    products.name,
    orders.quantity
FROM users
JOIN orders
    ON users.id = orders.user_id
JOIN products
    ON orders.product_id = products.id;
```

This is extremely common in real applications.

---

# 18. Subqueries

Query inside another query:

```sql
SELECT *
FROM users
WHERE age > (
    SELECT AVG(age)
    FROM users
);
```

Meaning:

> Find users older than the average age.

---

# 19. EXISTS

Check whether related records exist:

```sql
SELECT *
FROM users u
WHERE EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.user_id = u.id
);
```

Meaning:

> Find users who have at least one order.

---

# 20. CASE

SQL's version of `if/else`.

```sql
SELECT
    name,
    age,
    CASE
        WHEN age < 18 THEN 'minor'
        WHEN age < 65 THEN 'adult'
        ELSE 'senior'
    END AS category
FROM users;
```

---

# 21. COALESCE

Replace `NULL` with another value.

```sql
SELECT
    name,
    COALESCE(email, 'No email') AS email
FROM users;
```

If email is `NULL`:

```text
No email
```

---

# 22. INSERT

```sql
INSERT INTO users (name, age, email)
VALUES ('Alice', 25, 'alice@example.com');
```

Multiple rows:

```sql
INSERT INTO users (name, age)
VALUES
    ('Alice', 25),
    ('Bob', 30),
    ('Carol', 22);
```

---

# 23. UPDATE

```sql
UPDATE users
SET age = 26
WHERE id = 1;
```

Multiple columns:

```sql
UPDATE users
SET
    name = 'Alice Smith',
    age = 26
WHERE id = 1;
```

**Always be careful with `UPDATE` without `WHERE`.**

```sql
UPDATE users
SET age = 26;
```

This changes **every user**.

---

# 24. DELETE

```sql
DELETE FROM users
WHERE id = 1;
```

Again:

```sql
DELETE FROM users;
```

deletes **every row**.

---

# 25. CREATE TABLE

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INTEGER,
    email VARCHAR(255) UNIQUE
);
```

Common types:

```text
INTEGER
BIGINT
DECIMAL
NUMERIC
VARCHAR
TEXT
BOOLEAN
DATE
TIMESTAMP
```

PostgreSQL also commonly uses:

```sql
TIMESTAMPTZ
UUID
JSONB
```

---

# 26. Primary key

```sql
id INTEGER PRIMARY KEY
```

A primary key:

* uniquely identifies a row
* cannot be `NULL`
* should be unique

Example:

```text
users
id ← primary key
│
├── 1 Alice
├── 2 Bob
└── 3 Carol
```

---

# 27. Foreign key

```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    FOREIGN KEY (user_id)
        REFERENCES users(id)
);
```

This creates:

```text
users
  id
   ↑
   │
user_id
orders
```

It enforces a relationship between tables.

---

# 28. Constraints

Common constraints:

```sql
PRIMARY KEY
FOREIGN KEY
NOT NULL
UNIQUE
CHECK
DEFAULT
```

Example:

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER CHECK (age >= 0),
    country TEXT DEFAULT 'Germany'
);
```

---

# 29. ALTER TABLE

Add a column:

```sql
ALTER TABLE users
ADD COLUMN phone VARCHAR(30);
```

Remove:

```sql
ALTER TABLE users
DROP COLUMN phone;
```

Rename:

```sql
ALTER TABLE users
RENAME COLUMN name TO username;
```

---

# 30. CREATE INDEX

Indexes make searching faster.

```sql
CREATE INDEX idx_users_email
ON users(email);
```

Useful for frequently searched columns:

```sql
WHERE email = 'alice@example.com'
```

But indexes also have a cost: they consume storage and make `INSERT`/`UPDATE`/`DELETE` somewhat more expensive.

---

# 31. Transactions

Very important in backend development.

```sql
BEGIN;

UPDATE accounts
SET balance = balance - 100
WHERE id = 1;

UPDATE accounts
SET balance = balance + 100
WHERE id = 2;

COMMIT;
```

If something goes wrong:

```sql
ROLLBACK;
```

Think:

```text
BEGIN
  ↓
multiple operations
  ↓
COMMIT → save everything
  OR
ROLLBACK → undo everything
```

---

# 32. CTE — WITH

Useful for complex queries.

```sql
WITH expensive_orders AS (
    SELECT *
    FROM orders
    WHERE price > 100
)
SELECT *
FROM expensive_orders;
```

You can think of it as:

> temporarily name this query.

Multiple CTEs:

```sql
WITH
users_from_germany AS (
    SELECT *
    FROM users
    WHERE country = 'Germany'
),
large_orders AS (
    SELECT *
    FROM orders
    WHERE price > 100
)
SELECT ...
```

---

# 33. Window functions

More advanced but very useful.

Example:

```sql
SELECT
    name,
    salary,
    RANK() OVER (ORDER BY salary DESC) AS rank
FROM employees;
```

Result:

```text
Alice   6000   1
Bob     5000   2
Carol   4000   3
```

Unlike `GROUP BY`, window functions **don't collapse rows**.

Another common example:

```sql
SELECT
    name,
    department,
    salary,
    AVG(salary) OVER (
        PARTITION BY department
    ) AS department_avg
FROM employees;
```

---

# 34. SQL execution order

This is **extremely useful** for understanding SQL:

```text
FROM
  ↓
JOIN
  ↓
WHERE
  ↓
GROUP BY
  ↓
HAVING
  ↓
SELECT
  ↓
DISTINCT
  ↓
ORDER BY
  ↓
LIMIT
```

For example:

```sql
SELECT country, COUNT(*) AS number
FROM users
WHERE age >= 18
GROUP BY country
HAVING COUNT(*) > 10
ORDER BY number DESC
LIMIT 5;
```

Conceptually:

```text
1. FROM users
2. WHERE age >= 18
3. GROUP BY country
4. HAVING COUNT(*) > 10
5. SELECT country, COUNT(*)
6. ORDER BY number DESC
7. LIMIT 5
```

---

# 35. The most important SQL patterns

### Find

```sql
SELECT *
FROM table
WHERE condition;
```

### Sort

```sql
SELECT *
FROM table
ORDER BY column DESC;
```

### Count

```sql
SELECT COUNT(*)
FROM table;
```

### Group

```sql
SELECT category, COUNT(*)
FROM table
GROUP BY category;
```

### Filter groups

```sql
SELECT category, COUNT(*)
FROM table
GROUP BY category
HAVING COUNT(*) > 5;
```

### Join

```sql
SELECT *
FROM a
JOIN b ON a.id = b.a_id;
```

### Insert

```sql
INSERT INTO table (a, b)
VALUES (1, 'hello');
```

### Update

```sql
UPDATE table
SET a = 2
WHERE id = 1;
```

### Delete

```sql
DELETE FROM table
WHERE id = 1;
```

---

# 36. SQL vs NoSQL — quick mental model

For your internship, this distinction is useful:

**SQL**

```text
Database
 ├── users
 ├── machines
 ├── sensors
 └── measurements
```

Tables have structured relationships.

**NoSQL/document style**

```json
{
  "machine": {
    "id": 1,
    "name": "Machine A",
    "sensors": [
      {"id": 1, "type": "temperature"},
      {"id": 2, "type": "pressure"}
    ]
  }
}
```

SQL is particularly strong when you need:

```text
structured data
+
relationships
+
constraints
+
complex queries
+
transactions
```

---

# 37. For your Bosch internship

Given that you'll work with **Python + SQL databases + semantic data/knowledge graphs**, I'd prioritize these SQL topics:

### Tier 1 — must know

```text
SELECT
WHERE
ORDER BY
LIMIT
INSERT
UPDATE
DELETE
NULL
AND / OR
IN
LIKE
JOIN
```

### Tier 2 — very important

```text
GROUP BY
HAVING
COUNT / SUM / AVG
INNER JOIN
LEFT JOIN
PRIMARY KEY
FOREIGN KEY
UNIQUE
NOT NULL
CREATE TABLE
INDEX
TRANSACTIONS
```

### Tier 3 — backend/industrial SQL

```text
CTE / WITH
Subqueries
EXISTS
CASE
COALESCE
Window functions
Query optimization
Indexes
EXPLAIN / EXPLAIN ANALYZE
Transactions
Isolation levels
```

### One pattern I'd memorize especially well

```sql
SELECT
    m.id,
    m.name,
    COUNT(s.id) AS sensor_count
FROM machines m
LEFT JOIN sensors s
    ON s.machine_id = m.id
WHERE m.status = 'ACTIVE'
GROUP BY m.id, m.name
HAVING COUNT(s.id) > 2
ORDER BY sensor_count DESC;
```

This single query combines **JOIN + WHERE + GROUP BY + HAVING + COUNT + ORDER BY**, which are a huge part of practical SQL.
