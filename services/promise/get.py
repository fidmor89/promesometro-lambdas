import sys
import logging
import pymysql
import os

# Read configuration from enviroment variables.
rds_host = os.environ['db_endpoint']
name = os.environ['db_username']
password = os.environ['db_password']
db_name = os.environ['db_name']
port = os.environ['db_port']

logger = logging.getLogger()
logger.setLevel(logging.INFO)

query = """
SELECT
PM.PROMISE_ID,
PM.PROMISE,
C.CANDIDATE_ID,
C.NAME,
P.PARTY,
P.PARTY_ID,
PO.POSITION,
PO.POSITION_ID
FROM PROMISE_MASTER PM
INNER JOIN CANDIDATE C on PM.CANDIDATE_ID = C.CANDIDATE_ID
INNER JOIN PARTY P ON P.PARTY_ID = C.PARTY_ID
INNER JOIN POSITION PO ON PO.POSITION_ID = C.POSITION_ID """

columns = (
           'PROMISE_ID',
           'PROMISE',
           'CANDIDATE_ID',
           'NAME',
           'PARTY',
           'PARTY_ID',
           'POSITION',
           'POSITION_ID')

try:
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
except:
    logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
    sys.exit()

logger.info("SUCCESS: Connection to RDS mysql instance succeeded")

def lambda_handler(event, context):
    with conn.cursor() as cur:
        cur.execute(query)
        results = []
        for row in cur.fetchall():
            results.append(dict(zip(columns, row)))
        conn.commit()
        print("results:")
        print(results)

    return results
