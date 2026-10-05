import csv


def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    album = [] #struttura che conterrà tutte le foto dell'album
    try:
        with open(file_path,"r",encoding="utf-8") as csvFile: #evita .close()
            csv_reader = csv.reader(csvFile) #legge il file per intero
            header = next(csv_reader) #intestazione del ccsvFile
            for row in csv_reader:
                if not row or len(row) < 5: #evita la prima riga e se per caso avessimo più campi inseriti
                    continue
                codice, titolo, autore, mese, anno = ( #uso strip per togliere tutto ciò che non è un char
                    row[0].strip(), row[1].strip(), row[2].strip(),
                    int(row[3].strip()), int(row[4].strip()),
                )
                # struttura che contiene le singole foto
                foto = {"Codice": codice, "Titolo":titolo, "Autore":autore, "Mese":mese, "Anno":anno }
                album.append(foto) #popola l'album
        return album
    except FileNotFoundError:
        return None

def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    if mese < 1 or mese > 12: #controlli generali
        return None
    for foto in album:
        if foto["Codice"] == codice: #controlli generali
            return None
    fotoNuova = {"Codice":codice, "Titolo":titolo, "Autore":autore,"Mese":mese, "Anno":anno}

    try:
        with open(file_path, "a", newline="", encoding="utf-8") as csvFile:
            csvWriter = csv.writer(csvFile) #è una funzione che converte ciò che passi in un oggetto
            csvWriter.writerow([codice,titolo,autore,mese,anno]) #scrive la riga

        album.append(fotoNuova)
        return fotoNuova
    except FileNotFoundError:
        return None


def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    for foto in album: #itera per elemento del dizionario
        if foto["Codice"] == codice:
            return f"{foto['Codice']}, {foto['Titolo']}, {foto['Autore']}, {foto['Mese']}, {foto['Anno']}"
        return None


def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    titoli = [] #lista con i titoli delle foto di un certo anno
    for foto in album:
        if foto["Anno"] == anno:
            titoli.append(foto["Titolo"])
    return sorted(titoli) #ordinamento ASC senza specifica



def main():
    album = []
    file_path = "album_fotografico.csv"
    #prova = "prova" #prova di commit
    '''
    album = carica_da_file(file_path) #prove generali funzioni
    #print(album)
    titoli = elenco_foto_anno_per_titolo(album, 2019) #prove generali funzioni
    #print(titoli)
    fotoNuova = aggiungi_foto(album,"C400","Blu","Me",11,2019,file_path)
    print(fotoNuova)
    '''
    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo (Iniziale con la maiuscola): ").strip() #se no storta la funzione sorted
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")

if __name__ == "__main__":
    main()
