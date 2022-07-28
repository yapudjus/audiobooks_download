import re
import json
import requests
import urllib.parse


class search:
    def __init__(self, query):
        self.query = query
        data = {
            "action": "wpas_ajax_load",
            "page": "1",
            "form_data": f"search_query={query}&tax_periode=&tax_genre_livre=&tax_region=&tax_post_tag=&meta_duration=&orderby=&order=DESC&posts_per_page=1024&paged=1&wpas_id=laSearch&wpas_submit=1",
        }
        self.response = requests.post(
            "https://www.litteratureaudio.com/wp-admin/admin-ajax.php",
            data=data,
        )
        self.json = self.get_data(self.response.json()["results"])

    def get_data(self, results):
        articles = []
        for i in re.finditer(r"<article.*?>.*?</article>", results, re.DOTALL):
            tmp = i.group()
            url = (
                re.search(r'<a class="post-thumbnail-inner" href="(.*?)"', tmp)
                .group()
                .replace('<a class="post-thumbnail-inner" href="', "")
                .replace('"', "")
            )
            image = (
                re.search(r'src="(.*?)"', tmp)
                .group()
                .replace('src="', "")
                .replace('"', "")
            )
            title = (
                re.search(r'rel="bookmark">.*?</a></h3>', tmp)
                .group()
                .replace('rel="bookmark">', "")
                .replace("</a></h3>", "")
            )
            author = (
                re.search(r'rel="tag">.*?</a></span><span class="entry-voix">', tmp)
                .group()
                .replace('rel="tag">', "")
                .replace('</a></span><span class="entry-voix">', "")
            )
            if author.find("Auteurs divers") != -1 : author = "Auteurs divers"
            articles.append(
                {"url": url, "image": image, "title": title, "author": author}
            )
        return articles

class download :
    def __init__(self, url):
        self.url = url
        self.response = requests.get(self.url)
        self.tracks = self.get_tracks(url)

    def get_tracks(self, url):
        alltracks = []
        response = requests.get(url)
        pattern = r'<a class="btn-download no-ajax" title=".*?" href="https://www.litteratureaudio.com/mp3/.*?\.zip".*?>'
        for match in re.finditer(pattern, response.text):
            match = match.group()
            murl = re.search(r'href="(.*?)"', match).group().replace('href="', "").replace('"', "")
            mname = re.search(r'title=".*?"', match).group().replace('title="', "").replace('"', "")
            alltracks.append({"url": murl, "name": mname})
        return alltracks