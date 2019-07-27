import sys
import logging
import pymysql
import os
from datetime import date


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
                                           
    promise = event['PROMISE']           
    candidate_id = event['CANDIDATE_ID']     
    latitude = event['LATITUDE']
    longitude = event['LONGITUDE']
    device = event['DEVICE']
    user = event['USER_ID']

    #try to add record on promise_master, only allow new ones
    flag = empty(promise)

    if flag != 0:
        promise1 = get_promise_id(promise)
        insert_promise_detail(user,promise1,latitude,longitude,device)
    else:
        insert_promise_master(promise,candidate_id)
        promise1 = get_promise_id(promise)
        insert_promise_detail(user,promise1,latitude,longitude,device)
    
    thisdict =    {
        "statusCode": 200,
        "message": "Sucess promise added",
    }
    return thisdict
    
def get_promise_id(promise):

    query_get_id = f'''
        SELECT
        PROMISE_ID
        FROM PROMISE_MASTER WHERE PROMISE = '{promise}'
        '''
    
    print(query_get_id)


    
    with conn.cursor() as cur:
        cur.execute(query_get_id)
        id_v = (cur.fetchone()[0])
        print(id_v)

    return id_v

def insert_promise_master(promise,candidate_id):
    #get today's date
    today = date.today()
    #query for promise master
    query1 = f'''
        INSERT INTO PROMISE_MASTER(
        PROMISE_ID,
        PROMISE,
        CANDIDATE_ID,
        DATE
        )
        VALUES(
        default,
        '{promise}',
        '{candidate_id}',
        '{today}'
        )
        '''
    print(query1)

    with conn.cursor() as cur:
        cur.execute(query1)
        conn.commit()
    thisdict =    {
        "statusCode": 200,
        "PROMISE": promise,
        "message": "Promise master succesfully created",
    }
    return thisdict
    
def insert_promise_detail(user,promise_id,latitude,longitude,device):
    #get today's date
    today = date.today()
    #query for promise detail
    query2 = f'''
        INSERT INTO PROMISE_DETAIL(
        USER_ID,
        PROMISE_ID,
        LATITUDE,
        LONGITUDE,
        DATE,
        DEVICE
        )
        VALUES(
        '{user}',
        '{promise_id}',
        '{latitude}',
        '{longitude}',
        '{today}',
        '{device}'
        )
        '''
    print(query2)
    
    with conn.cursor() as cur:
        cur.execute(query2)
        conn.commit()

    thisdict =    {
        "statusCode": 200,
        "PROMISE": promise_id,
        "message": "Promise detail succesfully created",
    }
    return thisdict

def empty(promise):
    item_count = 0
    
    query_empty = f'''
        SELECT
        *
        FROM PROMISE_MASTER WHERE PROMISE = '{promise}'
        '''
    
    print(query_empty)
    
    with conn.cursor() as cur:
        cur.execute(query_empty)
        for row in cur:
            item_count += 1
            print(item_count)
        conn.commit()
    return item_count