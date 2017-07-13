cloudflare-ddns
===============
This is a continued version of [thatjpk's cloudflare-ddns](https://github.com/thatjpk/cloudflare-ddns).

Introduction
------------

A script for dynamically updating Cloudflare DNS records.
If you have a dynamic IP and you're hosting servers behind it, it's an easy way to make it 'pseudo-static'

Dependencies
------------

You'll need a [Python](https://www.python.org/downloads/) interpreter and the following libraries:

 - [PyYAML](https://bitbucket.org/xi/pyyaml) (`pip install pyyaml`)
 - [Requests](http://docs.python-requests.org/en/latest/) (`pip install
   requests`)

You can install them with `pip` :

	pip install -r requirements.txt
	
Features
-----
  - Command line usage
  - Can use `dig` to fetch the public IP
  - IPv4 and IPv6 support (A and AAAA records)
  - Logging
  - Multiple configuration files
  - Lightweight
  - Ability to edit some of your record settings such as:
  	- Time to Live (TTL)
	- Cloudflare proxy mode
  - Smart update (your record will be updated only if needed)

Usage
-----

First, a few assumptions:

  - You have a Cloudflare account.
  - You're using Cloudflare to host DNS for a domain you own.
  - You have an A/AAAA record in Cloudflare you intend to dynamically update.

To use this utility, create a copy of the `config.yml.template` file inside the `configs` folder (and
rename it to something like `ddns.example.com.yml` for example).  Create one configuration per each record / 
domain pair you intend to update.  For example, I might have two configuration
files: `example.com.yml` that updates the record for the naked (no www
prefix) domain example.com, and a second config, `www.example.com.yml` that updates the
record for www.example.com.

To do a one-off update of your DNS record, simply run `python
cloudflare_ddns.py www.example.com.yml` from your terminal.
The script will determine your public IP address and automatically update the
Cloudflare DNS record along with it.

If the program encounters an issue while attempting to update Cloudflare's 
records, you can check the `cloudflare-ddns.log` file inside the `logs` folder for more informations.

Because dynamic IPs can change regularly, it's recommended that you run this
utility periodically in the background to keep the Cloudflare record 
up-to-date.

Just add a line to your [crontab](http://en.wikipedia.org/wiki/Cron) and let
cron run it for you at a regular interval.

    # Every 30 minutes, check the current public IP, and update the record on Cloudflare if needed.
    */30 * * * * /path/to/code/cloudflare-ddns.py -c example.com.yml

This example will update the record every 30 minutes. You'll want to be sure
that you insert the correct paths to reflect were the codebase is located.

If you want to learn more about the Cloudflare API, you can read on
[here](http://www.cloudflare.com/docs/client-api.html).

Credits and Thanks
------------------

 - [Cloudflare](https://www.cloudflare.com/) for having an API and otherwise
   generally being cool.
 - [icanhazip.com](http://icanhazip.com/) for making grabbing your public IP
    from a script super easy.
 - [thatjpk](https://github.com/thatjpk/) for the initial releases of this project.

