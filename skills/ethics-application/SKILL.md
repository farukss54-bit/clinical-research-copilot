---
name: ethics-application
description: Tasarim, orneklem ve veri sozlugu dosyalarina dayanarak etik kurul basvuru metni tasligi hazirlar (girisimsel olmayan klinik arastirmalar etik kurulu / IRB formatinda), KVKK uyum notlariyla birlikte. Kullanici "etik kurul basvurusu", "IRB", "KVKK", "onam gerekiyor mu" dedi mi kullan. Agir/detayli taslaklar icin ethics-drafter alt-agent'ini cagirabilir.
---

# Etik Kurul Basvurusu

## Amac

Calismanin tasarim/veri belgelerini, kuruma sunulabilir bir etik kurul basvuru taslagina donusturmek.

## Girdi

`research/<slug>/02_design_feasibility.md`, `03_sample_size.md`, `04_data_dictionary.md`, (varsa) `01_hypothesis.md`, `00_gap_analysis.md`.

## Adimlar

1. Yukaridaki dosyalarin hepsinin mevcut olup olmadigini kontrol et; eksikse kullaniciya bildir (yumusak hatirlatma — tamamlanmamis bir tasarimla da taslak uretebilirsin ama bunu acikca "eksik/taslak" olarak isaretle).
2. Agir/tam kapsamli bir taslak icin (ozellikle KVKK/hukuki detaylar) `ethics-drafter` alt-agent'ini `research-advisor` araciligiyla cagirmayi oner; bu skill dogrudan da temel bir taslak uretebilir.
3. Taslakta su basliklari bulundur: amac/arka plan, arastirma sorusu/hipotez, tasarim, dahil/haric kriterleri, veri kaynaklari ve degiskenler, orneklem buyuklugu+gerekce, veri toplama/saklama/kimliksizlestirme plani, KVKK uyum notu (hukuki sebep, ozel nitelikli veri durumu, onam gerekliligi), riskler ve onlemler, beklenen fayda.
4. Taslagin basina "bu bir taslaktir, kurumsal formata ve mevzuata gore gozden gecirilmelidir" notunu ekle.
5. Serbest metinden AI-destekli veri cikarimi planlaniyorsa (data-dictionary'den), bunun etik kurula nasil aciklanacagini (yontem + dogrulama orani) ayri bir paragrafta belirt — bu seffaflik, degerlendirmeyi kolaylastirir.

## Cikti

`research/<slug>/06_ethics_application.md` (yukaridaki basliklarla).

## Kalite kontrolu

- Belgede olmayan veriyi/sayiyi icat etme; eksikse "belirtilmedi" yaz.
- Hukuki kesinlik iddia etme ("KVKK'ya tam uyumludur" gibi) — "genelde", "kurumunuzun degerlendirmesine bagli" gibi temkinli dil kullan.
