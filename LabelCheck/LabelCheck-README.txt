***CAUTION: ALL THE .txt FILES MUST FOLLOW THE FILE NAMING FORMAT
SUCH AS 'w01A01.txt'. THE CONTENT WITHIN THE .txt FILES MUST ALSO BE 
CORRECTLY FORMATTED TO AVOID CRASHING OR UNWANTED RESULTS***

'LabelCheck.py' is designed to go through all the label files within
the folder were the Python script is loacted. The script reviews all the
labels in each .txt file and ensures that they are one of the following:

	RAQ	TA	TA-Q:
	TAQ:	ST	G	
	MS	ST-Q	STO

If the program finds label that does not match any of the above then it will
mark as an error. All errors found will be compiled and formatted into
a new file called 'LabelCheck.csv'. 

TO RUN THE SCRIPT OPEN THE PYTHON FILE IN IDLE AND PRESS F5. ONCE IT IS
RUNNING IN THE SHELL TYPE 'main()' AND PRESS ENTER.