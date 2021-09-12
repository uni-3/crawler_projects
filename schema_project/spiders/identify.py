import requests
import extruct

import spiders.const  as const

def identify_schema_formats(url):
    resp = requests.get(url, headers={"User-Agent": const.USER_AGENT})
    data = extruct.extract(resp.text, base_url=url, encoding=resp.encoding)
    found = []

    for format, value in data.items():
        if value:
            found.append(format)

    return sorted(found)