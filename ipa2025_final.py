#######################################################################################
# Yourname: Alisala Tunleng
# Your student ID: 66070221
# Your GitHub Repo: https://github.com/ayyaya21/IPA2025-Final.git

#######################################################################################
# 1. Import libraries for API requests, JSON formatting, time, os, (restconf_final or netconf_final), netmiko_final, and ansible_final.

from restconf_final import *
from netconf_final import *
# from netmiko_final import gigabit_status
# from ansible_final import showrun
import os
import time
from dotenv import load_dotenv
from requests_toolbelt import MultipartEncoder
load_dotenv()

#######################################################################################
# 2. Assign the Webex access token to the variable ACCESS_TOKEN using environment variables.

ACCESS_TOKEN = os.getenv("WEBEX_TOKEN")

#######################################################################################
# 3. Prepare parameters get the latest message for messages API.

# Defines a variable that will hold the roomId
roomIdToGetMessages = (
    "Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vYmQwODczMTAtNmMyNi0xMWYwLWE1MWMtNzkzZDM2ZjZjM2Zm"
)

method = ""

while True:
    # always add 1 second of delay to the loop to not go over a rate limit of API calls
    time.sleep(1)

    # the Webex Teams GET parameters
    #  "roomId" is the ID of the selected room
    #  "max": 1  limits to get only the very last message in the room
    getParameters = {"roomId": roomIdToGetMessages, "max": 1}

    # the Webex Teams HTTP header, including the Authoriztion
    getHTTPHeader = {"Authorization": 'Bearer ' +  ACCESS_TOKEN, "Accept": "application/json"}

# 4. Provide the URL to the Webex Teams messages API, and extract location from the received message.
    
    # Send a GET request to the Webex Teams messages API.
    # - Use the GetParameters to get only the latest message.
    # - Store the message in the "r" variable.
    r = requests.get(
        "https://webexapis.com/v1/messages",
        params=getParameters,
        headers=getHTTPHeader,
    )
    # verify if the retuned HTTP status code is 200/OK
    if not r.status_code == 200:
        raise Exception(
            "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
        )

    # get the JSON formatted returned data
    json_data = r.json()

    # check if there are any messages in the "items" array
    if len(json_data["items"]) == 0:
        raise Exception("There are no messages in the room.")

    # store the array of messages
    messages = json_data["items"]
    
    # store the text of the first message in the array
    message = messages[0]["text"]

    isEnd = False
    # check if the text of the message starts with the magic character "/" followed by your studentID and a space and followed by a command name
    #  e.g.  "/66070123 create"
    if message.startswith("/66070221"):
        print("Received message: " + message)
        option = message.split()[1]
        if option == "restconf":
            method = 'restconf'
            responseMessage = "Ok: Restconf"
            isEnd = True
        elif option == "netconf":
            method = 'netconf'
            responseMessage = "Ok: Netconf"
            isEnd = True
        elif not method:
            responseMessage = "Error: No method specified"
            isEnd = True
        elif (option != "restconf" or option != "netconf") and method != "":
            if option == "10.0.15.61" and len(message.split()) < 3:
                responseMessage = "Error: No command found"
                isEnd = True
            if option != "10.0.15.61":
                responseMessage = "Error: No IP specified"
                isEnd = True

        # 5. Complete the logic for each command
        if not isEnd and method == 'restconf':
            command = message.split()[2]
            if command == "create":
                responseMessage = rest_create()
            elif command == "delete":
                responseMessage = rest_delete()
            elif command == "enable":
                responseMessage = rest_enable()
            elif command == "disable":
                responseMessage = rest_disable()
            elif command == "status":
                responseMessage = rest_status()
            # elif command == "gigabit_status":
            #     responseMessage = gigabit_status()
            # elif command == "showrun":
            #     responseMessage = showrun()
            else:
                responseMessage = "Error: No command or unknown command"   
 
        elif not isEnd and method == 'netconf':
            command = message.split()[2]
            if command == "create":
                responseMessage = net_create()
            elif command == "delete":
                responseMessage = net_delete()
            elif command == "enable":
                responseMessage = net_enable()
            elif command == "disable":
                responseMessage = net_disable()
            elif command == "status":
                responseMessage = net_status()
            # elif command == "gigabit_status":
            #     responseMessage = gigabit_status()
            # elif command == "showrun":
            #     responseMessage = showrun()
            else:
                responseMessage = "Error: No command or unknown command"
        
        # 6. Complete the code to post the message to the Webex Teams room.

        # The Webex Teams POST JSON data for command showrun
        # - "roomId" is is ID of the selected room
        # - "text": is always "show running config"
        # - "files": is a tuple of filename, fileobject, and filetype.

        # the Webex Teams HTTP headers, including the Authoriztion and Content-Type
        
        # Prepare postData and HTTPHeaders for command showrun
        # Need to attach file if responseMessage is 'ok'; 
        # Read Send a Message with Attachments Local File Attachments
        # https://developer.webex.com/docs/basics for more detail

        if option == "showrun" and responseMessage != "Error: Ansible":
            pass
            # filename = responseMessage
            # fileobject = open(filename, "rb")
            # filetype = "text/plain"

            # postData = MultipartEncoder(
            #     fields={
            #         "roomId": roomIdToGetMessages,
            #         "text": "show running config",
            #         "files": (filename, fileobject, filetype)
            #     }
            # )
            # HTTPHeaders = {
            # "Authorization": 'Bearer ' + ACCESS_TOKEN,
            # "Content-Type": postData.content_type,
            # }
        # other commands only send text, or no attached file.
        else:
            postData = {"roomId": roomIdToGetMessages, "text": responseMessage}
            postData = json.dumps(postData)

            # the Webex Teams HTTP headers, including the Authoriztion and Content-Type
            HTTPHeaders = {"Authorization": 'Bearer ' + ACCESS_TOKEN, "Content-Type": "application/json"}   

        # Post the call to the Webex Teams message API.
        r = requests.post(
            "https://webexapis.com/v1/messages",
            data=postData,
            headers=HTTPHeaders,
        )
        if not r.status_code == 200:
            raise Exception(
                "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
            )
