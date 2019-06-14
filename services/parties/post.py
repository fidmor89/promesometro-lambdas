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

try:
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
except:
    logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
    sys.exit()

logger.info("SUCCESS: Connection to RDS mysql instance succeeded")

def lambda_handler(event, context):

    party = event['PARTY']
    short_name = event['SHORT_NAME']
    secretary = event['SECRETARY']
    founded = event['FOUNDED']
    founder = event['FOUNDER']
    site_url = event['SITE_URL']
    logo_url = event['LOGO_URL']
    description = event['DESCRIPTION']

    query = f'''
        INSERT INTO PARTY(
        PARTY_ID,
        PARTY,
        SHORT_NAME,
        SECRETARY,
        FOUNDED,
        FOUNDER,
        SITE_URL,
        LOGO_URL,
        DESCRIPTION
        )
        VALUES(
        default,
        '{party}',
        '{short_name}',
        '{secretary}',
        '{founded}',
        '{founder}',
        '{site_url}',
        '{logo_url}',
        '{description}'
        )
        '''
    with conn.cursor() as cur:
        cur.execute(query)
        conn.commit()

    thisdict =    {
        "statusCode": 200,
        "PARTY": party,
        "message": "Party succesfully created",
    }
    return thisdict
