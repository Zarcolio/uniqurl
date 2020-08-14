# About uniqurl
Use uniqurl to filter only unique content from a list of URLs with stdin, making it usable within piped commands.
From all URLs that have duplicate content (tested with MD5 on the content), the shortest URL is shown.

# Why uniqurl?
If you have a lot of URLs, but some URLs point to the same page or contain apparent useless, use uniqurl to filter those URLS with duplicate content.
This leaves you with less targets to scan when you start off with a large list.

# Install
Uniqurl should be able to run with a default Kali Linux installation without installing additional Python packages. 
Just run:
```
git clone https://github.com/Zarcolio/uniqurl
cd uniqurl
bash install.sh
```
If you're running into trouble running uniqurl, please drop me an issue and I'll try to fix it :)

# Usage
```
usage: uniqurl [-h] [-headers <headers>] [-cookies <cookies>] [-proxy <proxy>] [-redirect <boolean>] 
[-timeout <seconds>] [-workers <workers>]

Use uniqurl to distinguish unique URLs based on the MD5 hash of the content of the page. This script uses URLs as input.

optional arguments:
  -h, --help           show this help message and exit
  -headers <headers>   Supply header to a GET request.
  -cookies <cookies>   Supply cookie to a GET request.
  -proxy <proxy>       Supply a proxy to a GET request.
  -redirect <boolean>  Allow redirects, defaults to "True", use "False" to disable.
  -timeout <seconds>   Define a timeout for the requests, defaults to 2 seconds.
  -workers <workers>   Define a number of parallel workers, defaults to 20 workers.
```

# Examples
To get only unique URLs by [hakrawler](https://github.com/hakluke/hakrawler) just run (don't forget '-plain' in the command):
```
hakrawler -url google.com -plain|uniqurl
```

Want to pass the URLs from [waybackurls](https://github.com/tomnomnom/waybackurls), 5 at a time to uniqurl?
```
cat waybackurls.txt |uniqurl --workers 5
```

If you have a list of URLs, you can throw it at uniqurl, for example through a proxy:
```
cat urls.txt|uniqurl --proxies http://127.0.0.1:8080
```
# Contribute?
Do you have some usefull additions to the script, please send in a pull request to help make this script better :)
