This application is a simple command line interface which asks the user for his name,address and message. 
It will then get the receiver's address using the Google Civic Information API. For this application it will fetch the first officer at the administrative level. 
Finally using Lob API, the application will create a letter and print out the URL of the PDF link of the letter. It will also download the letter into the current directory. 

To run :

	python Lob.py

Resources Used:
1. https://developers.google.com/civic-information/docs/v2/representatives/representativeInfoByAddress
2. https://lob.com/docs/python#letters
3. https://lob.com/docs#html-examples ( I used some of the Lob styling provided to create the HTML of the letter)

P.S : The version of Python I am using is 2.7.10. I also used the Test API Keys.