import os
import re
from src import galaxyaudiobooks
from src import bookaudiobooks
from src import litteratureaudio
from src import common
import html

debug = True

debugger = common.debug(debug)

query = input("Search: ")

print(f'searching for "{query}" on galaxyaudiobook.com')
galaxylist = galaxyaudiobooks.search(query).json
print(f'searching for "{query}" on bookaudiobooks.com')
bookaudiolist = bookaudiobooks.search(query).json
print(f'searching for "{query}" on litteratureaudio.com')
litteratureaudiolist = litteratureaudio.search(query).json

sources = {
    "Galaxy": {"length": len(galaxylist), "data": galaxylist, "name": "Galaxy"},
    "Bookaudio": {
        "length": len(bookaudiolist),
        "data": bookaudiolist,
        "name": "Bookaudio",
    },
    "litteratureaudio": {
        "length": len(litteratureaudiolist),
        "data": litteratureaudiolist,
        "name": "litteratureaudio",
    },
}

sourcescount = 0
for i in sources:
    if sources[i]["length"] > 0:
        print(f'{sourcescount}. {sources[i]["name"]} ({sources[i]["length"]})')
    sourcescount += 1
sourceselect = input("source: ")

sourceselect = int(sourceselect)
sourceselect = sources[list(sources.keys())[sourceselect]]["name"]

booklist, sourcetype = sources[sourceselect]["data"], sources[sourceselect]["name"]

for i in range(len(booklist)):
    if sourcetype == "Galaxy":
        print(f'{i}. {html.unescape(booklist[i]["title"])}')
    elif sourcetype == "Bookaudio":
        print(f'{i}. {html.unescape(booklist[i]["title"])}')
    elif sourcetype == "litteratureaudio":
        print(f'{i}. {html.unescape(booklist[i]["author"])} | {html.unescape(booklist[i]["title"])}')

inp = input("Selection: ")

if inp.find("--") != -1:
    ids = [i for i in range(int(inp.split("--")[0]), int(inp.split("--")[1]) + 1)]
elif inp.find(", ") != -1:
    ids = [*inp.split(", ")]
elif inp.find(". ") != -1:
    ids = [*inp.split(". ")]
elif inp.find("*") != -1:
    ids = [i for i in range(0, len(booklist))]
else:
    ids = list([inp])

to_down = [booklist[int(x)] for x in ids]

bookcount = 0
for book in to_down:
    bookcount += 1
    book["title"] = html.unescape(book["title"])
    debugger.log(f"{bookcount}/{len(to_down)} {book['title']}")
    bookdir = os.path.join(
        os.getcwd(), "out", re.sub(r'( |[/:,.;!§*µ$£¨ù%&"])', "_", book["title"])
    )
    if not os.path.isdir(bookdir):
        os.mkdir(bookdir)
    if not os.path.isfile(os.path.join(bookdir, "loaded")):
        coverfile = os.path.join(bookdir, "cover.jpg")
        print(f'Downloading cover for {book["title"]}')
        debugger.log(f'{book["image"]} => {coverfile}')
        common.common.download_file(book["image"], coverfile, lbl=book["image"])
        debugger.log(f'{book} => {os.path.join(bookdir, "book.json")}')
        common.common.write_data(book, os.path.join(bookdir, "book.json"))

        if sourcetype == "Galaxy":
            tracks = galaxyaudiobooks.download(book["url"]).tracks
        if sourcetype == "Bookaudio":
            tracks = bookaudiobooks.download(book["url"]).tracks
        if sourcetype == "litteratureaudio":
            tracks = litteratureaudio.download(book["url"]).tracks
        trackcount = 0
        for track in tracks:
            trackcount += 1
            track["name"] = html.unescape(track["name"])
            print(
                f'Downloading track {track["name"]} ({trackcount}/{len(tracks)}) from book {book["title"]} ({bookcount}/{len(to_down)}) '
            )
            out = (
                os.path.join(bookdir, re.sub(r'( |[/:,.;!§*µ$£¨ù%&"])', "_", track["name"]))
                + ".mp3"
            )
            if sourcetype == "Galaxy":
                link = galaxyaudiobooks.download.get_url(track["chapter_id"])
            elif sourcetype == "Bookaudio":
                link = track["url"]
            elif sourcetype == "litteratureaudio":
                link = track["url"]
                out = out.replace(".mp3", ".zip")
            debugger.log(f'{link} => {out}')
            outpath = common.common.download_file(link, out, lbl = f'{book["title"]} ({bookcount}/{len(to_down)})')
            print(f"Saved to {outpath}")
            
            if sourcetype == "litteratureaudio" :
                # unzip the file to the same folder
                import zipfile
                debugger.log(f"Unzipping {outpath} to {bookdir}")
                zip_file = outpath
                try:
                    with zipfile.ZipFile(zip_file) as z:
                        z.extractall(bookdir)
                        print("Extracted all")
                except:
                    print("Invalid file")
    with open(os.path.join(bookdir, "loaded"), "w") as f:
        f.write("loaded")
    if sourcetype == "litteratureaudio":
        for i in os.listdir(bookdir):
            if i.endswith(".zip"):
                print(f'removing file {i}')
                os.remove(os.path.join(bookdir, i))
    for i in os.listdir(bookdir):
        if os.path.isdir(os.path.join(bookdir, i)):
            for j in os.listdir(os.path.join(bookdir, i)):
                if j.endswith(".mp3"):
                    debugger.log(f'{os.path.join(bookdir, i, j)} => {os.path.join(bookdir)}')
                    os.rename(os.path.join(bookdir, i, j), os.path.join(bookdir, j))
                elif j.endswith(".txt") :
                    os.remove(os.path.join(bookdir, i, j))
            os.rmdir(os.path.join(bookdir, i))