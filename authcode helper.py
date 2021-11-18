#encodes and decodes base64 strings, native to python
import base64

#This code will give you the base-64 encoded string needed for html request headers

#set up your authorization variables
accountsid = ""
token = ""

#converts your authorization details to utf-8 if they are not already
accountsidbyte = accountsid.encode('utf-8')
tokenbyte = token.encode('utf-8')

#just a helper character used to get the proper authentication header
helper = ":"
helperbyte = helper.encode('utf-8')

#combines your authentication details into a string
authcode = accountsidbyte+helperbyte+tokenbyte
#encodes this string to base64
authcode = base64.b64encode(authcode)
#decodes base64 to format appropriate for a header
authcode = authcode.decode()
#prints code to console for copy/paste, or return this variable in a larger project
print(authcode)