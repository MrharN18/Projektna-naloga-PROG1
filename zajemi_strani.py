import re
import orodja

vzorec_povezave = re.compile(
     r'<a class="bookTitle" itemprop="url" href="(?P<link>.*?)">.*?',
     flags=re.DOTALL
)

vzorec_povezave_avtorja = re.compile(
    r'<a class="authorName" itemprop="url" href="(?P<author_link>.*?)><span itemprop="name">(?P<ime>.*?)</span>',
    flags = re.DOTALL
)


def posamezne_knjige(st_knjige, vsebina, povezava):
    url = 'https://www.goodreads.com/' + povezava
    ime_datoteke = f'zajeti-podatki/knjige/knjiga-{st_knjige}.html'
    orodja.shrani_spletno_stran(url, ime_datoteke)


def avtor(povezava_avtor, ime):
    url = povezava_avtor
    ime_avtorja = ime
    ime_datoteke = f'zajeti-podatki/avtorji/{ime_avtorja}.html'
    orodja.shrani_spletno_stran(url, ime_datoteke)

st_knjige = 1

def knjige_na_strani(st_strani):
    global st_knjige
    url = f'https://www.goodreads.com/list/show/1.Best_Books_Ever?page={st_strani}'
    ime_datoteke = 'zajeti-podatki/najboljse-knjige-{}.html'.format(st_strani)
    orodja.shrani_spletno_stran(url, ime_datoteke)
    vsebina = orodja.vsebina_datoteke(ime_datoteke)

    # Shranimo knjige
    for knjiga in vzorec_povezave.finditer(vsebina):
        povezava = knjiga.group(1)
        posamezne_knjige(st_knjige, vsebina, povezava)
        st_knjige += 1

    # Shranimo avtorje
    for knjiga in vzorec_povezave_avtorja.finditer(vsebina):
        povezava_avtorja = knjiga.group(1)
        ime_avtorja = knjiga.group(2).replace('&#39;', '\'')
        avtor(povezava_avtorja, ime_avtorja)
    print(st_knjige)


for st_strani in range(1, 6):
    knjige_na_strani(st_strani)


