import re
import os
import json
import requests
import urllib.parse
from clint.textui import progress


class search:
    def __init__(self, query):
        self.query = query
        self.url = f"https://galaxyaudiobook.com/?s={urllib.parse.quote(query)}"
        self.response = requests.get(self.url)
        self.json = self.get_data(self.response)

    def get_data(self, response):
        alldata = []
        pattern = r"<article(.|\n)*?</article>"
        # find all occurences matching the pattern and return them in a list
        for match in re.finditer(pattern, response.text):
            temp = match.group()
            url = (
                re.search(r'<a href="https://galaxyaudiobook.com.*?">', temp)
                .group()
                .replace('<a href="', "")
                .replace('">', "")
            )
            image = (
                re.search(
                    r'src="https://galaxyaudiobook.com/wp-content/uploads/.*?" class="attachment-full size-full wp-post-image" ',
                    temp,
                )
                .group()
                .replace('src="', "")
                .replace('" class="attachment-full size-full wp-post-image" ', "")
            )
            title = (
                re.search(r'rel="bookmark">.*.</a></h2>', temp)
                .group()
                .replace('rel="bookmark">', "")
                .replace("</a></h2>", "")
            )
            publish_date = (
                re.search(
                    r'<time class="entry-date published" datetime=".*?" itemprop="datePublished">',
                    temp,
                )
                .group()
                .replace('<time class="entry-date published" datetime="', "")
                .replace('" itemprop="datePublished">', "")
            )
            alldata.append(
                {
                    "url": url,
                    "image": image,
                    "title": title,
                    "publish_date": publish_date,
                }
            )
        return alldata


class download:
    def __init__(self, url):
        self.url = url
        self.response = requests.get(self.url)
        self.tracks = self.get_tracks(self.response)

    def get_tracks(self, response):
        tracks_tmp = (
            re.search(r"tracks = \[(.|\n)*?\]", response.text)
            .group()
            .replace("tracks = [", "")
            .replace("]", "")
        )
        tracks_tmp_2 = tracks_tmp.split("}")
        tracks = []
        for i in range(1, len(tracks_tmp_2) - 1):
            tmp = (
                tracks_tmp_2[i].replace("\n", "").replace("  ", "").replace(",{", "{")
                + "}"
            )
            tmp = tmp.replace(",}", "}")
            tracks.append(json.loads(tmp))
        return tracks

    def get_url(chapter_id):
        r = requests.post(
            "https://api.galaxyaudiobook.com/api/getMp3Link",
            data=f'{{"chapterId": {chapter_id}, "serverType": 1}}',
            headers={
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.5",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "application/json; charset=utf-8",
                "DNT": "1",
                "Origin": "https://galaxyaudiobook.com",
                "Pragma": "no-cache",
                "Referer": "https://galaxyaudiobook.com/",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-site",
                "Sec-GPC": "1",
                "TE": "trailers",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
            },
            cookies={},
            auth=(),
        )
        
        return(r.json()["link_mp3"])
    def download_file(url, out):
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
