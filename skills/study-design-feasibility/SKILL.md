---
name: study-design-feasibility
description: Hipotez/soru netlestikten sonra uygun calisma tasarimini (kohort, vaka-kontrol, kesitsel, prediction model gelistirme vb.) secer, degisken listesini (exposure/outcome/confounder) cikarir ve en onemlisi FIZIBILITE denetimi yapar (hangi veri HBYS'de var, hangisi serbest metinde, zaman damgalari guvenilir mi, orneklem yeterli mi). Kullanici "tasarim secelim", "fizibilite", "hangi veri gerekli", "bu yapilabilir mi" dedi mi kullan.
---

# Calisma Tasarimi ve Fizibilite Denetimi

## Amac

Soyut hipotezi, GERCEKTEN yurutulebilir bir plana donusturmek. Bu fazin basarisizligi (fizibilite sorunlari gec fark edilirse) projenin en pahali hatasidir — bu yuzden bu skill agirlikli olarak SORU SORMAYA ve mevcut veriyi denetlemeye odaklanir, hemen cozum uretmeye degil.

## Girdi

`research/<slug>/01_hypothesis.md`.

## Adimlar

1. **Tasarim tipini sec** ve gerekcelendir: retrospektif kohort / vaka-kontrol / kesitsel / prognostik-prediction model gelistirme / tani dogrulugu / sistematik derleme. ML tabanli prediction model calismalari genelde retrospektif kohort + model gelistirme+validasyon seklindedir; bunu acikca belirt.
2. **Degisken listesi** cikar: outcome(lar), ana exposure/predictor(ler), bilinen confounder'lar (literatur taramasindan), demografik/klinik kovaryatlar.
3. **Fizibilite denetimi** — kullaniciya asagidaki sorulari sor (cevaplari biliyorsa direkt iste, bilmiyorsa kucuk bir pilot chart review onerisiyle devam et):
   - Her degisken HBYS'de YAPILANDIRILMIS bir alanda mi, yoksa serbest metinde mi? Serbest metindekiler icin cikarim stratejisi gerekecek (manuel abstraksiyon formu veya AI-destekli cikarim + dogrulama alt-ornegi) — bunu simdi isaretle, detayini data-dictionary-crf fazinda cikar.
   - Kritik zaman damgalari (varsa) otomatik sistem kaydi mi (PACS/HBYS log) yoksa elle girilen mi?
   - Outcome olcumu icin takip suresi gercekci mi (kullanicinin daha once belirttigi kisitlari — orn. "90 gun imkansiz" — burada uygula, in-hospital/taburculuk alternatiflerine don)?
   - Yillik vaka hacmi ve mevcut retrospektif pencere, hedeflenen orneklem buyuklugune (sonraki fazda kesinlesecek ama kaba bir tahmin simdi yap) yeterli mi?
   - Dahil etme/disli tutma kriterleri, secim yanliligi yaratacak sekilde daraltiliyor mu (methodology-critic'in sonra bakacagi bir konu ama ilk isaretleme burada)?
   - Tek merkez mi coklu merkez mi; coklu merkezse veri uyumlulugu/standardizasyon sorunu var mi?
4. Yukaridaki denetimde ciddi bir engel (orn. kritik outcome hic kayitli degil) bulunursa, hipotez fazina geri donup soruyu revize etmeyi ACIKCA oner — bu ileri geri gidis normaldir ve erken yakalanmasi degerlidir.

## Cikti

`research/<slug>/02_design_feasibility.md`:
- Secilen tasarim + gerekce
- Degisken listesi (outcome/exposure/confounder, her biri icin veri kaynagi ve yapilandirilmis/serbest-metin durumu)
- Fizibilite denetim sonuclari (yukaridaki sorularin cevaplari)
- Tespit edilen riskler/acikla ve onerilen hafifletmeler
- Pilot chart review onerisi (eger belirsizlik yuksekse, kac dosyalik bir on-tarama onerilir)

## Kalite kontrolu

- "Bu veri muhtemelen vardir" gibi varsayimlara dayanma — kullaniciya acikca sor, bilmiyorsa bunu bir "bilinmiyor, pilot tarama gerekir" olarak isaretle.
- Tasarim secimini mutlaka hipotezdeki outcome/zaman penceresiyle tutarli kil.
