## downloading https://vk.com/obrazovach to db
[obrazovach_database](https://yadi.sk/d/PQVarYAy3HEjAE)
 
- **posts**

| **pid** | text      | ccount         | from_id      |
|---------|-----------|----------------|--------------|
| post id | post text | comments count | community id |


- **comments**:

| **cid**   | text         | pid     | from_id | reply_to_cid                            |
|-----------|--------------|---------|---------|-----------------------------------------|
| comment id| comment text | post id | user id | id of the comment our comment replies to|


- **authors**:

| **uid** | bdate         | city      |
|---------|---------------|-----------|
| user id | date of birth | city name |
