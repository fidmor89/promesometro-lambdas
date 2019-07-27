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
C.CANDIDATE_ID,
C.PARTY_ID,
C.POSITION_ID,
C.NAME,
C.DESCRIPTION,
C.SITE_URL,
C.TWITTER,
C.FACEBOOK,
C.STALL,
C.PIC_URL,
P.PARTY,
P2.POSITION
FROM CANDIDATE C
INNER JOIN PARTY P on C.PARTY_ID = P.PARTY_ID
INNER JOIN POSITION P2 on C.POSITION_ID = P2.POSITION_ID """

columns = (
           'CANDIDATE_ID',
           'PARTY_ID',
           'POSITION_ID',
           'NAME',
           'DESCRIPTION',
           'SITE_URL',
           'TWITTER',
           'FACEBOOK',
       'STALL',
       'PIC_URL',
       'PARTY',
       'POSITION')

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
    return results
