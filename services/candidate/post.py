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

    party_id = event['PARTY_ID']
    position_id = event['POSITION_ID']
    name = event['NAME']
    description = event['DESCRIPTION']
    site_url = event['SITE_URL']
    twitter = event['TWITTER']
    facebook = event['FACEBOOK']
    stall = event['STALL']
    pic_url = event['PIC_URL']

    query = f'''
        INSERT INTO CANDIDATE(
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
        )
        VALUES(
        default,
        '{party_id}',
        '{position_id}',
        '{name}',
        '{description}',
        '{site_url}',
        '{twitter}',
        '{facebook}',
        '{stall}',
        '{pic_url}'
        )
        '''
    with conn.cursor() as cur:
        cur.execute(query)
        conn.commit()

    thisdict =    {
        "statusCode": 200,
        "PARTY": name,
        "message": "Party succesfully created",
    }
    return thisdict
