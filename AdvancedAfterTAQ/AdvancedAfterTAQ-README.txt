***CAUTION: ALL THE .txt FILES MUST HAVE FOLLOW THE FILE NAMING FORMAT
SUCH AS 'w01A01.txt'. THE CONTENT WITHIN THE .txt FILES MUST ALSO BE 
CORRECTLY FORMATTED TO AVOID CRASHING OR UNWANTED RESULTS***

'AdvancedAfterTAQ.py' is designed to go through all the label files within
the folder where the Python script is located. IT MUST ALSO HAVE A .csv FILE
NAMED 'CodeToQuestion' CONTAINING THE QUESTIONS AND THEIR CORRESPONDING CODE.
The program will output 3 differente .csv files. They are as follows:

'AdvancedAfterTAQ.csv'
	The file contains weeks 1-10 and sections B, C, and E. For each 
	recitation there is a subcategory of 'Code' such as kb. The 
	csv will also include the time length of:
		Wait Time 1 - The gap length after a TAQ
		Wait Time 2 - the gap length after a student event
		Student     - the length of any student event after a TAQ
	The csv will include the count of:
		Wait Time 1 - the gap immediately following the TAQ
		Wait Time 2 - the gap immediately following a student event
		Student     - if the TAQ received 1 > student event
		TA	    - if the TAQ did not receive a student event

'Uncoded.csv'
	The file contains all the questions that could not be found within
	the 'CodeToQuestion.csv'. NOTE: Event the slightest change in the
	text of the question such as an extra space could make a question
	unidentifiable.

'Undetermined.csv'
	The file contains all the questions that were trimmed from the end
	of a text file. This occurs when there is a TAQ but the file ends
	before the it can reach the next TA event.

TO RUN THE SCRIPT OPEN THE PYTHON FILE IN IDLE AND PRESS F5. ONCE IT IS
RUNNING IN THE SHELL TYPE 'main()' AND PRESS ENTER.