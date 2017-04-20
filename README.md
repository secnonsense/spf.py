# spf.py
Python Script for Digging into a domain's SPF records

Anyone who has worked with anti-spam products knows the pain of dealing with anti-spoofing policies and running dig TXT commands through layers and layers of includes in SPF records.  This simple script automates that process.  Only ip4 and 1pv6 addresses, includes and a records associated with mx records are processed at this time.
