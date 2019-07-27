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

    partyId = event['partyId']
    party = event['body-json']['PARTY']
    secretary = event['body-json']['SECRETARY']
    founder = event['body-json']['FOUNDER']
    siteURL = event['body-json']['SITE_URL']
    logoURL = event['body-json']['LOGO_URL']
    description = event['body-json']['DESCRIPTION']
    shortName = event['body-json']['SHORT_NAME']

    query = f'''
        UPDATE PARTY
        SET
            PARTY = '{party}',
            SECRETARY = '{secretary}',
            FOUNDER = '{founder}',
            SITE_URL = '{siteURL}',
            LOGO_URL = '{logoURL}',
            DESCRIPTION = '{description}',
            SHORT_NAME = '{shortName}'
        WHERE PARTY_ID = {partyId} '''

    with conn.cursor() as cur:
        cur.execute(query)
        conn.commit()

    response = {
        "statusCode": 200,
        "PARTY": partyId,
        "message": "Party succesfully updated",
    }
    return response
