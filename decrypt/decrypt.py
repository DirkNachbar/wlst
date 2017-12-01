#/bin/python
#=====================================================================
#
# $Id: decrypt.py $
#
# PURPOSE:    Script to decrypt any Password or Username 
#             within a WebLogic Server Domain
#
# PARAMETERS: none
#
# NOTES:      none
#
# AUTHOR:     Dirk Nachbar, https://dirknachbar.blogspot.com
#
# MODIFIED:
#
#
#=====================================================================
 
# Import weblogic.security.internal and weblogic.security.internal.encryption
from weblogic.security.internal import *
from weblogic.security.internal.encryption import *
 
# Provide Domain Home Location
domain = raw_input("Provide Domain Home location: ")
 
# Get encryption service with above Domain Home Location
encryptService = SerializedSystemIni.getEncryptionService(domain)
clearOrEncryptService = ClearOrEncryptedService(encryptService)
 
# Provide the encrypted password or username, e.g. from boot.properties
encrypted_pwd = raw_input("Provide encrypted password or username (e.g.: {AES}jNdVLr...): ")
 
# Clear the encrypted value from escaping characters
cleared_pwd = encrypted_pwd.replace("\\", "")
 
# Personal security hint :-)
raw_input("Make sure that nobody is staying behind you :-) Press ENTER to see the password ...")
 
# Decrypt the encrypted password or username
print "Value in cleartext is: " + clearOrEncryptService.decrypt(cleared_pwd)

