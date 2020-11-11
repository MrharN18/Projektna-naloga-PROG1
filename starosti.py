import re
import orodja
import datetime


def izracun_starosti(datoteka):

    vzorec_rojstva = re.compile(
        r'<div class="dataItem" itemprop=\'birthDate\'>.*?(?P<birth_month>\w.*?)\W(?P<birth_day>\d{1,2}).*?(?P<birth_year>\d{3,4}).*?',
        flags=re.DOTALL
    )


    vzorec_smrti = re.compile(
        r'<div class="dataItem" itemprop=\'deathDate\'>(?P<death_month>\w.*?)\W(?P<death_day>\d{1,2}).*?(?P<death_year>\d{3,4})</div>',
        flags=re.DOTALL
    )

    vsebina = orodja.vsebina_datoteke(datoteka)

    rojstvo = re.search(vzorec_rojstva, vsebina)
    if rojstvo:
        mesec_rojstva = rojstvo.group(1)
        if mesec_rojstva == 'January': mesec_rojstva = 1  
        elif mesec_rojstva == 'February': mesec_rojstva = 2
        elif mesec_rojstva == 'March': mesec_rojstva = 3
        elif mesec_rojstva == 'April': mesec_rojstva = 4
        elif mesec_rojstva == 'May': mesec_rojstva = 5
        elif mesec_rojstva == 'June': mesec_rojstva = 6
        elif mesec_rojstva == 'July': mesec_rojstva = 7
        elif mesec_rojstva == 'August': mesec_rojstva = 8
        elif mesec_rojstva == 'September': mesec_rojstva = 9
        elif mesec_rojstva == 'October': mesec_rojstva = 10
        elif mesec_rojstva == 'November': mesec_rojstva = 11
        elif mesec_rojstva == 'December': mesec_rojstva = 12
        dan_rojstva = int(rojstvo.group(2))
        leto_rojstva = int(rojstvo.group(3))
    else: 
        return None, None

# Ce so avtorji ze umrli, starost predstavlja starost, ko so umrli.

    smrt = re.search(vzorec_smrti, vsebina)
    if smrt:
        mesec_smrti = smrt.group(1)
        if mesec_smrti == 'January': mesec_smrti = 1  
        elif mesec_smrti == 'February': mesec_smrti = 2
        elif mesec_smrti == 'March': mesec_smrti = 3
        elif mesec_smrti == 'April': mesec_smrti = 4
        elif mesec_smrti == 'May': mesec_smrti = 5
        elif mesec_smrti == 'June': mesec_smrti = 6
        elif mesec_smrti == 'July': mesec_smrti = 7
        elif mesec_smrti == 'August': mesec_smrti = 8
        elif mesec_smrti == 'September': mesec_smrti = 9
        elif mesec_smrti == 'October': mesec_smrti = 10
        elif mesec_smrti == 'November': mesec_smrti = 11
        elif mesec_smrti == 'December': mesec_smrti = 12
        dan_smrti = int(smrt.group(2))
        leto_smrti = int(smrt.group(3))

        if mesec_smrti > mesec_rojstva:
            starost = leto_smrti - leto_rojstva
        elif mesec_smrti == mesec_rojstva:
            if dan_smrti > dan_rojstva:
                starost = leto_smrti - leto_rojstva
            else:
                starost = leto_smrti - leto_rojstva - 1
        else:
            starost = leto_smrti - leto_rojstva - 1
        

    else:
        date = str(datetime.datetime.today()).split()[0].split('-')
        leto, mesec, dan = int(date[0]), int(date[1]), int(date[2])

        if mesec >= mesec_rojstva:
            starost = leto - leto_rojstva
        elif mesec == mesec_rojstva:
            if dan >= dan_rojstva:
                starost = leto - leto_rojstva
            else:
                starost = leto - leto_rojstva - 1
        else:
            starost = leto - leto_rojstva - 1

    return leto_rojstva, abs(starost)
