import paramiko
import time
import urllib.request
import os



def main():
    #function for calling the different test functions
    print("Choose your sub program:\n"
          "1 for testing point to point call with manual input \n"
          )
    prog = input("Your choice: ")
    if prog == "1":
        test_call()
    elif prog == "7":
        test_version()
    else:
        cls()
        main()

def cls():
    #function for clearing the screen for better overview
    os.system('cls' if os.name=='nt' else 'clear')

def test_call():
    host = input("IP Address of endpoint: ")
    username = input("User name: ")
    password = input("Password: ")
    destination = input("Call destination: ")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=22,  look_for_keys=False, allow_agent=False)
    client_shell = client.invoke_shell()
    client_shell.recv(1024)
    time.sleep(2)
    client_shell.send("xcommand Dial Number:"+destination+"\n")
    time.sleep(4)
    #
    # Module for Authentication on TC based endpoint based on the credentials insert earlier
    #
    loginmanager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    # this creates a password manager
    endpointurl = 'http://'+host+'/getxml?location=/Status/Call'
    #creates endpoint URL based on earlier provided host IP
    loginmanager.add_password(None, endpointurl, username, password)
    # because we have put None at the start it will always
    # use this username/password combination forÂ Â urls
    # for which `theurl` is a super-url
    authhandler = urllib.request.HTTPBasicAuthHandler(loginmanager)
    # create the AuthHandler
    opener = urllib.request.build_opener(authhandler)
    urllib.request.install_opener(opener)
    responseString = urllib.request.urlopen(endpointurl).read().decode("utf-8")
    # makes the XML request from endpoint for
    print(responseString)
    time.sleep(2)
    client_shell.send("xcommand call disconnectall\n")
    client.close()
    time.sleep(2)
    cls()
    return main()


main()