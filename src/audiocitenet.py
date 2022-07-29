import re
import requests


class search:
    def __init__(self, query):
        self.query = query
        data = {"r": query}
        self.response = requests.post(
            "https://www.audiocite.net/recherche.php",
            data=data,
        )
        self.json = self.get_data(self.response.text)

    def get_data(self, results):
        articles = []
        for i in re.finditer(
            r'<div class="clearfix ">.*?</div><br/>', results, re.DOTALL
        ):
            tmp = i.group()
            url = (
                re.search(r'<a href="https://www.audiocite.net/.*?"', tmp)
                .group()
                .replace('<a href="', "")
                .replace('"', "")
            )
            image = (
                re.search(r'<img src="https://www.audiocite.net/.*?"', tmp)
                .group()
                .replace('<img src="', "")
                .replace('"', "")
            )
            title = (
                re.search(r'<span class="titrenouveaute">.*?</span>', tmp)
                .group()
                .replace('<span class="titrenouveaute">', "")
                .replace("</span>", "")
            )
            author = (
                re.search(r'<span class="auteurnouveaute">.*?</span>', tmp)
                .group()
                .replace('<span class="auteurnouveaute">', "")
                .replace("</span>", "")
            )
            duration = (
                re.search(r'<span class="bolder">.*?</span>', tmp)
                .group()
                .replace('<span class="bolder">', "")
                .replace("</span>", "")
            )
            size = (
                re.search(r"de .*?<br/><br/>", tmp)
                .group()
                .replace("de ", "")
                .replace("<br/>", "")
            )
            articles.append(
                {
                    "url": url,
                    "image": image,
                    "title": title,
                    "author": author,
                    "duration": duration,
                    "size": size,
                }
            )
        return articles

class download:
    def __init__(self, url):
        self.url = url
        self.response = requests.get(self.url)
        self.tracks = self.get_tracks(url)

    def get_tracks(self, url):
        alltracks = []
        response = requests.get(url)
        pattern = r'(href="https://archive.org/download/.*?(mp3|zip)"|href="../download\.php\?id=.*?")'
        for tmp in re.finditer(pattern, response.text) : 
            tname = str(len(alltracks))
            turl = tmp.group().replace('href="', "").replace('"', "").replace("../", "https://www.audiocite.net/")
            alltracks.append({"name": tname, "url": turl})
        if len(alltracks) == 0:
            print(f"No tracks found for {url}")
        return alltracks
