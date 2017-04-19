#!/usr/bin/python

#uses dnspython - http://www.dnspython.org/
import sys, re, dns.resolver

x = y = 0
spf = []
lspf = []
lookup = []
mxlookup = []

#First Lookup of Domain Passed as Argument - Added to lookup list
lookup.append("mailgun.com")

#Primary Loop for processing initial DNS lookup and itterating through includes
while lookup:
#Choose Record type of lookup - A for MX Records and TXT for SPF
    if lookup[y] in mxlookup:
        Q = "A"
    else:
        Q = "TXT"
#DNS query and print domain name being processed
    answers = dns.resolver.query(lookup[y], Q)
    print "\ndomain block:  " + lookup[y] + "\n"

    for server in answers:
        lspf = re.split('\s', str(server))
        spf = [s.strip('"') for s in lspf]
        print '\n' + Q + ' Record: ' + ' '.join(spf) + '\n'
#Loop to look at all elements of the returned record
        for i in range(0, len(spf)):
            if spf[0] != 'v=spf1' and Q != "A":
                print "No spf\n"
#Add includes to lookup for further processing and increment counter
            elif "include" in spf[i]:
                inc = spf[i].split(":")
                lookup.append(inc[1])
                x = x+1
#Add MX "A" records to lookup and mxlookup so their query can be handled properly
            elif spf[i] == "a":
                lookup.append(spf[i+1])
                mxlookup.append(spf[i+1])
                x = x+1
#Print the IPv4 addresses in an easily copiable block
            elif "ip4:" in spf[i]:
                ip = spf[i].split(":")
                print ip[1]
            elif "ip6:" in spf[i]:
                ip6 = spf[i]
                print ip6[4:]
            elif Q == "A":
                print spf[i]
#Counter to be sure we don't loop beyond the end of the lookup list
    y = y+1
    if y > x:
        quit()
