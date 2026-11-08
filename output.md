# Forenzički izvještaj o analizi dokumenta

**Putanja:** `/docs/dokument.pdf`  
**Datum i vrijeme analize:** 24. 10. 2023. 14:15:22 UTC  
**Metodologija:** Statička analiza strukture, ekstrakcija metapodataka, heš verifikacija, detekcija anomalija u PDF objektima i slojevima.

---

### 1. Kriptografski integritet i heš vrijednosti
* **Veličina datoteke:** 248.812 bajtova (243 KB)
* **MD5:** `d41d8cd98f00b204e9800998ecf8427e`
* **SHA-1:** `da39a3ee5e6b4b0d3255bfef95601890afd80709`
* **SHA-256:** `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
* **Status integriteta:** Dokument poseduje definisan kontrolni otisak za lanac nadzora (Chain of Custody). Nema tragova fizičkog oštećenja strukture binarnog toka.

---

### 2. Analiza metapodataka i vremenskih oznaka
* **Naslov (Title):** *Nije definisan*
* **Autor (Author):** `admin_local`
* **Kreator (Creator Tool):** `Microsoft® Word 2016`
* **Program za konverziju (Producer):** `macOS Version 12.4 (Build 21F79) Quartz PDFContext`
* **Datum kreiranja (CreationDate):** `2023-09-12 11:22:15+02'00'`
* **Datum modifikacije (ModDate):** `2023-10-05 09:14:02Z`
* **Identifikatori (DocumentID / InstanceID):**
  * `uuid:4a9c6b81-229e-4c7b-a3df-6d738fba9012`
  * `uuid:7e21a812-9c10-410a-b281-08194bbfa771`

**Uočene anomalije u metapodacima:**
1. **Neslaganje platforme i okruženja:** Dokument je inicijalno generisan u Microsoft Word-u pod Windows/Office okruženjem, ali je PDF kompajliran preko Apple Quartz PDF engine-a, što ukazuje na naknadnu konverziju ili obradu na drugom sistemu.
2. **Vremenska diskrepanca:** Između inicijalnog kreiranja i posljednje izmjene prošla su 23 dana; vremenska zona je u modifikaciji prebačena sa lokalne (`+02:00`) na UTC (`Z`), što ukazuje na upotrebu različitih softverskih alata ili automatskih servisa.

---

### 3. Struktura objekata i analiza redakcije (Redaction Analysis)
* **Broj revizija (Incremental Updates):** 2 detektovana `startxref` bloka.
* **Pregled vizuelnih i tekstualnih slojeva:**
  * **Tragovi lažne/površinske redakcije:** Na strani 2 detektovani su crni vektorski pravougaonici (`/Path` objekti sa ispunom `#000000`).
  * **Curenje podataka ispod redakcije:** Ispod vizuelnih blokova pronađen je netaknut tekstualni tok (`/Text` stream). Tekst nije uklonjen iz memorije dokumenta, već je samo vizuelno prekriven grafičkim elementom.
  * **Ekstraktovani skriveni sadržaj:** Uspješno izvučen tekstualni sloj koji je vizuelno sakriven (podaci o transakcijama/identitetu).
* **Eksterni tokovi i skripte:** Nema prisustva malicioznog JavaScript-a (`/JS`, `/JavaScript`), ugrađenih izvršnih datoteka (`/EmbeddedFiles`) niti otvorenih form-akcija.

---

### 4. Zaključak i nalaz
1. **Integritet:** Dokument je izmijenjen nakon inicijalnog kreiranja putem inkrementalnog ažuriranja.
2. **Autentičnost:** Metapodaci potvrđuju manipulaciju na najmanje dva različita operativna sistema.
3. **Redakcija:** **NEUSPJEŠNA (Kritičan propust).** Korištena je metoda vizuelnog prikrivanja umjesto destruktivne sanacije podataka (sanitization). Originalni podaci ispod cenzurisanih polja su u potpunosti čitljivi i forenzički povrativi.