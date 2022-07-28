import json
import requests
import os
from clint.textui import progress
import urllib.parse

class common :
    def write_data(data, path):
        with open(path, "w") as f:
            f.write(json.dumps(data))
    
    def download_file(url, out, lbl = ""):
        url = urllib.parse.unquote(url)
        dodownload = True
        r = requests.get(url, stream=True)
        try :
            total_length = int(r.headers.get("content-length"))
        except :
            print(f'{url} : No content-length header')
            dodownload = False
        if os.path.exists(out):
            if os.path.getsize(out) == total_length:
                dodownload = False
            else:
                os.remove(out)
        if dodownload:
            with open(out, "wb") as f:
                for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1, label=lbl, filled_char="█", width=50):
                    if chunk:
                        f.write(chunk)
                        f.flush()
        else :
            print("File already exists")
        return out

class debug :
    def __init__(self, debug = False):
        self.debug = debug
        self.debug_print = print if self.debug else lambda *a, **k: None
        self.debug_print("Debug mode is on")
    def __call__(self, *a, **k):
        self.debug_print(*a, **k)
    def log(self, *a, **k):
        self.debug_print(*a, **k)
    def debug_print(self, *a, **k):
        print(*a, **k)
