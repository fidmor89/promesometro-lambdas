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
CANDIDATE_ID,
PARTY_ID,
POSITION_ID,
NAME,
DESCRIPTION,
SITE_URL,
TWITTER,
FACEBOOK,
STALL,
PIC_URL
FROM CANDIDATE """

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
		   'PIC_URL')

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
    return results
