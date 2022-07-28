import json
import requests
import os
from clint.textui import progress
import urllib.parse

class common :
    def write_data(data, path):
        with open(path, "w") as f:
            f.write(json.dumps(data))
    
    def download_file(url, out):
        url = urllib.parse.unquote(url)
        r = requests.get(url, stream=True)
        total_length = int(r.headers.get("content-length"))
        dodownload = True
        if os.path.exists(out):
            if os.path.getsize(out) == total_length:
                dodownload = False
            else:
                os.remove(out)
        if dodownload:
            with open(out, "wb") as f:
                for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
                    if chunk:
                        f.write(chunk)
                        f.flush()
        else :
            print("File already exists")
        return out
