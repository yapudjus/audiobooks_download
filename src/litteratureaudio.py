import re
import requests


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
            try :
                author = (
                    re.search(r'rel="tag">.*?</a></span><span class="entry-voix">', tmp)
                    .group()
                    .replace('rel="tag">', "")
                    .replace('</a></span><span class="entry-voix">', "")
                )
            except :
                author = "unknown"
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
        
        if len(alltracks) == 0 : # zip code
            pattern = r'<a class="btn-download no-ajax" title=".*?" href="https://www.litteratureaudio.com/mp3/.*?\.zip".*?>'
            tmp = []
            for i in re.finditer(pattern, response.text) : tmp.append(i)
            if len(tmp) > 0 :
                print('zip')
                for match in tmp:
                    match = match.group()
                    murl = re.search(r'href="(.*?)"', match).group().replace('href="', "").replace('"', "")
                    mname = re.search(r'title=".*?"', match).group().replace('title="', "").replace('"', "")
                    alltracks.append({"url": murl, "name": mname})
        
        if len(alltracks) == 0 : # mp3 code
            print('mp3')
            pattern = r'<a.*?href="https://www.litteratureaudio.com/mp3/.*?".*?(</a)?>'
            matches = re.finditer(pattern, response.text)
            tmp = []
            for i in mathes : tmp.append(i)
            if len(tmp) > 0 :
                for match in matches :
                    if match.group().find('rel="home"') == -1 and match.group().find('.zip') == -1 :
                        match = match.group()
                        murl = re.search(r'href="(.*?)"', match).group().replace('href="', "").replace('"', "")
                        mname = re.search(r'">.*?</a>', match).group().replace('">', "").replace('</a>', "")
                        alltracks.append({"url": murl, "name": mname})
        
        if len(alltracks) == 0 : # zip fallback code
            print('zip_fallback_1')
            pattern = r'"https://www.litteratureaudio.com/mp3/.*?\.zip"'
            matches = re.finditer(pattern, response.text)
            tmp = []
            for i in matches : tmp.append(i)
            if len(tmp) > 0 :
                for i in matches :
                    mname = i.group().replace('"https://www.litteratureaudio.com/mp3/', "")
                    murl = i.group()
        
        if len(alltracks) == 0 : # mp3 fallback code
            print('mp3_fallback_1')
            pattern = r'"https://www.litteratureaudio.com/mp3/.*?\.mp3"'
            matches = re.finditer(pattern, response.text)
            tmp = []
            for i in matches : tmp.append(i)
            if len(tmp) > 0 :
                for i in matches :
                    mname = i.group().replace('"https://www.litteratureaudio.com/mp3/', "")
                    murl = i.group()
        
        if len(alltracks) == 0 : # no more fallback code
                print('no more fallback solution for this book')
        return alltracks
