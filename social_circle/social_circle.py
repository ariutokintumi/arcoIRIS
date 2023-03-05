# Copyright 2022 Cartesi Pte. Ltd.
#
# SPDX-License-Identifier: Apache-2.0
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy of the
# License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

from os import environ
import traceback
import logging
import requests
import json
import sqlite3

list_of_users = []

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")

con = sqlite3.connect("data.db")

#how to create an empty variable 
def init_db():
    cur = con.cursor()
    cur.execute(""" 
        CREATE TABLE IF NOT EXISTS payloads(
            payload text, sender text, input integer, epoch integer, created_at date
        )
    
    """)
    con.commit()

INSERT_SQL = """
INSERT INTO payloads (payload, sender, input, epoch, created_at)
VALUES (?,?,?,?,?)
"""

class User:
    def __init__(self, username,wallet_address):
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.bio = bio
        self.people = []
        self.wallet_address = wallet_address

        
    def add_friend(self,friend):
        if friend in self.friends:
            raise ValueError("User is already a friend.")
        
    def get_friends(self):
        return self.people
    
    def __str__(self):
        return f"{self.firstname} {self.lastname}"
    
    def add_friend(self, friend):
        self.people.append(friend)
    
    def get_friends(self):
        for User in self.people:
            return f"{self.firstname} {self.lastname}"
        
    def respond(self,yorn,sender):
        if yorn == ('y'or'yes'or 'Y' or 'YES'):
            sender.add_friend(self)
            self.add_friend(sender)
            print(f'{self} and {sender} are now friends!')
            return "accept"
        #send to catesi node 

        elif yorn == ('n'or'no'or 'N' or 'NO'):
            return "reject"
        
    def accepts(self,friend):
        self.people.append(friend)
        return f'I just became friends with {friend}'

def get_user_with_username(username):
    count = 0
    for a in list_of_users:
        if a.username == username:
            return count
        else:
            count +=1

def get_username_with_wallet(wallet_address):
    count = 0
    for a in list_of_users:
        if a.wallet_address == wallet_address:
            return count
        else:
            count +=1

accept_or_reject = 'yes'


#host mode link fixed
#docker compose -f ./docker-compose.yml -f ./docker-compose.override.yml -f ./docker-compose-host.yml up
#ROLLUP_HTTP_SERVER_URL="http://127.0.0.1:5004" python3 social_circle.py 


def hex2str(hex):
    """
    Decodes a hex string into a regular string
    """
    return bytes.fromhex(hex[2:]).decode("utf-8")

def str2hex(str):
    """
    Encodes a string as a hex string
    """
    return "0x" + str.encode("utf-8").hex()

def handle_advance(data):
    """
    An advance request may be processed as follows:

    1. A notice may be generated, if appropriate:

    #how to create a notice
    response = requests.post(rollup_server + "/notice", json={"payload": data["payload"]})

    logger.info(f"Received notice status {response.status_code} body {response.content}")

    2. During processing, any exception must be handled accordingly:

    try:
        # Execute sensible operation
        op.execute(params)

    except Exception as e:
        # status must be "reject"
        status = "reject"
        msg = "Error executing operation"
        logger.error(msg)
        response = requests.post(rollup_server + "/report", json={"payload": str2hex(msg)})

    finally:
        # Close any resource, if necessary
        res.close()

    3. Finish processing

    return status
    """

    """
    The sample code from the Echo DApp simply generates a notice with the payload of the
    request and print some log messages.
    """
    #put pyhton code here to run everytime

    logger.info(f"Received advance request data {data}")

    status = "accept"
    try:
        payload = hex2str(data["payload"])
    
        cur = con.cursor()

        cur.execute(INSERT_SQL,(data['payload'],
        data["metadata"]["msg_sender"],
        data["metadata"]["input_index"],
        data["metadata"]["epoch_index"],
        data["metadata"]["timestamp"]))

        con.commit()
        # logger.info(type(payload['payload']))
        # logger.info(payload['payload'])
        logger.info(type(data["payload"]))
        logger.info(type(data["metadata"]["msg_sender"]))
        #input, epoch, created_at)


        logger.info("Adding notice")
        #store data - payload is what is being sent on input
        
        logger.info(f"payload {data['payload']}")
        logger.info(f"hex2str {hex2str(data['payload'])}")
        input_string = hex2str(data['payload'])
        json_object = json.loads(input_string)
        logger.info(json_object)

       # json_object = json.loads(test_json)

        receiver = None
        sender = None

        if(json_object['type'] == "friend_request"):
            receiver = json_object['friend_username']
            sender = json_object['username']
            if receiver not in list_of_users:
                list_of_users.append(receiver)
            if sender not in list_of_users:
                list_of_users.append(sender)
            logger.info(f'list of users:{list_of_users}')

            #sender = list_of_users[get_user_with_username(json_object['username'])]
            if status == "accept":
                #create a notice with json output
                logger.info(f'{sender} and {receiver} are now friends')
                logger.info(f'{receiver} has accepted {sender} request ')
        

        #output 
        #convert string to hex
        message_return = (f'{receiver} has accepted {sender} request ')
        response = requests.post(rollup_server + "/notice", json={"payload": str2hex(message_return)})
        
        #convert to hex to string to json and then process

        logger.info(f"Received notice status {response.status_code} body {response.content}")

    except Exception as e:
        status = "reject"
        msg = f"Error processing data {data}\n{traceback.format_exc()}"
        logger.error(msg)
        response = requests.post(rollup_server + "/report", json={"payload": str2hex(msg)})
        logger.info(f"Received report status {response.status_code} body {response.content}")

    return status

def handle_inspect(data):
    logger.info(f"Received inspect request data {data}")
    logger.info("Adding report")
    response = requests.post(rollup_server + "/report", json={"payload": data["payload"]})
    logger.info(f"Received report status {response.status_code}")
    return "accept"

handlers = {
    "advance_state": handle_advance,
    "inspect_state": handle_inspect,
}

init_db()

finish = {"status": "accept"}
rollup_address = None #sender metadata = data["metadata"]["msg_sender"]
reciever = None # from payload


while True:
    logger.info("Sending finish")
    response = requests.post(rollup_server + "/finish", json=finish)
    logger.info(f"Received finish status {response.status_code}")
    if response.status_code == 202:
        logger.info("No pending rollup request, trying again")
    else:
        rollup_request = response.json()
        data = rollup_request["data"]
        if "metadata" in data:
            metadata = data["metadata"]
            if metadata["epoch_index"] == 0 and metadata["input_index"] == 0:
                rollup_address = metadata["msg_sender"]
                logger.info(f"Captured rollup address: {rollup_address}")
                continue
        handler = handlers[rollup_request["request_type"]]
        finish["status"] = handler(rollup_request["data"])
