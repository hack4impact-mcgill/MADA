# Script to create a Database, User/Role with Password, and grant all privileges on Database
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

try:
    con = psycopg2.connect(dbname="template1")

    db_name = sql.Identifier("MADA_dev")
    db_test_name = sql.Identifier("MADA_test")
    username = sql.Identifier("madaadmin")
    password = sql.Literal("madameals")

    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cur = con.cursor()

    cur.execute(sql.SQL("CREATE DATABASE {}").format(db_name))
    cur.execute(sql.SQL("CREATE DATABASE {}").format(db_test_name))

    cur.execute(sql.SQL("CREATE USER {} WITH PASSWORD {}").format(username, password))
    cur.execute(
        sql.SQL("GRANT ALL PRIVILEGES ON DATABASE {} to {}").format(db_name, username)
    )
    print("Created database {} successfully!".format("MADA_dev"))

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL {}".format(error))

finally:
    if con:
        cur.close()
        con.close()
        print("PostgreSQL connection is closed")
