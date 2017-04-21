## https://vk.com/obrazovach
[obrazovach_database](https://yadi.sk/d/IzRxDgrq3HEAF5)
- **posts** :
***pid*** = post id (primary key)
text = post text
ccount = comments count
from_id = community id

- **comments**:
***cid*** = comment id (primary key)
text = comment text
pid = post id,
from_id = author id
reply_to_cid = id of the comment our comment replies to

- **authors**:
***uid*** = user id  (primary key)
bdate = date of birth
city = city name


