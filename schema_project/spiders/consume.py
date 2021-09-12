import requests
from extruct import JsonLdExtractor, MicrodataExtractor, OpenGraphExtractor, RDFaExtractor
from parsers.microdata import format_microdata
from parsers.opengraph import format_og
from parsers.rdfa import format_rdfa
from parsers.jsonld import format_jsonld

import spiders.const  as const

class SchemaCrawler:

    default_headers = {
        'User-Agent': const.USER_AGENT
    }


    def __init__(self, headers=None):
        self.extractors = [
            (JsonLdExtractor(), format_jsonld),
            (MicrodataExtractor(), format_microdata),
            (RDFaExtractor(), format_rdfa),
            (OpenGraphExtractor(), format_og),
        ]

        if headers:
            self.headers = headers
        else:
            self.headers = self.default_headers

        # 接続（cookieなど）を保持する
        self.session = requests.session()
    
    def crawl(self, url):
        resp = self.session.get(url, headers=self.headers)
        assert resp.status_code == 200

        results = {}
        for extractor, parser in self.extractors[::-1]:
            extracted_nodes = extractor.extract(resp.text)
            if parser:
                extracted_nodes = [parser(node) for node in extracted_nodes]
            results[type(extractor).__name__] = [node for node in extracted_nodes if node]

        return results

    def crawl_flat(self, url):
        flat = {}
        for extracted_nodes in self.crawl(url).values():
            for result in extracted_nodes:
                flat.update(result)

        return flat

    def crawl_merged(self, url):
        merged = {}
        for extracted_nodes in sorted(self.crawl(url).values(), key=len):
            for i, result in enumerate(extracted_nodes):
                try:
                    merged[i].update(result)
                except IndexError:
                    merged.append(result)

        return merged





