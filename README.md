## Simple Python Based SSL Checker

This script takes a list of domains, checks to see if they have valid SSL certificates, and outputs some basic information about each certificate the script finds. See example_data.txt for input format (one domain per line). Output files are CSV.

### Usage
```
usage: ssl_check.py [-h] [-f FILE] [-v] [-q] [-o OUTFILE] [--get-certs]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  File with domains (one per line)
  -v, --verbose         Output extra information
  -q, --quiet           Suppress all output
  -o OUTFILE, --outfile OUTFILE
                        File to print results into
  --get-certs           Download the CA Certs currently in use by Mozilla.
```

### CA Cert information

This script will look for a list of CA root certificates in a cacert.pem file. It will download a recent copy built from Firefox source if you use the --get-certs flag. You can also provide your own.
For more about the copy that gets downloaded see: http://curl.haxx.se/docs/caextract.html
Their pem download files is here: http://curl.haxx.se/ca/cacert.pem
And directly from Mozilla here: http://hg.mozilla.org/mozilla-central/file/tip/security/nss/lib/ckfw/builtins/certdata.txt
