# get-free-domains

Utility for getting a list of free domains of given length and top level domain.

## Usage

```shell
get-free-domains --length LENGTH
                 --tld TLD
                 [--nameserver [NAMESERVER ...]]
                 [--file FILE]
                 [--prefix PREFIX]
                 [--threads THREADS]
```

Arguments with '*' are required, the others optional.

| Argument   | Description                                                      |
| ---------- | ---------------------------------------------------------------- |
| length*     |  how many characters should the domain consist of aside the TLD  |
| tld*        | the TLD like .com, .org etc.                                     |
| nameserver | which nameservers to ask, might be multiple                      |
| file       | output text file                                                 |
| threads    | number of concurrent threads to connect to nameservers           |

## Example

```shell
main.py --length 3 --tld foo --threads 50 --file foo.txt
```

produces the file _foo.txt_ which contains all most probably free TLD .foo domains with a length of 3 characters.

All combinations from aaa.foo to zzz.foo will be sent to the nameservers.

There will be very likely false positives without DNS entries but WHOIS entries, especially when using very short length.