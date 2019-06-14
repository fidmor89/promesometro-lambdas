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

query = """
    SELECT PARTY_ID,
    PARTY,
    SECRETARY,
    FOUNDED,
    FOUNDER,
    SITE_URL,
    LOGO_URL,
    DESCRIPTION,
    SHORT_NAME
    FROM PARTY """

columns = (
           'PARTY_ID',
           'PARTY',
           'SECRETARY',
           'FOUNDED',
           'FOUNDER',
           'SITE_URL',
           'LOGO_URL',
           'DESCRIPTION',
           'SHORT_NAME')

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
