import re
import json
import requests
import urllib.parse


class search:
    def __init__(self, query):
        self.query = query
        self.url = f"https://bookaudiobooks.com/?s={urllib.parse.quote(query)}"
        self.response = requests.get(self.url)
        self.json = self.get_data(self.response)

    def get_data(self, response):
        alldata = []
        pattern = r"<article(.|\n)*?</article>"
        # find all occurences matching the pattern and return them in a list
        for match in re.finditer(pattern, response.text):
            temp = match.group()
            url = (
                re.search(
                    r'<h2 class="entry-title"><a href="https://bookaudiobooks.com/.*?">',
                    temp,
                )
                .group()
                .replace('<h2 class="entry-title"><a href="', "")
                .replace('">', "")
                .replace('" rel="bookmark', "")
            )
            image = (
                re.search(
                    r'src=".*?"',
                    temp,
                )
                .group()
                .replace('src="', "")
                .replace('"', "")
            )
            title = (
                re.search(r'title=".*">', temp)
                .group()
                .replace('title="', "")
                .replace('">', "")
            )
            alldata.append(
                {
                    "url": url,
                    "image": image,
                    "title": title,
                }
            )
        return alldata


class download:
    def __init__(self, url):
        self.url = url
        self.response = requests.get(self.url)
        self.tracks = self.get_tracks(self.url)

    def get_tracks(self, url):
        alltracks = []
        response = requests.get(url)
        pattern = r'class="page-links"(.|\n)*?</div>'
        pagestemp = re.search(pattern, response.text).group()
        pagestemp = pagestemp.replace('class="page-links">Pages: ', "").replace(
            "</div>", ""
        )
        for i in re.finditer(r'"post-page-numbers">\d*?</a>', pagestemp) :
            pagescount = i.group().replace('"post-page-numbers">', "").replace("</a>", "")
            trackcount = 0
        for i in range(1, int(pagescount) + 1):
            turl = f"{url}/{i}"
            urllist = []
            response = requests.get(turl)
            for i in re.finditer(r'https://ipaudio6.com/wp-content/uploads/BOOKAUDIO/.*?\.mp3', response.text):
                alltracks.append({
                    "url": i.group(),
                    "name": f"{trackcount}"
                })
                trackcount += 1
        return alltracks
