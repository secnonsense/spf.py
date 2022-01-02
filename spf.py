#!/usr/bin/python
"""This script uses dnspython - http://www.dnspython.org/ to lookup spf records
and iterate through all of the answers outputing IP addresses"""

import sys
import re
import dns.resolver

def lookup_loop(lookup):
    """Main loop to do DNS lookups and parse out IP addresses"""
    counter = counter2 = 0
    spf, lspf, alookup, mxlookup, all_ips = ([] for z in range(5))
    #Primary Loop for processing initial DNS lookup and itterating through includes
    while lookup:
    #Choose Record type of lookup
        if lookup[counter2] in alookup:
            query_type = "A"
        elif lookup[counter2] in mxlookup:
            query_type = "MX"
        else:
            query_type = "TXT"
    #DNS query and print domain name being processed while handling any error exceptions
        try:
            answers = dns.resolver.resolve(lookup[counter2], query_type)
        except dns.resolver.NXDOMAIN:
            print("\nNo such domain %s" % lookup[counter2] + "\n")
            quit()
        except dns.resolver.NoNameservers:
            print("\nNo answers for domain %s" % lookup[counter2] + " for " + query_type + " record query\n")
            quit()
        except dns.resolver.NoAnswer:
            print("\nNo " + query_type + " record answer for domain %s" % lookup[counter2] + "\n")
            quit()
        print("\ndomain block:  " + lookup[counter2])

        for server in answers:
            lspf = re.split('\s', str(server))
            spf = [s.strip('"') for s in lspf]
            print('\n' + query_type + ' Record: ' + ' '.join(spf) + '\n')
    #Loop to look at all elements of the returned record
            for i in range(0, len(spf)):
                if spf[0] != 'v=spf1' and query_type != "A" and query_type != "MX":
                    print("No spf\n")
    #Add includes to lookup for further processing and increment counter
                elif "include:" in spf[i]:
                    inc = spf[i].split(":")
                    lookup.append(inc[1])
                    counter += 1
    #Add a "A" records to lookup and alookup so their query can be handled properly
                elif "a:" in spf[i].lower() and "ip6" not in spf[i].lower():
                    split_value = spf[i].split(":")
                    lookup.append(split_value[1])
                    alookup.append(split_value[1])
                    counter += 1
                elif spf[i].lower() == "mx" or spf[i].lower() == "+mx":
                    lookup.append(lookup[counter2])
                    mxlookup.append(lookup[counter2])
                    counter += 1
                elif spf[i].lower() == "a" or spf[i].lower() == "+a":
                    lookup.append(lookup[counter2])
                    alookup.append(lookup[counter2])
                    counter += 1

    #Print the IPv4 addresses in an easily copiable block
                elif "ip4:" in spf[i].lower():
                    ip_address = spf[i].split(":")
                    if "/" not in ip_address[1]:
                        print(ip_address[1] + "/32")
                        all_ips.append(ip_address[1])
                    else:
                        print(ip_address[1])
                        all_ips.append(ip_address[1])
                elif "ip6:" in spf[i].lower():
                    ip6 = spf[i]
                    print(ip6[4:])
                    all_ips.append(ip6[4:])
                elif query_type == "A":
                    print(spf[i] + "/32")
                    all_ips.append(spf[i] + "/32")
                elif query_type == "MX" and len(spf[i]) > 3:
                    lookup.append(spf[i])
                    alookup.append(spf[i])
                    counter += 1
    #Counter to be sure we don't loop beyond the end of the lookup list
        counter2 += 1
        print("\n=====================================")
        if counter2 > counter:
            print("\n")
            print(','.join(all_ips))
            print("\n")
            quit()

def main():
    lookup = []
    if len(sys.argv) < 2:
        print("\nThis script recursively looks for spf records for a given domain name.")
        print("\nUsage: ./spf.py domain.com\n")
        quit()
    #First Lookup of Domain Passed as Argument - Added to lookup list
    lookup.append(sys.argv[1])
    lookup_loop(lookup)

if __name__ == "__main__":
    main()
