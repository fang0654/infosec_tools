#!/usr/bin/env python3

import requests
import argparse
import pdb
import re
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


if __name__ == "__main__":
    args = argparse.ArgumentParser()

    args.add_argument("--url", help="URL to scan, ie https://www.google.com")
    args.add_argument("--proxy", help="Proxy to use", default=None)
    args.add_argument("--output", help="Output file", default="results.txt")
    opts = args.parse_args()

    if opts.proxy:
        proxies = {"http": opts.proxy, "https": opts.proxy}
    else:
        proxies = None
    res = requests.get(opts.url, proxies=proxies, verify=False)

    url = opts.url
    if url[-1] == "/":
        url = url[:-1]
    if res.status_code == 200:
        potential_hits = re.findall(r'"text/javascript"(.*?)">', res.text)

        for p in potential_hits:
            if "http" not in p:
                quot = '"'
                map_name = p.split(quot)[-1]
                map_url = f"{url}{'' if map_name[0] == '/' else '/'}{map_name}.map"

                map_file = requests.get(map_url)

                if (
                    map_file.status_code == 200
                    and map_file.text
                    and map_file.text[:10] == '{"version"'
                ):
                    print(f"Map found at {map_url}")
                    open(opts.output, "a").write(f"{map_url}\n")
