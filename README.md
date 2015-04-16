## Simple Python Based SSL Checker

This script takes a list of domains, checks to see if they have valid SSL certificates, and outputs some basic information about each certificate the script finds.

### Usage
```
ssl_check.py [-h] [-f FILE] [-v] [-q] [-o OUTFILE]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  File with domains (one per line)
  -v, --verbose         Output extra information
  -q, --quiet           Suppress all output
  -o OUTFILE, --outfile OUTFILE
                        File to print results into
```
