#!/usr/bin/env python3
'''
ssl_check.py

Provides a basic mechanism to grab SSL certificates from a list of domains to
check their future validity. Outputs a list of all certs, their domain,
authority, expiration date, and signing algorithm.
'''
import argparse
import sys
import ssl
import subprocess
import csv
import os.path
import urllib.request


data_file = None
output_file = None
checked_domains = {}  # Use a dictionary to avoid dupicates in saved results
# these are phrases used in OpenSSL output we'll look for later.
key_words = ['Signature Algorithm:',
             'Not Before:',
             'Not After :',
             'Issuer:']
clean_keys = [k[:-1].strip() for k in key_words]  # remove : from keys for csv


parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help="File with domains (one per line)")
parser.add_argument('-v', '--verbose', help="Output extra information",
                    action="store_true")
parser.add_argument('-q', '--quiet', help="Suppress all output",
                    action="store_true")
parser.add_argument('-o', '--outfile', help="File to print results into")
parser.add_argument('--get-certs', help=
                    "Download the CA Certs currently in use by Mozilla.",
                    action="store_true")

args = parser.parse_args()

# Only allow verbose or quiet, not both
if args.verbose and args.quiet:
    print("Cannot run in verbose mode quietly. Select one not both.")

# If the user asked to load the CA set, do that.
if args.get_certs:
    cafile = urllib.request.urlopen("http://curl.haxx.se/ca/cacert.pem")
    output = open('cacert.pem', 'wb')
    output.write(cafile.read())
    output.close()
    exit()
elif args.file is None:
    print("Input file of domains is required.")
    exit()


# Check/setup input file.
try:
    data_file = open(args.file, 'rt')
except:
    print("Unable to open URL data file")
    exit()

# Check/setup out file
if args.outfile:
    try:
        output_file = open(args.outfile, 'w')
    except:
        print("Unable to open output file")
        exit()

# Setup complete. Loop over the input, checking each cert and hanlding results.
for domain in data_file:
    if domain[0] is '#':
        continue
    else:
        domain = domain.strip()

        if args.verbose:
            print('==========================')
            print("Checking: {domain}".format(domain=domain))

        # Create all the keys for each row, so we can easily dump to CSV later.
        checked_domains[domain] = dict.fromkeys(clean_keys)
        checked_domains[domain]['Domain'] = domain

        try:
            cert = ssl.get_server_certificate(addr=[domain, 443],
                                              ssl_version=ssl.PROTOCOL_TLSv1,
                                              ca_certs='./cacert.pem')

            # Since ssl doesn't provide everything we need have OpenSSL decode
            # the certificate. Avoids having a requirement of loading pyOpenSSL
            # but likely slows the process down a bit.
            p = subprocess.Popen(['openssl', 'x509', '-text'],
                                 stdout=subprocess.PIPE,
                                 stdin=subprocess.PIPE,
                                 stderr=subprocess.STDOUT,
                                 universal_newlines=True)
            cert_data = p.communicate(input=cert)[0]
            for line in cert_data.split('\n'):
                for key in key_words:
                    if line.strip()[:len(key)] == key:
                        checked_domains[domain][key[:-1].strip()] = \
                            line.strip()[len(key):].strip()
                        if args.verbose:
                            print(line.strip())

        except Exception as e:
            checked_domains[domain]['Errors'] = e
            if not args.quiet:
                print("Error checking {domain}".format(domain=domain))
            if args.verbose:
                print(e)

if args.outfile is not None:
    writer = csv.DictWriter(
       output_file,
       fieldnames=['Domain', 'Errors']+clean_keys,
       delimiter=',',
       quotechar='"',
       quoting=csv.QUOTE_MINIMAL,
       extrasaction='ignore'
    )
    writer.writeheader()
    for a in checked_domains:
        writer.writerow(checked_domains[a])
