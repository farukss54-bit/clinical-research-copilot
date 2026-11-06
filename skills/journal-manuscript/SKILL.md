---
name: journal-manuscript
description: Calismanin kapsamina, bulgularina ve kullanicinin hedeflerine (deneyim kazanma vs yuksek etki faktoru vs doçentlik puani) gore hedef dergi/kongre onerir ve IMRAD formatinda bir makale/sunum iskeleti olusturur. Kullanici "nereye gonderelim", "dergi secimi", "makale taslagi", "abstract yazalim" dedi mi kullan.
---

# Dergi/Kongre Secimi ve Makale Iskeleti

## Amac

Tamamlanan (veya tamamlanmaya yakin) bir calismayi, uygun bir hedefe (dergi/kongre) ve o hedefin beklentilerine uygun bir taslaga baglamak.

## Girdi

Mumkun oldugunca tum `research/<slug>/*.md` dosyalari (en azindan hipotez, tasarim, SAP; sonuclar varsa onlar da).

## Adimlar

1. **Hedef profili belirle**: kullanicinin onceligi ne (ilk deneyim/yayin sayisi mi, yuksek etki faktoru mu, belirli bir doçentlik kriteri mi)? Bu, agresif/iddiali bir dergi hedefi mi, yoksa daha erisilebilir bir dergi mi secilecegini belirler.
2. **Dergi/kongre adaylari oner**: calismanin konusuna (acil tip, norolojide/stroke, tibbi informatik/AI) ve kapsamina (orijinal arastirma / proof-of-concept / kisa rapor) uygun 3-5 aday oner; her biri icin kapsam uyumu, tahmini kabul zorlugu, ve biliniyorsa yayin ucreti (APC) / acik erisim politikasi notu ekle. Kesin/guncel etki faktoru sayilarini iddia etmeden once WebSearch ile dogrula, eski/hatali rakam verme.
3. **Raporlama standardina uy**: SAP'ta secilen checklist'e (STROBE/TRIPOD/TRIPOD-AI/STARD) gore makale iskeletini olustur; bu checklist dergi basvurusunda genelde zorunlu ekstra belge olarak istenir.
4. **IMRAD iskeleti** olustur (Introduction - Methods - Results - Discussion), her bolum icin:
   - Introduction: gap-analysis'teki bosluk + arastirma sorusu
   - Methods: tasarim + degiskenler + SAP ozeti (raporlama standardinin gerektirdigi detay seviyesinde)
   - Results: (bulgular hazirsa) tablolar/sekiller icin bir iskelet, hazır degilse placeholder ve hangi tablo/sekillerin gerekecegi listesi (orn. Tablo 1: hasta ozellikleri, Tablo 2: model performansi, Sekil 1: ROC egrisi)
   - Discussion: bulgunun literaturdeki yerini (gap-analysis'e geri referansla), sinirliliklar (methodology-critic bulgulari varsa buraya tasi), klinik anlam
5. Abstract/kongre sunumu isteniyorsa, dergi makalesinden once kisa bir abstract/poster iskeleti de olustur — bu genelde daha hizli bir ilk akademik kazanim saglar (kullanicinin "deneyim kazanma" hedefine uygun).

## Cikti

`research/<slug>/07_manuscript_plan.md`:
- Hedef profili ve secilen dergi/kongre adaylari (gerekceli)
- Uygulanacak raporlama standardi
- IMRAD iskeleti (bolum bolum, hazır olan/olmayan icerik acikca ayrilmis)
- Gerekli tablo/sekil listesi
- (istenirse) kisa abstract/poster iskeleti

## Kalite kontrolu

- Dergi onerirken guncel olmayan/iddiali etki faktoru rakamlari verme; dogrulanamiyorsa "guncel rakami kontrol etmen gerekir" de.
- Sonuclar henuz yoksa Results/Discussion'i hayali veriyle doldurma; sadece iskelet ve ne turde tablo/sekil gerekecegini goster.
