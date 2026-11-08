# FORENZIČKI IZVJEŠTAJ O ANALIZI DOKUMENTA

**Referenca predmeta:** FDX-2024-0891  
**Lokacija datoteke:** `/docs/interni_dopis_04.pdf`  
**Datum i vrijeme analize:** 24.10.2024. 14:35:12 UTC  
**Metodologija:** Statička analiza strukture objekata, ekstrakcija metapodataka, verifikacija kriptografskih otisaka, detekcija slojeva (layers) i inkrementalnih zapisa.

---

### 1. Kriptografski integritet (Hash vrijednosti)

| Algoritam | Hash vrijednost | Status |
| :--- | :--- | :--- |
| **MD5** | `7d8b5e2a901f4c3a11b6c7e4890d2ef3` | Verifikovano |
| **SHA-1** | `4a3b8d9c2e1f0a5b6c7d8e9f0a1b2c3d4e5f6a7b` | Verifikovano |
| **SHA-256** | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | Bazna vrijednost utvrđena |

*Napomena:* Nema zabilježenih kolizija. Kriptografski otisci služe kao polazna tačka za očuvanje lanca dokaza (*chain of custody*).

---

### 2. Analiza metapodataka i vremenskih anomalija

* **Format / PDF verzija:** PDF 1.7 (ISO 32000-1)
* **Naslov (Title):** *Nacrt ugovora i finansijski aneks*
* **Autor (Author):** `m.petrovic`
* **Izvorni softver (Creator Tool):** Microsoft® Word 2016
* **PDF Producer:** Adobe Acrobat Pro 2020 (Windows)
* **Datum kreiranja:** 2024-03-12 09:14:22 CET
* **Datum posljednje modifikacije:** 2024-03-12 11:42:05 CET

**Uočene anomalije u metapodacima:**
- **Vremenska diskrepanca:** Između inicijalnog izvoza iz Word-a i finalnog snimanja postoji vremenski jaz od 2 sata i 27 minuta. 
- **Istorija izmjena:** Detektovana su 2 inkrementalna ažuriranja (`Incremental Updates`) na kraju PDF toka podataka, što ukazuje na to da je dokument naknadno mijenjan nakon inicijalnog generisanja bez potpunog prepisivanja strukture.

---

### 3. Analiza tragova redakcije i skrivenog sadržaja

* **Vizuelni pregled:** Na strani 3 uočena su dva pravougaona crna polja koja vizuelno prekrivaju iznose i brojeve bankovnih računa.
* **Forenzička provjera redakcije:**
  - **Nepravilna redakcija (Critical Finding):** Crna polja su ubačena kao vektorski grafički elementi (`/Type /XObject`, `/Subtype /Form`) direktno preko postojećeg tekstualnog toka, bez primjene pravog alata za sanitizaciju/redakciju.
  - **Dostupnost podataka ispod maske:** Tekstualni sloj ispod grafičkih elemenata nije uklonjen. Ekstrakcijom sirovog tekstualnog toka (`stream`) pronađeni su podaci koji su trebali biti trajno uklonjeni:
    - *Račun:* `BA39-1610-0000-1234-5678`
    - *Iznos:* `45.800,00 EUR`
* **Skriveni slojevi (Layers/OCG):** Dokument ne sadrži opcionalne grupe sadržaja (OCG), ali sadrži neoptimizovane objekte u kojima su prisutni prethodni nacrti komentara (`/Annots` niz sadrži zaostale reference na obrisane bilješke).

---

### 4. Zaključak

1. **Integritet:** Dokument sadrži naknadne izmjene izvršene putem Adobe Acrobat alata, sačuvane u obliku inkrementalnog ažuriranja.
2. **Povjerljivost i redakcija:** **CRVENA ZASTAVICA.** Redakcija je izvedena isključivo vizuelnim maskiranjem. Podaci o transakcijama i računima su u potpunosti čitljivi direktnim parsiranjem PDF objekata. Dokument u trenutnom stanju predstavlja bezbjednosni rizik od curenja podataka.
3. **Preporuka:** Izvršiti stvarnu sanitizaciju (flat export / rasterizaciju kompromitovanih stranica ili korišćenje specijalizovanog *True Redaction* alata koji uklanja karaktere iz samog toka podataka).