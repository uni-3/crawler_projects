import csv
import click
from crawler import crawl

BASE_URL = ""

@click.command()
@click.argument("outfile", type=click.File('w'))
def main(outfile):
    url = BASE_URL
    csv_writer = None
    for job in crawl(url):
        if not csv_writer:
            csv_writer = csv.DictWriter(outfile, job)
            csv_writer.writeheader()
        csv_writer.writerow(job)

if __name__ == "__main__":
    main()

