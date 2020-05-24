from scraper import void
import argparse


parser = argparse.ArgumentParser()

parser.add_argument("host", help="The URL To Crawl",
                    type=str)

parser.add_argument("amount", help="Amount of generations; 1 generation == sending 1 request to each internal/external link found @ an index then returning those links. Upon next generation, the previously found links will be visited/indexed and so on.",
                    type=int)


args = parser.parse_args()



void.crawler(
# PROXY METHOD IS ALMOST WORKING, JUST CANNOT 100% ENSURE ALL "GOOD" PROXIES WILL CONNECT TO CERTAIN ENDPOINTS.
    args.host, 1, args.amount, True, False, "proxies/http_proxies.txt", "proxies/ssl_proxies.txt"
    )















