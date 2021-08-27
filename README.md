# Python Morning Mailer
This is a simple python script I created for a company to assist in automating send out emails for work order status updates in association with a web application called Property Preservation Wizard (PPW).

## Executable
This can be created in a .EXE program. I used pyinstaller to do this.

    pyinstaller --onefile -w main-2.py

## Configuration
The configuration for this program is embedded in the program as this was meant to be distributed to employees of the company.

Line 12:
You can place names into this array and the program will skip emailing this vendor. For example:

    contractor_blacklist  = ['Doe, John', 'Doe, Jane']

Line 33:
Use this line to place the direct readable link to a json file containing your vendors and their email. For example:

    {
	    "Worksheet":  [
		    {
			    "Name":  "Doe, John",
			    "Email":  "example@example.com"
		    },
		]
	}

Line 50: Email subject.
Lines 53 & 64: Your email address.
Line 62: Your email address and password.
Line 82: The plaintext version of your email.
Line 86: The HTML version of your email.

## Instructions
1. Select the work orders you need a status on and export them to an excel sheet from PPW.
2. Open the excel sheet and delete all columns except (they should be in this order): WO #, Date Due, Client, Address, Contractor
3. In the top left, click File -> Save As -> Browse. For the "Save as type", make sure you have "CSV (Comma delimited)" selected and save the file wherever you want.
4. Open the program/run the script and select the CSV file that you just saved.
5. Give the program a minute to send the emails. The program will automatically close when it is done.

The program creates a log file named "email_log_(TODAYS DATE)". You can open it and check that all of the emails were sent successfully or unsuccessfully.
