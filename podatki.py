import podatki_priprava as pod

def main(redownload=True,):
    for i in range(20):
        url = f"https://www.studentski-servis.com/studenti/prosta-dela?scrolltop=1&kljb=&page={i + 1}&isci=1&sort=&dm1s=1&hourlyratefrom=6.2&hourlyrateto=21&hourly_rate=6.2%3B21"
        if (redownload):
            pod.save_frontpage(url, "podatki.html", f"podatki{i + 1}.html")
    besedilo = ""
    for i in range(20):
        besedilo += pod.datoteka_v_niz("podatki.html", f"podatki{i + 1}.html")
    oglasi = pod.besedilo_v_oglase(besedilo)
    ads = [pod.podatki(oglas) for oglas in oglasi]
    pod.oglasi_v_csv(ads, "podatki.csv", "podatki.csv")

        
if __name__ == '__main__':
    main()

