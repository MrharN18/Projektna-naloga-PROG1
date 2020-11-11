Projektna-naloga-PROG1
======================

## Najboljše knjige

Analiziral bom prvih _500 knjig_ na strani [goodreads](https://www.goodreads.com/list/show/1.Best_Books_Ever?page=1). Knjige bodo razvrščene glede na število točk (score), ki je izračunano iz števila glasov (votes) in iz podatka, kako visoko na seznam so te knjige uvrstili glasovalci. `(število točk se nanaša na ta specifičen seznam)`

#### V podatkih bom zajel:
* Naslov knjige in avtorja
* leto izida izdaje ter leto izida originala
* število strani, žanre
* povprečno oceno knjige (average rating) in število ocen (ratings) 
* število točk in število glasov
* literarne nagrade


#### Delovne hipoteze:
* Ali imajo knjige s 300 in manj stranmi višje število točk in višjo povprečno oceno?
* Ali obstaja povezava med številom glasov in številom prejetih nagrad? 
* Povprečna starost avtorjev, ko je njihova uspešnica izšla, je višja od 40 let.
* Ali ljudje raje berejo fantazijo kot klasiko?
* Cena knjige je višja, če ima knjiga višjo oceno.


#### Zajeti podatki:
V mapi obdelani-podatki je pet csv in ena json datoteka:
* datoteka avtorji.csv vsebuje id avtorja in id knjige, ki jo je ta avtor napisal
* datoteka knjige.csv vsebuje vse podatke o knjigi, ki so našteti zgoraj
* datoteka osebe.csv vsebuje id avtorja, njegovo ime ter leto rojstva in starost avtorja
* datoteka zanri.csv vsebuje vse žanre posameznih knjig
* datoteka nagrade.csv vsebuje vse nagrade, ki jih je posamezna knjiga prejela

Ker sem podatke zajel sam, so vključene tudi skripte za zajem in obdelavo podatkov. V datoteko starosti.py sem napisal še funkcijo za izračun starosti avtorja iz podatkov o letu rojstva, če so ti bili podani na spletni strani.
