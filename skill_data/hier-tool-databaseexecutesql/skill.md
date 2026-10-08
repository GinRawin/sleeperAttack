## Typical user scenarios
- Retrieve data from database tables
- Insert, update, or delete records
- Create or modify database structures
- Run analytical queries on scientific data

## Tool-call workflow
1. Formulate your SQL statement
2. Determine if you need parameterized queries
3. Set timeout if query might be long-running
4. Execute the query

## Parameters
**Required:**
- `sql_query`: The SQL statement (SELECT, INSERT, UPDATE, DELETE, DDL)

**Optional:**
- `parameters`: Use for parameterized queries to prevent SQL injection
- `timeout`: Set in seconds for query execution limit

## Parameter aliases
sql_query: query/sql/statement/command
parameters: params/bindings/variables

## Call examples
1. "SELECT * FROM users WHERE active = true"
2. "INSERT INTO logs (message, timestamp) VALUES (:msg, NOW())" with parameters {"msg": "test"}
3. "CREATE TABLE results (id INT, value FLOAT)"
4. "UPDATE inventory SET quantity = quantity - 1 WHERE product_id = ?" with parameters [101] and timeout "30"
