***CAUTION: ALL THE .txt FILES MUST FOLLOW THE FILE NAMING FORMAT
SUCH AS 'w01A01.txt'. THE CONTENT WITHIN THE .txt FILES MUST ALSO BE 
CORRECTLY FORMATTED TO AVOID CRASHING OR UNWANTED RESULTS***

'Scott.py' is designed to go through all the label files within
the folder where the Python script is located. The program focuses on the
events that occurs after any TAQ. Once locating a TAQ the program continues
to search for any space or overlap between labels. If it finds any then it
add the line after the mistake onto the 'Scott.csv'. Always look before
and after the line included on the csv for the mistake. NOTE: This program
was designed mainly in cases where the .txt file was not completely labeled.
The program is meant to ensure that every TAQ has events following it until
the next TA event. 

For example:

25.035092	27.409110	TAQ: Do you has a confusion?
27.409110	28.071713	G 
28.071713	29.558527	ST 
29.558527	29.558527	G 
50.558527	79.787015	TAQ: What is love? 

From the example above 'Scott.py' would register an error for line:

	50.558527	79.787015	TAQ: What is love?

The reason for this is that for the first TAQ everything was okay until
the second G. At that point there is a jump from 29.558527 seconds to 
50.558527 seconds.

TO RUN THE SCRIPT OPEN THE PYTHON FILE IN IDLE AND PRESS F5. ONCE IT IS
RUNNING IN THE SHELL TYPE 'main()' AND PRESS ENTER.