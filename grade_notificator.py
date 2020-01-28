import requests
import smtplib
import time

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tabulate import tabulate
from bs4 import BeautifulSoup as bs
from copy import deepcopy

# Login data to change
wwsi_login = 'your_login'
wwsi_password = 'your_password'

source_email = 'you_source_email@gmail.com'
source_password = 'your_password'

target_email = 'your_target_email@gmail.com'

check_every_x_minutes = 5

def send_mail(source_email, source_password, target_email, table):
    """
    Sends mail with message from source_mail to target_email
    Source mail must be gmail account
    Input:
        source_email, source_password - login and password for source account
        target_email - email that message should be send to
        table - table with data
    """
    # Create server
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    # Connect to server
    server.ehlo()
    server.connect('smtp.gmail.com', 465)
    server.ehlo()
    # Login
    server.login(source_email, source_password)
    # Content of message
    text = "WWSI Grade Notificator has detected changes in your grades:\n{table}"
    text = text.format(table=tabulate(table, headers="firstrow", tablefmt="grid"))
    msg = MIMEMultipart("alternative", None, [MIMEText(text)])
    msg['Subject'] = "WWSI grade changed"
    # Send the mail
    server.sendmail(source_email, target_email, msg.as_string())
    server.quit()


def get_grades(wwsi_login, wwsi_password):
    """
    Get grades and headers from wwsi grades website
    Input:
        wwsi_login, wwsi_password - login and password for wwsi account
    Output:
        headers - list of headers for every column
        grades - list of lists with every data of every subject
    """
    s = requests.Session()
    url = 'https://student.wwsi.edu.pl/oceny'
    data = {
        'login': wwsi_login,
        'password': wwsi_password,
        'login_send': 'send'
        }

    r = s.post(url, data=data)
    soup = bs(r.text, 'html.parser')

    headers = soup.find("tr")
    headers = headers.text.split(" ")
    # Remove empty elements from list
    headers.remove("")
    headers.remove("")

    grades = soup.find_all("td")

    data = []
    for row in range(0, len(grades), len(headers)):
        data.append([])
        for i in range(len(headers)):
            data[int(row/len(headers))].append(grades[row+i].text)

    headers = [''] + headers
    return headers, data

# Main function
if __name__ == "__main__":
    headers, grades = get_grades(wwsi_login, wwsi_password) # Inital load of grades
    while True:
        # Get new grades
        old_grades = deepcopy(grades)
        success = False
        while not success:
            try:
                headers, grades = get_grades(wwsi_login, wwsi_password)
                success = True
            except:
                print("WWSI connect error")
                time.sleep(1)
    
        if old_grades != grades:
            # Create table
            changed_grades = []
            for num in range(len(grades)):
                if old_grades[num] != grades[num]:
                    changed_grades.append((old_grades[num], grades[num]))
                msg = []
                msg.append(headers)
                for changes in changed_grades:
                    msg.append(['NEW'] + changes[0])
                    msg.append(['OLD'] + changes[1])
            # Send table
            success = False
            while not success:
                try:
                    send_mail(source_email, source_password, target_email, msg)
                    print('New grades sent')
                    success = True
                except:
                    print('GMAIL connect error')
                    time.sleep(1)
        else:
            print(time.strftime("%H:%M:%S", time.localtime()), '   No new grades')

        time.sleep(check_every_x_minutes*60)
