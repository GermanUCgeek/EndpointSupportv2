import paramiko
import time
import urllib.request
import os
import csv

def main():
    # asking for CSV file import for IP address batch job
    print("You want to use a CSV file for IP address import Import?")
    csv_select = input("Your Choice (yes/no): ")
    if csv_select == "yes":
        csv_import()
    else:
        # function for calling the different test functions
        print("Choose your sub program:\n"
              "1 for testing point to point call with manual input \n"
              )
        prog = input("Your choice: ")
        if prog == "1":
            user=input("Insert admin user:")
            eppw=input("Insert admin password:")
            endpoint=input("Insert Endpoint IP:")
            epOS=input("Insert endpoint OS (TC,CTS):")
            print(epOS[1])
            test_call(user,eppw,endpoint,epOS)
        else:
            cls()
            main()


def cls():
    # function for clearing the screen for better overview
    os.system('cls' if os.name == 'nt' else 'clear')


def test_call(usernames,passwords,hosts,typeOS):
    try:
        destination = input("Call destination: ")
        print(typeOS)
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
            else:
                print("Invalid Entry in CSV File for TypeSelect")
        return main()

    except TimeoutError as err:
        print('SSH connection error, please check entered information\n', err)
        test_call()


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
