|Build Status|

sender_policy_flattener
=======================

We had a problem in our organisation that caused our SPF records to become invalid:

When customers computers were querying our SPF records, there were more than 10 lookups required after following all of the ``include:`` remarks.

Solution? Query them ourselves, and create a much more condense list of SPF records.

But wait... What if the upstream records change?
------------------------------------------------

Part of what the script does is that it creates a JSON file that keeps track of the last list of IP Addresses that your combination of SPF records had.

When the hashsum of your IP Addresses changes, it will send out an email (or just dump HTML if it can't find an email server) with a handy diff & BIND format for viewing what has changed, and promptly updating it.

You could theoretically extract the flat IP records from the resulting JSON file and automatically update your DNS configuration with it.

How do I install it?
--------------------

via git clone
~~~~~~~~~~~~~

Clone this repo and run 

.. code:: shell

    pip install -r requirements.txt
    python setup.py install

You can also do this from within a virtualenv if that tickles your fancy (I recommend it).

via pip
~~~~~~~

.. code:: shell

    pip install sender_policy_flattener

How do I use it?
----------------

Python 2.7, or 3.3+ is required.

Here's the usage:

.. code:: shell

    usage: spflat [-h] [-c CONFIG] [-r RESOLVERS] [-e MAILSERVER] [-t TOADDR]
                  [-f FROMADDR] [-s SUBJECT] [-D SENDING_DOMAIN] [-d DOMAINS]
                  [-o OUTPUT]
    
    A script that crawls and compacts SPF records into IP networks. This helps to
    avoid exceeding the DNS lookup limit of the Sender Policy Framework (SPF)
    https://tools.ietf.org/html/rfc7208#section-4.6.4
    
    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            Name/path of JSON configuration file
      -r RESOLVERS, --resolvers RESOLVERS
                            Comma separated DNS servers to be used
      -e MAILSERVER, -mailserver MAILSERVER
                            Server to use for mailing alerts
      -t TOADDR, -to TOADDR
                            Recipient address for email alert
      -f FROMADDR, -from FROMADDR
                            Sending address for email alert
      -s SUBJECT, -subject SUBJECT
                            Subject string, must contain {zone}
      -D SENDING_DOMAIN, --sending-domain SENDING_DOMAIN
                            The domain which emails are being sent from
      -d DOMAINS, --domains DOMAINS
                            Comma separated domain:rrtype to flatten to IP
                            addresses. Imagine these are your SPF include
                            statements.
      -o OUTPUT, --output OUTPUT
                            Name/path of output file

Example

.. code:: shell

    spflat --resolvers 8.8.8.8,8.8.4.4 \
           --to me@mydomain.com \
           --from admin@mydomain.com \
           --subject 'SPF for {zone} has changed!' \
           --domains gmail.com:txt,sendgrid.com:txt,yahoo.com:a \
           --sending-domain mydomain.com
        
or

.. code:: shell

    spflat --config spf.json

You can specify a config file, or you can specify all of the optional arguments from the command line.

I've provided a ``settings.json`` file with an example configuration file.


3rd party dependencies
----------------------

* netaddr
* dnspython

Example email format
--------------------

|Example screenshot|


.. |Build Status| image:: https://api.travis-ci.org/cetanu/sender_policy_flattener.svg?branch=master
   :target: https://travis-ci.org/cetanu/sender_policy_flattener
.. |Example screenshot| image:: https://raw.githubusercontent.com/cetanu/sender_policy_flattener/master/example/email_example.png
