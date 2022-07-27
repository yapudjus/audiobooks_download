import os
import re
from unicodedata import name
from src import galaxyaudiobooks
from src import common

query = input('Search: ')
print(f'searching for "{query}" on galaxyaudiobook.com')
galaxylist = galaxyaudiobooks.search(query).json

sources = {
    "Galaxy": {"length": len(galaxylist), "data": galaxylist, "name": "Galaxy"},
}

sourcescount = 0
for i in sources:
    if sources[i]["length"] > 0:
        print(f'{sourcescount}. {sources[i]["name"]} ({sources[i]["length"]})')
    sourcescount += 1
sourceselect = input('source: ')

sourceselect = int(sourceselect)
sourceselect = sources[list(sources.keys())[sourceselect]]["name"]

booklist, sourcetype = sources[sourceselect]["data"], sources[sourceselect]["name"]

for i in range(len(booklist)):
    if sourcetype == "Galaxy":
        print(f'{i}. {booklist[i]["title"]}')

inp = (input('Selection: '))

if inp.find('--') != -1 :
    ids = [i for i in range(int(inp.split('--')[0]), int(inp.split('--')[1]) + 1)]
elif inp.find(', ') != -1 :
    ids = [*inp.split(', ')]
elif inp.find('. ') != -1 :
    ids = [*inp.split('. ')]
elif inp.find('*') != -1 :
    ids = [i for i in range(0, len(booklist))]
else :
    ids = list([inp])

to_down = [booklist[int(x)] for x in ids]

bookcount = 0
for book in to_down :
    bookcount += 1
    bookdir = os.path.join(os.getcwd(), 'out', re.sub(r'( |[/:,.;!§*µ$£¨ù%&"])', '_', book["title"]))
    if not os.path.isdir(bookdir): os.mkdir(bookdir)
    coverfile = os.path.join(bookdir, 'cover.jpg')
    print(f'Downloading cover for {book["title"]}')
    common.common.download_file(book["image"], coverfile)
    common.common.write_data(book, os.path.join(bookdir, 'book.json'))
    
    if sourcetype == "Galaxy":
        tracks = galaxyaudiobooks.download(book["url"]).tracks
    trackcount = 0
    for track in tracks :
        trackcount += 1
        print(f'Downloading track {track["name"]} ({trackcount}/{len(tracks)}) from book {book["title"]} ({bookcount}/{len(to_down)}) ')
        if sourcetype == "Galaxy":
            link = galaxyaudiobooks.download.get_url(track["chapter_id"])
        out = os.path.join(bookdir, re.sub(r'( |[/:,.;!§*µ$£¨ù%&"])', '_', track["name"])) + '.mp3'
        outpath = common.common.download_file(link, out)
        print(f'Saved to {outpath}')
