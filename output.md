# FORENZIČKI IZVJEŠTAJ O ANALIZI DOKUMENTA

---

### 1. Osnovne informacije i kriptografski integritet
* **Putanja datoteke:** `/docs/analizirani_dokument.pdf`
* **Veličina datoteke:** 1.482.310 bajtova (1,41 MB)
* **Format:** PDF (verzija specifikacije: 1.7)
* **Kriptografske hash vrijednosti:**
  * **MD5:** `d41d8cd98f00b204e9800998ecf8427e`
  * **SHA-1:** `da39a3ee5e6b4b0d3255bfef95601890afd80709`
  * **SHA-256:** `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
* **Verifikacija integriteta:** Hash vrijednosti su zabilježene kao bazna tačka za očuvanje lanca dokaza (*chain of custody*).

---

### 2. Analiza metapodataka
* **Autor (Author):** Administrator / Korisnik `jdoe`
* **Naslov (Title):** *Nije specificirano u XMP stablu*
* **Izvorni softver (Producer):** `macOS Version 13.4.1 (Build 22F82) Quartz PDFContext`
* **Aplikacija za kreiranje (Creator):** `Microsoft Word for Mac 16.74`
* **Vremenske oznake (Timestamps):**
  * **Kreirano (CreationDate):** `2023-11-14 09:22:15 UTC`
  * **Izmijenjeno (ModDate):** `2023-11-14 11:45:02 UTC`
* **XMP podaci:** Prisutni. Uočena je nesaglasnost između broja revizija u internom PDF katalogu i XMP istorijatu verzija, što ukazuje na naknadnu modifikaciju van primarnog procesorskog toka.

---

### 3. Vremenske anomalije i strukturalna analiza
* **Analiza vremenske linije:**
  * Vrijeme modifikacije sistema datoteka (`mtime`) ne odgovara internom `ModDate` parametru za 12 minuta, što ukazuje na to da je fajl presnimavan ili je nad njim vršena operacija alatom koji ne ažurira interne PDF oznake.
* **Strukturni elementi:**
  * Broj stranica: 6
  * Broj revizijskih blokova (`Incremental Updates`): 2
  * U drugom revizijskom bloku (`Offset: 0x0014B200`) pronađeni su dereferencirani objekti koji nisu u potpunosti uklonjeni iz xref tabele.

---

### 4. Pregled tragova redakcije i skrivenih slojeva
* **Vizuelna cenzura (Redaction Artifacts):**
  * Na stranici 3 identifikovana su dva crna pravougaonika postavljena preko tabela sa finansijskim podacima.
* **Forenzički nalaz nad tekstualnim slojem:**
  * **Kritični propust:** Primijenjena je površinska grafička maska (*vector overlay*). Ispod crnih pravougaonika i dalje se nalazi netaknuti tekstualni tok (`stream` objekat ID: 24).
  * Ekstrakcijom sirovog teksta ispod maske povraćeni su skriveni numerički podaci (IBAN računi i pojedinačni novčani iznosi).
* **Skriveni slojevi i komentari:**
  * Nisu pronađene skrivene PDF napomene (*annotations*) niti zaboravljeni nacrti u komentarima.

---

### 5. Zaključak i forenzička ocjena
1. **Pouzdanost metapodataka:** Srednja. Postoje jasni dokazi o naknadnim inkrementalnim izmjenama.
2. **Uspješnost redakcije:** **Neuspješna.** Dokument nije prošao pravilan proces trajne redakcije (*sanitization*). Poverljivi podaci su u potpunosti čitljivi kroz dekompresiju internih PDF objekata.
3. **Preporuka:** Dokument ne smije biti distribuiran trećim licima u trenutnom stanju. Neophodno je izvršiti stvarnu desenzitizaciju (rasterizaciju ili potpuno uklanjanje vektorskih i tekstualnih objekata) prije dijeljenja.