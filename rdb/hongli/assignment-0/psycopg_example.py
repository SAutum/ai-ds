import psycopg

"""
psycopg will automatically read its parameters from the following environment variables:

* username: PGUSER
* password: PGPASSWORD
* host: PGHOST

You can set them in your shell like this (make sure to choose a good password):

```
export PGHOST='127.0.0.1'
export PGUSER='postgres'
export PGPASSWORD='chooseGoodPassword'
```

For future exercises, do not pass those parameters manually to the .connect()
function or it will break our tests!
"""

connection = psycopg.connect()

cursor = connection.cursor()

cursor.execute("SELECT NOW()")

result = cursor.fetchall()

print("Success! You've got a date! It is", result)
