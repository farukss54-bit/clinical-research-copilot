---
name: sample-size-power
description: Calisma tasarimi ve degisken listesi belli olduktan sonra orneklem buyuklugu/istatistiksel guc hesabi yapar. Klasik hipotez testleri icin standart guc hesabi, ML/prediction model calismalari icin events-per-variable (EPV) ve kalibrasyon-odakli ornekleme kurallarini kullanir. Kullanici "orneklem buyuklugu", "guc hesabi", "kac hasta gerekli", "power analysis" dedi mi kullan.
---

# Orneklem Buyuklugu / Guc Hesabi

## Amac

"Kac hastaya ihtiyacim var" sorusuna, calisma tipine uygun ve savunulabilir bir yontemle cevap vermek; ayrica mevcut/erisilebilir vaka hacmiyle bu hedefin gercekci olup olmadigini karsilastirmak.

## Girdi

`research/<slug>/02_design_feasibility.md` (tasarim tipi, birincil outcome, yillik vaka hacmi tahmini).

## Adimlar

1. **Calisma tipine gore yontem sec**:
   - Klasik karsilastirma (iki grup ortalama/oran farki): standart guc hesabi — beklenen etki buyuklugu (literaturden veya kucuk bir pilot veriden), alfa (genelde 0.05), guc (genelde 0.80-0.90), tek/cift yonlu test.
   - Prediction/ML modeli gelistirme: EPV kurali (nadir olay sayisina gore en az 10-20 olay/degisken), tercihen formel bir hesaplama mantigi (orn. pmsampsize yaklasimindaki gibi: hedef shrinkage faktoru, beklenen C-istatistigi/R2, outcome prevalansi dikkate alinarak). Sadece "kabaca 10xdegisken" demekle sinirli kalma; literatur taramasindaki benzer calismalarin orneklem/olay sayilarini da referans goster.
   - Dis validasyon / tani dogrulugu calismalari icin ilgili ozel formuller (sensitivite/spesifisite hedef genislik) kullan.
2. Hesabi ADIM ADIM goster (girdi degerler + formul/mantik + sonuc) — kullanici kontrol edebilsin ve gerekirse biyoistatistikçiye gosterebilsin.
3. Beklenen eksik veri/disli tutma oranini (orn. %10-20) hesaba katarak HEDEF orneklemi biraz yukari duzelt.
4. Mevcut yillik vaka hacmi ve retrospektif pencere ile bu hedefin ne kadar surede/kac yilda karsilanacagini hesapla; eger kullanicinin hastanesi yuksek hacimli ise (tromboliz+trombektomi gibi) bunu acikca olumlu bir fizibilite notu olarak isaretle.
5. Belirsizlik/varsayimlari acikca listele (orn. "etki buyuklugu X calismasindan alindi, kendi populasyonunda farkli olabilir").
6. Sonucu, `research-advisor` araciligiyla `biostatistics-reviewer` alt-agent'ina gozden gecirtmeyi oner (ozellikle ML/prediction model hesaplarinda EPV ve kalibrasyon pek cok arastirmaci tarafindan atlanir).

## Cikti

`research/<slug>/03_sample_size.md`:
- Secilen yontem ve gerekcesi
- Adim adim hesap (girdi -> formul/mantik -> sonuc)
- Eksik veri duzeltmesiyle nihai hedef orneklem
- Mevcut vaka hacmiyle karsilastirma / sureye donusturme
- Varsayimlar ve belirsizlikler
- Biyoistatistikci incelemesi onerisi/sonucu (varsa)

## Kalite kontrolu

- Asla "yeterli olur" gibi gerekcesiz bir sayi uretme; her sayinin bir kaynagi/mantigi olmali.
- Klasik test ile prediction model mantigini birbirine karistirma — hangisi kullaniliyorsa onun kendi kurallarini uygula.
- ML modeli soz konusuysa, SADECE EPV'ye bakip kalibrasyon/dis validasyon ihtiyacini atlama; bunu SAP fazina (05_sap.md) acik bir not olarak tasiyacagini belirt.
