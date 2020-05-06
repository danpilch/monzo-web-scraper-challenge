# monzo-web-scraper-challenge

challenge for interview

# info

A basic web scraper to get links from html pages for monzo interview

# requirements

python3 
python3-pip

[install]
`pip3 install --user -r requirements.txt`

# usage
```
usage: a simple web crawler [-h] [--url URL]
                            [--log {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

optional arguments:
  -h, --help            show this help message and exit
  --url URL, -u URL     Root URL to start crawling from
  --log {DEBUG,INFO,WARNING,ERROR,CRITICAL}, -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Set the logging level
```

# run
`python3 run.py -u https://monzo.com` 
or
```
docker build . -t simple_scraper
docker run simple_scraper
```


# testing
`nosetests tests.py --logging-level=INFO`
