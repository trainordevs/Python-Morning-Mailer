import smtplib, ssl, csv, sys, json, logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from urllib.request import urlopen 
from datetime import date

orders = {}
contractors = {}
## You can input names (as a string) here so that the program automatically skips these contractors.
contractor_blacklist = []

logging.basicConfig(filename="email_log_{d}".format(d = date.today()), filemode='a', format='%(asctime)s | %(levelname)s | %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)

def send_email(csv_file, plaintext, html):
    if not csv_file:
        messagebox.showerror("No file selected.", "The program will now exit as you did not select a CSV file.")
        sys.exit()
    
    with open(csv_file, 'r', encoding='utf8') as file:
        reader = csv.reader(file)

        col_count = len(next(reader))
        if col_count != 5:
            messagebox.showerror("Failed to Load CSV", "Your CSV should only have 5 columns: WO #, Date Due, Client, Address, Contractor")
            sys.exit()

        for wo_num, date_due, client, address, contractor in reader:
            if contractor not in contractor_blacklist:
                if contractor in orders:
                    orders[contractor].append([wo_num, date_due, client, address])
                else:
                    orders[contractor] = [[wo_num, date_due, client, address]]
    
    ## This is where the URL for a json file containing contractors and their emails.
    response = urlopen("")
    data = json.loads(response.read())

    for i in data['Worksheet']:
        if i['Name'] not in contractors:
            name = i['Name']
            contractors[name] = i['Email']
    
    for order in orders:
        work = ""

        for wo in orders[order]:
            work += "<tr><td>" + wo[0] + "</td><td>" + wo[1] + "</td><td>" + wo[3] + "</td></tr>"

        email = contractors[order]
        
        message = MIMEMultipart("alternative")
        ## Email subject.
        message["Subject"] = ""
        ## Your email account.
        message["From"] = ""
        message["To"] = email
        message.attach(plaintext)
        message.attach(html)
        context = ssl.create_default_context()

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                ## Your email account and password.
                server.login("", "")
                server.sendmail(
                    ## Your email account.
                    "",
                    email,
                    message.as_string().format(
                        work=work
                    )
                )
                logging.info("{contractor}: Successful.".format(contractor = order))
                server.quit()
        except:
            logging.error("{contractor}: Unsuccessful.".format(contractor = order))
        
        email = ""
        message["To"] = ""

#######################################

def main():
    ## Your email in plaintext.
    plaintext = MIMEText("""\
        """, "plain")

    ## Your email in HTML.
    html = MIMEText("""\
        """, "html")

    send_email(askopenfilename(), plaintext, html)

if __name__ == '__main__':
    main()
