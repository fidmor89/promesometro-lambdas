import json
import sys
import logging
import rds_config
import pymysql

rds_host  = rds_config.db_endpoint
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name
port = 3306

logger = logging.getLogger()
logger.setLevel(logging.INFO)

print(rds_host)
print(name)
print(password)
print(db_name)

try:
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
except:
    logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
    sys.exit()

logger.info("SUCCESS: Connection to RDS mysql instance succeeded")

def lambda_handler(event, context):
    """
        This function fetches content from MySQL RDS instance
        """

    item_count = 0

    with conn.cursor() as cur:
        #   cur.execute("create table Employee3 ( EmpID  int NOT NULL, Name varchar(255) NOT NULL, PRIMARY KEY (EmpID))")
        cur.execute('insert into PARTY (PARTY_ID,PARTY) values(default,"WINAQ2")')

        conn.commit()
        cur.execute("select * from PARTY")
        for row in cur:
            item_count += 1
            logger.info(row)
            print(row)
    conn.commit()

return "Added %d items from RDS MySQL table" %(item_count)
