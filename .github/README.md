<h4 align="center">A script for dynamically updating Cloudflare DNS records.</h4>

<p align="center">
    <a href="https://github.com/totaldebug/cloudflare-ddns/commits/master">
    <img src="https://img.shields.io/github/last-commit/totaldebug/cloudflare-ddns.svg?style=flat-square&logo=github&logoColor=white"
         alt="GitHub last commit">
    <a href="https://github.com/totaldebug/cloudflare-ddns/issues">
    <img src="https://img.shields.io/github/issues-raw/totaldebug/cloudflare-ddns.svg?style=flat-square&logo=github&logoColor=white"
         alt="GitHub issues">
    <a href="https://github.com/totaldebug/cloudflare-ddns/pulls">
    <img src="https://img.shields.io/github/issues-pr-raw/totaldebug/cloudflare-ddns.svg?style=flat-square&logo=github&logoColor=white"
         alt="GitHub pull requests">
</p>

<p align="center">
  <a href="#about">About</a> •
  <a href="#configuration">Configuration</a> •
  <a href="#features">Features</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#author">Author</a> •
  <a href="#support">Support</a> •
  <a href="#donate">Donate</a> •
  <a href="#credits">Credits</a> •
  <a href="#license">License</a>
</p>

---

## About

<table>
<tr>
<td>

**cloudflare-ddns** is a **high-quality** _app_ that is capable of **updating DNS Records**

It comes in extremely useful if you have a **dynamic IP Address** and you are hosting servers behind it, its an easy way to make it **_pseydo-static_**.

This is an updated version of [adrienbrignon's cloudflare-ddns](https://github.com/adrienbrignon/cloudflare-ddns).

</td>
</tr>
</table>

## Configuration

### Dependencies

- [Python3](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/)
  - `pip3 install poetry`

### Install Python Packages

```shell
poetry install --no-dev
```

### Usage

First, a few assumptions:
 - You are using CloudFlare to host the DNS for a domain you own.
 - You have one or more A/AAAA records in Cloudflare you intend to dynamically update.

1. To use this utility, create a copy of the `example.com.yml` file inside the `zones` folder.
2. Rename the file to your domain zone name.
3. To do a one-off update of your DNS record, simply run:
```shell
python cloudflare-ddns.py -z example.com
```

The script will determine your public IP address and automatically update the records along with it and the settings you provided.

If the program encounters an issue while attempting to update Cloudflare's
records, you can check the the `logs` folder for more informations.

Because dynamic IPs can change regularly, it's recommended that you run this
utility periodically in the background to keep your records up-to-date.

Just add a line to your [crontab](http://en.wikipedia.org/wiki/Cron) and let
cron run it for you at a regular interval.

```shell
# Every 30 minutes, update my Cloudflare records.
*/30 * * * * python /path/to/cloudflare-ddns.py -z example.com
```

This example will update your records every 30 minutes. You'll want to be sure
that you insert the correct paths to reflect where the codebase is located.

If you want to learn more about the Cloudflare API, you can read on
[here](https://api.cloudflare.com/).

### YAML Configuration

If you want to restrict the token access to only be allowed to update a specific zone then set the `cf_zone:` option.

This option being set means a list of the zones is not required.


## Features

|                                                |         🔰         |
| ---------------------------------------------- | :----------------: |
| Smart update (records only updated if needed)  |         ✔️         |
| Lightweight                                    |         ✔️         |
| Built-in Logging                               |         ✔️         |
| Proxy Mode                                     |         ✔️         |
| IPv4 Suport (A Records)                        |         ✔️         |
| IPv6 Support (AAAA Records)                    |         ✔️         |
| HTTP or Dig to gain IP Address                 |         ✔️         |
| One config file                                |         ✔️         |

## Contributing

Got **something interesting** you'd like to **share**? Learn about [contributing](https://github.com/totaldebug/.github/blob/main/.github/CONTRIBUTING.md).

## Author

| [![TotalDebug](https://totaldebug.uk/assets/images/logo.png)](https://linkedin.com/in/marksie1988) 	|
|:---------------------------------------------------------------------------------------------------------:	|
|                                            **marksie1988 (Steven Marks)**                                            	|

## Support

Reach out to me at one of the following places:

- via [Discord](https://discord.gg/6fmekudc8Q)
- Raise an issue in GitHub

## Donate

## Credits
 - [Cloudflare](https://www.cloudflare.com/) for having an API and otherwise
   generally being cool.
 - [icanhazip.com](http://icanhazip.com/) for making grabbing your public IP
    from a script super easy.
 - [thatjpk](https://github.com/thatjpk/) for the initial releases of this project.

## License

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-orange.svg?style=flat-square)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

- Copyright © [Total Debug](https://totaldebug.uk "Total Debug").
