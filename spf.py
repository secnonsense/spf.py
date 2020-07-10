#!/usr/bin/python

#uses dnspython - http://www.dnspython.org/
import sys, re, dns.resolver

if len(sys.argv) < 2:
    print("\nThis script recursively looks for spf records for a given domain name.")
    print("\nUsage: ./spf.py domain.com\n")
    quit()

x = y = 0
spf, lspf, lookup, alookup, mxlookup = ([] for z in range(5))

#First Lookup of Domain Passed as Argument - Added to lookup list
lookup.append(sys.argv[1])

#Primary Loop for processing initial DNS lookup and itterating through includes
while lookup:
#Choose Record type of lookup
    if lookup[y] in alookup:
        Q = "A"
    elif lookup[y] in mxlookup:
        Q = "MX"
    else:
        Q = "TXT"
#DNS query and print domain name being processed while handling any error exceptions
    try:
        answers = dns.resolver.query(lookup[y], Q)
    except dns.resolver.NXDOMAIN:
        print("\nNo such domain %s" % lookup[y] + "\n")
        quit()
    except dns.resolver.NoNameservers:
        print("\nNo answers for domain %s" % lookup[y] + " for " + Q + " record query\n")
        quit()
    except dns.resolver.NoAnswer:
        print("\nNo " + Q + " record answer for domain %s" % lookup[y] + "\n")
        quit()
    print("\ndomain block:  " + lookup[y])

    for server in answers:
        lspf = re.split('\s', str(server))
        spf = [s.strip('"') for s in lspf]
        print('\n' + Q + ' Record: ' + ' '.join(spf) + '\n')
#Loop to look at all elements of the returned record
        for i in range(0, len(spf)):
            if spf[0] != 'v=spf1' and Q != "A" and Q != "MX":
                print("No spf\n")
#Add includes to lookup for further processing and increment counter
            elif "include:" in spf[i]:
                inc = spf[i].split(":")
                lookup.append(inc[1])
                x = x+1
#Add a "A" records to lookup and alookup so their query can be handled properly
            elif "a:" in spf[i].lower() and "ip6" not in spf[i].lower():
                a = spf[i].split(":")
                lookup.append(a[1])
                alookup.append(a[1])
                x = x+1
            elif spf[i].lower() == "mx" or spf[i].lower() == "+mx":
                lookup.append(lookup[y])
                mxlookup.append(lookup[y])
                x = x+1
            elif spf[i].lower() == "a" or spf[i].lower() == "+a":
                lookup.append(lookup[y])
                alookup.append(lookup[y])
                x = x+1

#Print the IPv4 addresses in an easily copiable block
            elif "ip4:" in spf[i].lower():
                ip = spf[i].split(":")
                if "/" not in ip[1]:
                    print(ip[1] + "/32")
                else:
                    print(ip[1])
            elif "ip6:" in spf[i].lower():
                ip6 = spf[i]
                print(ip6[4:])
            elif Q == "A":
                print(spf[i])
            elif Q == "MX" and len(spf[i]) > 3:
                lookup.append(spf[i])
                alookup.append(spf[i])
                x = x+1
#Counter to be sure we don't loop beyond the end of the lookup list
    y = y+1
    print("\n=====================================")
    if y > x:
        print("\n")
        quit()
