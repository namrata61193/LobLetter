import requests
import json
import pprint
import lob
import urllib2
import sys

lob.api_key = 'test_dda622147a74e452b39c364301afe4f2d06'
lob.api_version = '2016-01-19'


def download_file(download_url):
    response = urllib2.urlopen(download_url)
    file = open("Letter.pdf", 'w')
    file.write(response.read())
    file.close()
    print("Completed")


def create_address(receiver_name, receiver_line1, receiver_line2, receiver_city, receiver_state, sender_country,receiver_zipCode):
	"""Use the LOB Api and the given address to create the address in LOB's required format"""
	try:
		address = lob.Address.create(
		name = receiver_name,
		address_line1 = receiver_line1,
		address_line2 = receiver_line2,
		address_city = receiver_city,
		address_state = receiver_state,
		address_country = sender_country,
		address_zip = receiver_zipCode)
	except Exception, e:
		print str(e)
		sys.exit()
  	else:
  		return address
	

def verify_address(sender_address_line1, sender_address_line2, sender_city, sender_state, sender_zipcode , sender_country):
	"""Use the LOB Api and the sender's address to verify if the input address is valid"""
	try:
		verified_address = lob.Verification.create(
		address_line1 = sender_address_line1,
		address_line2 = sender_address_line2,
		address_city = sender_city,
		address_state = sender_state,
		address_zip = sender_zipcode,
		address_country = sender_country)
	except Exception, e:
		print str(e)
		sys.exit()
  	else:
  		return verified_address


def create_letter(from_address, to_address, data):
	"""Use the LOB Api,sender's address,receiver's address and some html to create a new letter"""
	try:
		example_letter = lob.Letter.create(
	    description = 'Letter to Legislature',
	    to_address = to_address,
	    from_address = from_address,
	    file = """
	      <html>
	<head>
	<link href='https://fonts.googleapis.com/css?family=Open+Sans' rel='stylesheet' type='text/css'>
	<title>Lob.com Sample Letter Template = true</title>
	<style>
	  *, *:before, *:after {
	    -webkit-box-sizing: border-box;
	    -moz-box-sizing: border-box;
	    box-sizing: border-box;
	  }

	  body {
	    width: 8.5in;
	    height: 11in;
	    margin: 0;
	    padding: 0;
	  }

	  .page {
	    page-break-after: always;
	  }

	  .page-content {
	    position: relative;
	    width: 8.125in;
	    height: 10.625in;
	    left: 0.1875in;
	    top: 0.1875in;
	    background-color: rgba(255,0,255,0.3);
	  }

	  .text {
	    position: relative;
	    left: 20px;
	    top: 20px;
	    width: 6in;
	    font-family: sans-serif;
	    font-size: 30px;
	    top: 3in;
	  }

	  #return-address-window {
	    position: absolute;
	    left: .625in;
	    top: .5in;
	    width: 3.25in;
	    height: .800in;
	    background-color: rgba(255,255,255,1);
	  }

	  #return-address-text {
	    position: absolute;
	    left: .07in;
	    top: .25in;
	    width: 2.05in;
	    height: .5in;
	    background-color: rgba(255,255,255,1);
	    font-size: .11in;
	  }

	  #return-logo {
	    position: absolute;
	    left: .07in;
	    top: .02in;
	    width: 2.05in;
	    height: .3in;
	    background-color: white;
	  }

	  #recipient-address-window {
	    position: absolute;
	    left: .625in;
	    top: 1.75in;
	    width: 3.25in;
	    height: 1in;
	    background-color: rgba(255,255,255,1);
	  }

	  #recipient-address-text {
	    position: absolute;
	    left: .07in;
	    top: .05in;
	    width: 2.92in;
	    height: .9in;
	    background-color: rgba(255,255,255,1);
	  }

	</style>
	</head>

	<body>
	  <div class="page">
	    <div class="page-content">
	      <div class="text">
	      	{{text}}
	      </div>
	    </div>
	    <div id="return-address-window">
	      <div id="return-address-text">
	      </div>
	    </div>
	    <div id="recipient-address-window">
	      <div id="recipient-address-text">
	      </div>
	    </div>
	  </div>
	</body>

	</html>
	      """,
	    data = {
	        'text':data
	    },
	    color = True
		)
	except Exception, e:
		print str(e)
		sys.exit()
  	else:
  		return example_letter
	
def main():
	#get sender's address from the user. Continue to request for address till it is valid.
	sender_name = raw_input('Please enter your name: ')
	sender_address_line1 = raw_input('Please enter Line1 of your address: ')
	sender_address_line2 = raw_input('Please enter Line2 of your address: ')
	sender_city = raw_input('Please enter your city: ')
	sender_state = raw_input('Please enter your state: ')
	sender_country = raw_input('Please enter your country: ')
	sender_zipcode = raw_input('Please enter your zipcode: ')

	verified_address = verify_address(sender_address_line1, sender_address_line2, sender_city, sender_state, sender_zipcode , sender_country)
	sender_address = verified_address.address.address_line1 
	sender_address += verified_address.address.address_line2 
	sender_address += verified_address.address.address_city 
	sender_address += verified_address.address.address_state
	sender_address += verified_address.address.address_zip

	#Google Representative Info by Address API CALL
	url = 'https://www.googleapis.com/civicinfo/v2/representatives?address='+sender_address+'&levels=administrativeArea1&key=AIzaSyBuVrQd-oZ_lvNXl5g0rBdiCysFflB2uRo'
	response = requests.get(url)
	#check if the response is valid
	if response.status_code != 200:
		error = json.loads(response.text)
		try:
			errors = error['error']
			print errors['message']
			sys.exit()
		except Exception, e:
			print str(e)
			sys.exit()


	data = json.loads(response.text)
	#fetch the receiver's address from the response. Break in case the official for that area doesnt exist. 
	try:
		official = data['officials'][0]
		receiver_address = official['address'][0]
		receiver_name = official['name']
		receiver_line1 = receiver_address['line1']
		try:
			receiver_line2 = receiver_address['line2']
		except:
			receiver_line2 = ""
		receiver_city = receiver_address['city']
		receiver_state = receiver_address['state']
		receiver_zipCode = receiver_address['zip']
	except Exception, e:
		print "Invalid Receiver's Address"
		sys.exit()
	
	from_address = create_address(sender_name,verified_address.address.address_line1,verified_address.address.address_line2,verified_address.address.address_city,verified_address.address.address_state,sender_country,verified_address.address.address_zip)
	to_address = create_address(receiver_name, receiver_line1, receiver_line2, receiver_city, receiver_state, sender_country,receiver_zipCode)
	data = raw_input('Please enter your message: ')
	example_letter = create_letter(from_address, to_address, data)
	#print the final URL for the letter
	print example_letter['url']
	#download the letter into current directory
	download_file(example_letter['url'])

if __name__ == "__main__":
    main()



