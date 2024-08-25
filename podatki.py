import requests
import re
import os
import csv

def url_v_niz(url):
    try:
        headers = {"User-agent" : "Chrome/111.05563.111"}
        spletna_stran= requests.get(url, headers=headers)
    except requests.exceptions.RequestException:
        print("Spletna stran je trenutno nedosegljiva")
        return None
    return spletna_stran.text

def niz_v_datoteko(tekst, directory, datoteka):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, datoteka)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(tekst)
    return None

def save_frontpage(spletna_stran, directory, datoteka):
    vsebina = url_v_niz(spletna_stran)
    niz_v_datoteko(vsebina, directory, datoteka)

def datoteka_v_niz(directory, datoteka):
    path = os.path.join(directory, datoteka)
    with open(path, "r", encoding='utf-8') as f:
        besedilo = f.read().replace("\n", " ")
    return besedilo

def besedilo_v_oglase(besedilo):
    vzorec = r'<article class="job-item" data-jobid=".*?VSTOPI IN SI POGLEJ VEČ</button>'
    return re.findall(vzorec, besedilo, flags=re.DOTALL)

def podatki(oglas):
    delo = re.search(r'2">.+<h5 class="mb-0">(.*)</h5>', oglas)
    št_oglasa = re.search(r'<article class="job-item" data-jobid="(\d*)">', oglas)
    lokacija = re.search(r'icon-location"></use></svg>(\D*)</p>', oglas)
    plača_neto = re.search(r'<strong>([^-]*) €/h neto</strong>', oglas)
    plača_bruto = re.search(r'</strong> \((.*?) €/h bruto\)</a>', oglas)
    opis = re.search(r'<p class="description text-break">(.*?)</p>', oglas)
    prosta_mesta = re.search(r'Prosta mesta: <strong><!--sse-->(.*?)<!--/sse--></strong></li>', oglas)
    trajanje = re.search(r'<li>Trajanje: <strong><!--sse-->(.*?)<!--/sse--></strong></li>', oglas)
    delovnik =  re.search(r'<li>Delovnik: <strong><!--sse-->(.*?)<!--/sse--></strong></li>', oglas)
    začetek_dela = re.search(r'<li>Začetek dela: <strong><!--sse-->(.*?)<!--/sse--></strong></li>', oglas)
    if delo == None or št_oglasa == None:
        return None
    return {
    'delo': delo.group(1),
    'št_oglasa': št_oglasa.group(1),
    'lokacija': lokacija.group(1).strip() if lokacija else 'ni znano',
    'plača_neto[€/h]': float(plača_neto.group(1)) if plača_neto else "coerce",
    'plača_bruto[€/h]': float(plača_bruto.group(1)) if plača_bruto else "coerce",
    'opis': opis.group(1) if opis else '',
    'prosta_mesta': prosta_mesta.group(1) if prosta_mesta else '1',
    'trajanje': trajanje.group(1) if trajanje else 'po dogovoru',
    'delovnik': delovnik.group(1) if delovnik else 'po dogovoru',
    'začetek_dela': začetek_dela.group(1) if začetek_dela else 'po dogovoru'}

def ads_from_file(datoteka, directory):
    vsebina = datoteka_v_niz(directory, datoteka)
    oglasi = besedilo_v_oglase(vsebina)
    ads = [podatki(oglas) for oglas in oglasi]
    return [ad for ad in ads if ad != None]

def zapiši_csv(fieldnames, vrste, directory, datoteka):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, datoteka)
    with open(path, 'w', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for vrsta in vrste:
            writer.writerow(vrsta)
    return

def oglasi_v_csv(oglasi, directory, datoteka):
    fieldnames = list(oglasi[0].keys())
    zapiši_csv(fieldnames, oglasi, directory, datoteka)
    return None

def main(redownload=True,):
    for i in range(20):
        url = f"https://www.studentski-servis.com/studenti/prosta-dela?scrolltop=1&kljb=&page={i + 1}&isci=1&sort=&dm1s=1&hourlyratefrom=6.2&hourlyrateto=21&hourly_rate=6.2%3B21"
        if (redownload):
            save_frontpage(url, "podatki.html", f"podatki{i + 1}.html")
    besedilo = ""
    for i in range(20):
        besedilo += datoteka_v_niz("podatki.html", f"podatki{i + 1}.html")
    oglasi = besedilo_v_oglase(besedilo)
    ads = [podatki(oglas) for oglas in oglasi]
    oglasi_v_csv(ads, "podatki.csv", "podatki.csv")

        
if __name__ == '__main__':
    main()

