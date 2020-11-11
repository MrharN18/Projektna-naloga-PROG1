import re
import orodja
import starosti


vzorec_bloka = re.compile(
    r'<tr itemscope itemtype="http://schema.org/Book">.*?'
    r'</td>\s*</tr>',
    flags=re.DOTALL
)

vzorec_ocene_in_glasov = re.compile(
    #r'<a class="bookTitle" itemprop="url" href="(?P<link>.*?)">.*?'
    r'<a href.*?score: (?P<score>(\d|,)+).*?'
    r'<a id="loading_link_\d+" .*?return false;">(?P<glasovi>(\d|,)+)',
    flags=re.DOTALL
)


vzorec_knjige = re.compile(
    r'<meta content=\'(?P<dolzina>\d+)\' property=\'books:page_count\'>.*?'
    r'<h1 id="bookTitle".*?itemprop="name">\n\s+(?P<naslov>.*?)\n.*?'
    r'<span itemprop="ratingValue">.*?(?P<avgrating>\d+.\d+).*?'
    r'<meta itemprop="ratingCount" content="\d+" />.*?(?P<ratings>(\d+|,)+).*?'
    r'<div class="row">\n.*?\n.*?(?P<leto>\d{3,4}).*?'    # leto izida te izdaje knjige
    r'<div class="infoBoxRowItem">.*?(?P<id>\d+\').*?',
    flags=re.DOTALL
)

vzorec_izdaje_originala = re.compile(
    r'\(first published.*?(?P<leto_original>-?\d{3,4})',
    flags=re.DOTALL
)

vzorec_reviews = re.compile(
     r'<meta itemprop="reviewCount" content="\d+".*?\n\s+(?P<reviews>\d+,?\d+).*?',
     flags=re.DOTALL
)

vzorec_osebe = re.compile(
    r'<a class="authorName" itemprop="url" href="https://www.goodreads.com/author/show/(?P<id_osebe>\d+).*?<span itemprop="name">(?P<ime>.*?)</span>',
    flags=re.DOTALL
)

vzorec_avtorja = re.compile(
    r'<div id="bookAuthors" class="">(?P<avtor>.+?)</a>',
    flags=re.DOTALL
)

vzorec_zanrov = re.compile(
    r'<div class=" clearFloats bigBox">.*?Genres(?P<zanri>.*?<div class="elementList elementListLast">.*?</a>)',
    flags=re.DOTALL
)

vzorec_zanra = re.compile(
    r'<a class="actionLinkLite bookPageGenreLink" href="/genres/.*?>(?P<zanr>.*?)</a>\n*',
    flags=re.DOTALL
)

vzorec_nagrad = re.compile(
    r'<div class="infoBoxRowItem" itemprop=\'awards\'>(?P<nagrade>.*?)</div>',
    flags=re.DOTALL
)
vzorec_nagrade = re.compile(
    r'<a class="award" href="/award/show/.*?>(?P<nagrada>.*?)</a>.*?',
    flags=re.DOTALL
)






def izloci_osebe(niz):
    osebe = []
    for oseba in vzorec_osebe.finditer(niz):
        ime_avtorja = oseba.group(2).replace('&#39;', '\'')
        datoteka = f'zajeti-podatki/avtorji/{ime_avtorja}.html'
        leto_rojstva, starost = starosti.izracun_starosti(datoteka)
        osebe.append({
            'id_osebe': int(oseba.groupdict()['id_osebe']),
            'ime': ime_avtorja,
            'leto_rojstva' : leto_rojstva,
            'starost' : starost,
        })
    return osebe

def izloci_zanre(niz):
    zanri = set()
    for zadetek in vzorec_zanra.finditer(niz):
        zanri.add(zadetek.groupdict()['zanr'])
    zanri = list(zanri)
    return zanri

def izloci_nagrade(niz):
    nagrade = set()
    for zadetek in vzorec_nagrade.finditer(niz):
        nagrade.add(zadetek.groupdict()['nagrada'].replace('&#39;', '\''))
    nagrade = list(nagrade)
    return nagrade

def izloci_podatke_ocen_in_glasov(book):
    blok = vzorec_ocene_in_glasov.search(book).groupdict()
    blok['score'] = int(blok['score'].replace(',', ''))
    blok['glasovi'] = int(blok['glasovi'].replace(',', ''))

    return blok
    
