---
name: data-dictionary-crf
description: Degisken listesinden bir veri sozlugu / vaka rapor formu (CRF) tasligi uretir; her degiskenin tanimi, kaynak (yapilandirilmis alan mi serbest metin mi), kodlama semasi ve eksik veri stratejisini belirler. Serbest metinden veri cikarimi icin (manuel veya AI-destekli) bir abstraksiyon protokolu onerir. Kullanici "veri sozlugu", "CRF", "degiskenleri kodlayalim", "serbest metinden nasil cikaririm" dedi mi kullan.
---

# Veri Sozlugu / CRF Tasarimi

## Amac

Analiz edilebilir, tutarli, baska bir arastirmaciya (veya biyoistatistikciye) devredilebilir bir veri seti tanimi uretmek — ozellikle serbest metin kaynakli degiskenler icin sistematik bir cikarim protokolu kurmak.

## Girdi

`research/<slug>/02_design_feasibility.md` (degisken listesi ve her birinin yapilandirilmis/serbest-metin durumu).

## Adimlar

1. Her degisken icin bir satir olusturacak sekilde tabloyu kur: **Degisken adi | Tanim | Veri tipi (surekli/kategorik/binary) | Kaynak (HBYS alani adi / serbest metin / harici kayit) | Kodlama (orn. 0=yok,1=var; kategoriler) | Eksik veri kodu/stratejisi**.
2. **Serbest metin degiskenler** icin ozel bir abstraksiyon protokolu yaz:
   - Hangi not turunden (triyaj notu, nöroloji konsultasyon notu, radyoloji raporu) cikarilacagi
   - Cikarim kurali acik ve tekrarlanabilir olmali (orn. "NIHSS notta aciksa al, yoksa 'kayitli degil' olarak isaretle — tahmin etme")
   - Yontem secimi: (a) tamamen manuel abstraksiyon (altin standart, zaman maliyetli) vs (b) AI/LLM destekli yari-otomatik cikarim + bir alt-ornekte (orn. 50-100 kayit) manuel dogrulama ile uyum/dogruluk olcumu (bu kendisi metodolojik bir not olarak SAP'a tasinmali: "LLM-destekli cikarimin X alt-orneginde manuel ile uyumu Y% bulundu").
   - AI destekli cikarim seciliyorsa: hangi modelin kullanildigi, prompt'un nasil standartlastirildigi ve dogrulama sonucu ACIKCA raporlanmali (reprodubilite icin).
3. Eksik veri icin genel strateji belirle (complete-case vs imputation vs "eksiklik kendisi bir kategori") — SAP fazinda detaylandirilacagini not et.
4. Kodlama semasinin ileride ML modeline girdi olacak degiskenler icin uygun formatta (one-hot/ordinal/surekli) oldugunu kontrol et.
5. KVKK/anonimlik: veri setinde dogrudan tanimlayici olmadigini, calisma-spesifik ID kullanildigini dogrula.

## Cikti

`research/<slug>/04_data_dictionary.md`:
- Tam degisken tablosu (yukaridaki kolonlarla)
- Serbest metin abstraksiyon protokolu (yontem + varsa AI-destekli dogrulama plani)
- Eksik veri genel stratejisi
- KVKK/anonimlik notu

## Kalite kontrolu

- Her degiskenin kodlamasi, SAP'ta kullanilacak istatistiksel/ML yontemle uyumlu olmali (orn. surekli degiskeni gereksiz yere kategorize etmemek, bilgi kaybini onlemek).
- AI-destekli cikarim oneriliyorsa, dogrulanmamis/tek basina kullanimini onermeyecek kadar temkinli ol — mutlaka bir manuel dogrulama alt-ornegi iste.
