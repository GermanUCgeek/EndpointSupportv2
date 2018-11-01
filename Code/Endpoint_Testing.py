import paramiko
import time
import urllib.request
import os
import csv

def main():
    # asking for CSV file import for IP address batch job

    # function for calling the different test functions
    print("Choose your sub program:\n"
        "1 for testing point to point call with manual input \n"
        "2 for testing point to point call with CSV import \n"
        )
    prog = input("Your choice: ")
    if prog == "1":
        epOS = []
        user = []
        eppw = []
        endpoint = []
        user.append(input("Insert admin user:"))
        eppw.append(input("Insert admin password:"))
        endpoint.append(input("Insert Endpoint IP:"))
        epOS.append(input("Insert endpoint OS (TC,CTS):"))
        print(epOS[0])
        test_call(user,eppw,endpoint,epOS)
    elif prog == "2":
        csv_import()
    else:
        cls()
        main()


def cls():
    # function for clearing the screen for better overview
    os.system('cls' if os.name == 'nt' else 'clear')


def test_call(usernames,passwords,hosts,typeOS):
    #Test call module with the commands for the different kind of endpoints
    try:
        destination = input("Call destination: ")
        for i, host in enumerate(hosts):
            if typeOS[i] == 'TC':
                username=usernames[i]
                password=passwords[i]
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(hostname=host, username=username, password=password, port=22, look_for_keys=False,
                               allow_agent=False)
                client_shell = client.invoke_shell()
                client_shell.recv(1024)
                time.sleep(2)
                client_shell.send("xcommand Dial Number:" + destination + "\n")
                time.sleep(4)
                #
                # Module for Authentication on TC based endpoint based on the credentials insert earlier
                #
                loginmanager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
                # this creates a password manager
                endpointurl = 'http://' + host + '/getxml?location=/Status/Call'
                # creates endpoint URL based on earlier provided host IP
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
            elif typeOS[i] == 'CTS':
                username=usernames[i]
                password=passwords[i]
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(hostname=host, username=username, password=password, port=22, look_for_keys=False,
                               allow_agent=False)
                client_shell = client.invoke_shell()
                client_shell.recv(1024)
                time.sleep(2)
                client_shell.send("call start" + destination + "\n")
                time.sleep(10)
                client_shell.send("show call status \n")
                time.sleep(2)
                client_shell.send("call end \n")
            elif typeOS[i] == 'IX':
                username=usernames[i]
                password=passwords[i]
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(hostname=host, username=username, password=password, port=22, look_for_keys=False,
                               allow_agent=False)
                client_shell = client.invoke_shell()
                client_shell.recv(1024)
                time.sleep(2)
                client_shell.send("call start" + destination + "\n")
                time.sleep(10)
                client_shell.send("show call status \n")
                time.sleep(2)
                client_shell.send("call end \n")
            elif typeOS[i] == 'CE':
                username=usernames[i]
                password=passwords[i]
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(hostname=host, username=username, password=password, port=22, look_for_keys=False,
                               allow_agent=False)
                client_shell = client.invoke_shell()
                client_shell.recv(1024)
                time.sleep(2)
                client_shell.send("xcommand Dial Number:" + destination + "\n")
                time.sleep(4)
                #
                # Module for Authentication on CE based endpoint based on the credentials insert earlier
                #
                loginmanager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
                # this creates a password manager
                endpointurl = 'http://' + host + '/getxml?location=/Status/Call'
                # creates endpoint URL based on earlier provided host IP
                loginmanager.add_password(None, endpointurl, username, password)
                # because we have put None at the start it will always
                # use this username/password combination for urls
                # for which `theurl` is a super-url
                authhandler = urllib.request.HTTPBasicAuthHandler(loginmanager)
                # create the AuthHandler
                opener = urllib.request.build_opener(authhandler)
                urllib.request.install_opener(opener)
                responseString = urllib.request.urlopen(endpointurl).read().decode("utf-8")
                # makes the XML request from endpoint for
                print(responseString)
                time.sleep(2)
                client_shell.send("xcommand call disconnect\n")
                client.close()
                time.sleep(2)
                cls()
            else:
                print("Invalid Entry in CSV File for TypeSelect")
        return main()

    except TimeoutError as err:
        print('SSH connection error, please check entered information\n', err)
        main()


def csv_import():
    with open('Endpunkte.csv',) as csvfile:
        csv.register_dialect('endpunktliste', delimiter=';', quoting=csv.QUOTE_NONE)
        reader = csv.DictReader(csvfile,dialect='endpunktliste')
        return ImportEndpoints(reader)


def ImportEndpoints(CSVImport):
    hostsEP=[]
    userTC=[]
    PasswordTC=[]
    TypeEP=[]
    for row in CSVImport:
        if row['Status'] == 'active':
            hostsEP.append(row['real IP'])
            userTC.append(row['Username'])
            PasswordTC.append(row['Password'])
            TypeEP.append(row['TypeSelect'])
    return test_call(userTC,PasswordTC,hostsEP,TypeEP)

main()