def izloci_podatke_knjige(book):
    knjiga = vzorec_knjige.search(book).groupdict()
    knjiga['id'] = int(knjiga['id'].strip('\''))
    knjiga['dolzina'] = int(knjiga['dolzina'])
    knjiga['leto'] = int(knjiga['leto'])
    knjiga['avgrating'] = float(knjiga['avgrating'])
    knjiga['ratings'] = int(knjiga['ratings'].replace(',', ''))
    
    izdaja_originala = vzorec_izdaje_originala.search(book)

    if izdaja_originala:
        knjiga['leto_original'] = int(izdaja_originala.group(1))
    else:
        knjiga['leto_original'] = None


    reviews = vzorec_reviews.search(book)
    knjiga['reviews'] = int(reviews['reviews'].replace(',', ''))

    avtor = vzorec_avtorja.search(book)
    knjiga['avtor'] = izloci_osebe(avtor['avtor'])

    zanri = vzorec_zanrov.search(book)
    if zanri:
        knjiga['zanri'] = izloci_zanre(zanri['zanri'])
    else:
        knjiga['zanri'] = None
    nagrade = vzorec_nagrad.search(book)
    if nagrade:
        knjiga['nagrade'] = izloci_nagrade(nagrade['nagrade'])
    else:
        knjiga['nagrade'] = None


    return knjiga


def obdelaj_knjige(st_knjige):
    ime_datoteke = f'zajeti-podatki/knjige/knjiga-{st_knjige}.html'
    vsebina = orodja.vsebina_datoteke(ime_datoteke)
    yield izloci_podatke_knjige(vsebina)


def obdelaj_glavna_stran(st_strani):
    ime_datoteke = f'zajeti-podatki/najboljse-knjige-{st_strani}.html'
    vsebina = orodja.vsebina_datoteke(ime_datoteke)
    for blok in vzorec_bloka.finditer(vsebina):
        yield izloci_podatke_ocen_in_glasov(blok.group(0))



def izloci_gnezdene_podatke(knjige):
    osebe, nagrade, zanri, avtorji = [], [], [], []
    videne_osebe = set()

    def dodaj_osebo(knjiga, oseba):
        if oseba['id_osebe'] not in videne_osebe:
            videne_osebe.add(oseba['id_osebe'])
            osebe.append(oseba)
        avtorji.append({
            'knjiga': knjiga['id'],
            'oseba': oseba['id_osebe'],
        })


    for knjiga in knjige:
        for zanr in knjiga.pop('zanri'):
            zanri.append({'knjiga': knjiga['id'], 'zanr': zanr})
        if knjiga['nagrade']:
            for nagrada in knjiga.pop('nagrade'):
                nagrade.append({'knjiga': knjiga['id'], 'nagrada': nagrada})
        else:
            nagrade.append({'knjiga': knjiga['id'], 'nagrada' : None})
            knjiga.pop('nagrade')
        for oseba in knjiga.pop('avtor'):
            dodaj_osebo(knjiga, oseba)
            

    osebe.sort(key=lambda oseba: oseba['id_osebe'])
    avtorji.sort(key=lambda avtor: (avtor['oseba']))

    return osebe, zanri, nagrade, avtorji







knjige = []
count = 1
for st_strani in range(1, 6):
    for blok in obdelaj_glavna_stran(st_strani):
        for knjiga in obdelaj_knjige(count):
            knjige.append(knjiga)
            knjige[count - 1]['glasovi'] = blok['glasovi']
            knjige[count - 1]['score'] = blok['score']
        count += 1

knjige.sort(key=lambda knjiga: knjiga['id'])

orodja.zapisi_json(knjige, 'obdelani-podatki/knjige.json')

osebe, zanri, nagrade, avtorji = izloci_gnezdene_podatke(knjige)

orodja.zapisi_csv(knjige, ['id', 'naslov', 'dolzina', 'leto', 'leto_original', 'score', 'glasovi', 'avgrating', 'ratings', 'reviews'], 'obdelani-podatki/knjige.csv')
orodja.zapisi_csv(osebe, ['id_osebe', 'ime', 'starost', 'leto_rojstva'], 'obdelani-podatki/osebe.csv')
orodja.zapisi_csv(nagrade, ['knjiga', 'nagrada'], 'obdelani-podatki/nagrade.csv')
orodja.zapisi_csv(zanri, ['knjiga', 'zanr'], 'obdelani-podatki/zanri.csv')
orodja.zapisi_csv(avtorji, ['knjiga', 'oseba'], 'obdelani-podatki/avtorji.csv')
