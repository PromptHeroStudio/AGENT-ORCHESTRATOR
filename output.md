### IZVJEŠTAJ O FORENZIJSKOJ ANALIZI DOKUMENATA

**Status:** ❌ **NEMOGUĆE IZVRŠITI ODGOVARAĆU ANALIZU**

⚠️ **Ograničena funkcionalnost:** Kao AI asistent, **nemam direktan pristup** vašem lokalnom sistemu fajlova, mреžovim mapama (npr. `/docs`) ili hardverskom skladištu podataka. Alati `read_files` i `analyze_metadata` ne mogu se pokrenuti bez da mi se dostavi **sadržaj samog dokumenta** ili **binarna podataka** unutar ove razgovorne sesije.

---

#### 1. Metapodaci
- **Dostupnost:** ⚠️ Nesigurno / Nedostupno
- **Analiza:** Bez pristupa fajlu, nisam u mogućnosti izvaditi meta-podatuće kao što su:
  - `Creation Date` (Datum kreiranja)
  - `Modification Date` (Datum posljednje izmjene)
  - `Author` (Autor/Definicija korisnika)
  - `Last Modified By`
  - `Application Version` (npr. MS Word, PDF producer)
- **Napomena:** Metapodaci često otkrivaju diskrepancije (npr. datum kreiranja kasniji od datuma objave ili autor različite od najave).

#### 2. Hash Vrijednosti (SHA-256 / MD5)
- **Dostupnost:** ⚠️ Nesigurno / Nedostupno
- **Analiza:** Ne mogu izračunati kriptografski potpis (hash) bez pristupa sirovim bajtovima fajla.
- **Značaj:** Hash vrijednost je ključna za:
  - Verifikaciju integriteta (da li je datoteka zamijenjena ili oštećena).
  - Usporedbu sa izvornim primjerkom.

#### 3. Tragovi Redakcije i Struktura
- **Dostupnost:** ⚠️ Nesigurno / Nedostupno
- **Analiza:** Bez sadržaja, ne mogu analizirati:
  - **Skriti slojevi:** Tekst iza slike, bijeli tekst na bijeloj pozadini.
  - **Izmjene XML strukture:** Kod Word-a (.docx), pregledanje `document.xml` za obrisane rečenice ili promjene formatiranja.
  - **Metadata XML:** `core.xml` i `app.xml` u OOXML fajlovima.
  - **PDF specifičnosti:** Ovdje bih tražio `XMP` podatke, rotacija stranica, skriveni tekstovi (`Visible` = false) i logičke greške u vremenskoj osi PDF strukture.

---

#### 📌 Preporuka za nastavak

Da bih izvršio realnu forenzičku analizu, molim vas da uradite jedno od sljedećeg:

1. **Naljepite tekst dokumenta** direktno u chat (ako je tekstualan).
2. **Naljepite izlaz alata** kao što su:
   - Rezultat `exiftool document.pdf`
   - Rezultat `sha256sum document.pdf`
   - Rezultat `strings document.docx` (za Word fajlove)
3. **Objasnite kontekst:** Koje tipove anomalija sumnjičite? (npr. namjerno promijenjen datum, dodavan na dokument kasnije, skriveni tekst).

Kada mi dostavite navedene podatke, odmah ću generisati detaljan technicalni izveštaj o integritetu i poreklu.