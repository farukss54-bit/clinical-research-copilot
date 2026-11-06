---
name: sap-builder
description: Istatistiksel Analiz Plani (SAP) taslagi uretir - birincil/ikincil analiz yontemleri, ML model gelistirme/validasyon stratejisi, eksik veri yontemi ve uygun raporlama standardinin (STROBE/TRIPOD/TRIPOD-AI) secimini icerir. Kullanici "analiz plani", "SAP", "istatistiksel yontem", "modeli nasil valide ederim" dedi mi kullan.
---

# Istatistiksel Analiz Plani (SAP)

## Amac

Veri toplanmadan/analiz baslamadan ONCE, nasil analiz edilecegini onceden kilitlemek (outcome switching / p-hacking riskini azaltmak icin onemli) ve uygun bir raporlama standardina baglamak.

## Girdi

`research/<slug>/01_hypothesis.md`, `02_design_feasibility.md`, `03_sample_size.md`, `04_data_dictionary.md`.

## Adimlar

1. **Tanimlayici analiz plani**: hangi degiskenler nasil ozetlenecek (ortalama+SD / medyan+IQR / oran), grup karsilastirmalari icin hangi testler (dagilim varsayimlarina gore parametrik/non-parametrik).
2. **Birincil analiz**:
   - Klasik hipotez testi ise: hangi test, tek/cift yonlu, coklu karsilastirma duzeltmesi gerekip gerekmedigi.
   - Prediction/ML modeli ise: aday algoritmalar (orn. lojistik regresyon referans model + 1-2 ML algoritmasi — "once basit, sonra karmasik" ilkesi; sadece ML kullanip lojistik regresyonla karsilastirmamak ciddi bir metodolojik eksiklik olarak degerlendirilir), degisken secim yontemi (LASSO, klinik yargı, vb.), train/validation/test ayrimi (random split / temporal split / dis merkez validasyonu — hangisi mumkunse), performans metrikleri (AUC/discrimination + kalibrasyon egrisi/Brier skoru + klinik fayda icin decision curve analysis), model yorumlanabilirligi (SHAP vb.) planlaniyorsa belirt.
3. **Ikincil/alt grup analizleri**: onceden tanimla, sonradan "veriye bakip" eklenen alt grup analizlerini ayrica "kesif amacli/post-hoc" olarak isaretle.
4. **Eksik veri yontemi**: data-dictionary'deki stratejiyi burada formel hale getir (orn. coklu imputasyon kullanilacaksa kac imputasyon, hangi degiskenler dahil).
5. **Raporlama standardi sec ve gerekcelendir**:
   - Gozlemsel kohort/vaka-kontrol -> STROBE
   - Prediction model gelistirme/validasyon (klasik) -> TRIPOD
   - ML tabanli prediction model -> TRIPOD-AI (veya PROBAST ile bias riski degerlendirmesi)
   - Tani dogrulugu -> STARD
   Secilen checklist'in ana basliklarini kisaca listele, calisma onlari karsilayacak sekilde tasarlanmali.
6. Analiz icin kullanilacak yazilim/kutuphane (R/Python, hangi paketler) belirt — kullanicinin "amator ama AI araci kullanirim" seviyesine uygun, asiri karmasik olmayan bir araç seti oner.
7. `biostatistics-reviewer` alt-agent incelemesini oner/calistir.

## Cikti

`research/<slug>/05_sap.md`:
- Tanimlayici analiz plani
- Birincil analiz (yontem + gerekce)
- Ikincil/alt grup analizler (onceden tanimli vs kesif amacli ayrimi)
- Eksik veri yontemi
- Secilen raporlama standardi + ana baslik kontrol listesi
- Onerilen yazilim/arac seti
- Biyoistatistikci inceleme sonucu (varsa)

## Kalite kontrolu

- SAP, veri toplanmadan/analiz yapilmadan once yazilmis olmali (post-hoc SAP, sonuclarin guvenilirligini azaltir) — bunu kullaniciya hatirlat.
- ML modeli iceren her SAP'ta MUTLAKA kalibrasyon + dis/zamansal validasyon planindan bahsedilmeli; sadece AUC raporlamayi yeterli gorme.
