import os
import re
from src import galaxyaudiobooks

booklist = galaxyaudiobooks.search(input('Search: ')).json
for i in range(len(booklist)):
    print(f'{i}. {booklist[i]["publish_date"]} - {booklist[i]["title"]}')

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
    galaxyaudiobooks.download.download_file(book["image"], coverfile)
    
    tracks = galaxyaudiobooks.download(book["url"]).tracks
    trackcount = 0
    for track in tracks :
        trackcount += 1
        print(f'Downloading track {track["name"]} ({trackcount}/{len(tracks)}) from book {book["title"]} ({bookcount}/{len(to_down)}) ')
        link = galaxyaudiobooks.download.get_url(track["chapter_id"])
        out = os.path.join(bookdir, re.sub(r'( |[/:,.;!§*µ$£¨ù%&"])', '_', track["name"])) + '.mp3'
        outpath = galaxyaudiobooks.download.download_file(link, out)
        print(f'Saved to {outpath}')
