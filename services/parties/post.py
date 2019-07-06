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

    missing_parameter = 'Error - Required parameter is missing:'

    # Required Fields
    
    party = None
    if 'PARTY' in event:
        party = f"'{event['PARTY']}'"
    else:
        raise ValueError(f'{missing_parameter} PARTY')
        
    short_name = None
    if 'SHORT_NAME' in event:
        short_name = f"'{event['SHORT_NAME']}'"
    else:
        raise ValueError(f'{missing_parameter} SHORT_NAME')

    # Optional Fields
    
    secretary = None
    if 'SECRETARY' in event:
        secretary = f"'{event['SECRETARY']}'"
    else:
        secretary = "null"
        
    founder = None
    if 'FOUNDER' in event:
        founder = f"'{event['FOUNDER']}'"
    else:
        founder = "null"
        
    site_url = None
    if 'SITE_URL' in event:
        site_url = f"'{event['SITE_URL']}'"
    else:
        site_url = "null"
        
    logo_url = None
    if 'LOGO_URL' in event:
        logo_url = f"'{event['LOGO_URL']}'"
    else:
        logo_url = "null"
        
    description = None
    if 'DESCRIPTION' in event:
        description = f"'{event['DESCRIPTION']}'"
    else:
        description = "null"

    query = f'''
        INSERT INTO PARTY(
        PARTY_ID,
        PARTY,
        SHORT_NAME,
        SECRETARY,
        FOUNDER,
        SITE_URL,
        LOGO_URL,
        DESCRIPTION
        )
        VALUES(
        default,
        {party},
        {short_name},
        {secretary},
        {founder},
        {site_url},
        {logo_url},
        {description}
        )
        '''

    queryForId = 'SELECT LAST_INSERT_ID();'

    with conn.cursor() as cur:
        cur.execute(query)
        cur.execute(queryForId)
        rows = cur.fetchall()
        inserted_id = rows[0][0]
        conn.commit()

    response =    {
        "statusCode": 200,
        "message": "Party succesfully created",
        "ID": inserted_id,
    }
    return response
