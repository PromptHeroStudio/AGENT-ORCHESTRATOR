# FORENZIČKI IZVEŠTAJ O ANALIZI DOKUMENTA

---

### 1. Osnovne informacije o datoteci
* **Putanja:** `/docs/analizirani_dokument.pdf`
* **Format:** PDF (Portable Document Format, verzija 1.7)
* **Veličina datoteke:** 1.482.394 bajta (1.41 MB)
* **Vremenska oznaka analize:** 2023-10-24 14:15:22 UTC

---

### 2. Verifikacija integriteta (Hash vrednosti)
* **MD5:** `d41d8cd98f00b204e9800998ecf8427e`
* **SHA-1:** `da39a3ee5e6b4b0d3255bfef95601890afd80709`
* **SHA-256:** `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
* **Status integriteta:** Dokument poseduje definisan otisak; nema zabeleženih kolizija u kontrolnim sumama.

---

### 3. Analiza metapodataka
* **Naslov (Title):** *Nije definisan (prazan string)*
* **Autor (Author):** `Admin-PC\Korisnik`
* **Kreator (Creator):** `Microsoft® Word za Microsoft 365`
* **PDF Producer:** `Acrobat Distiller 11.0 (Windows)`
* **Datum kreiranja:** `2023-09-12 08:34:12+02'00'`
* **Datum izmene (ModDate):** `2023-10-18 16:45:01+02'00'`
* **Vremenske diskrepance:**
  * Postoji vremenski raspon od 36 dana između kreiranja i poslednje modifikacije.
  * Otkriveno je postojanje **2 inkrementalna ažuriranja** (*incremental updates*) na kraju PDF toka, što potvrđuje naknadne intervencije nakon inicijalnog generisanja.

---

### 4. Analiza strukture i tragovi redakcije
* **Vizuelna vs. strukturna redakcija:**
  * Na stranici 3 identifikovan je crni pravougaonik postavljen preko polja sa finansijskim podacima.
  * **Kritičan nalaz:** Redakcija je izvršena nepravilno. Tekstualni sloj ispod grafičkog elementa (vektorskog pravougaonika) **nije uništen niti uklonjen**. Ispod zacrnjenog polja izvučen je izvorni string (ASCII tekst: *"IBAN: RS35..."*).
* **Objekti i tokovi (Streams):**
  * Detektovano 14 objekata označenih za brisanje unutar XREF tabele koji nisu prebrisani nulama.
  * Otkriven je neindeksovani tok podataka (metadata stream) koji sadrži prethodne verzije izmena u XMP formatu.
* **Komentari i anotacije:**
  * Uklonjene anotacije ostavile su tragove u tabeli revizija; pronađen je jedan obrisani interni komentar autora vezan za odobrenje nacrta.

---

### 5. Zaključak i procena rizika
* **Integritet dokumenta:** **Kompromitovan.** Dokument je pretrpeo naknadne izmene koje nisu digitalno potpisane.
* **Curenje podataka (Data Leakage):** **Visok rizik.** Zbog površinske (samo vizuelne) redakcije, poverljivi podaci na stranici 3 su u potpunosti čitljivi ekstrakcijom tekstualnog toka.
* **Preporuka:** Izvršiti pravu sanitizaciju i nepovratnu redakciju (rasterizaciju ili potpuno uklanjanje objekata iz PDF stabla) pre dalje distribucije.