---
name: literature-gap-scan
description: Bir klinik arastirma konusu/alani icin literatur taramasi yaparak doldurulmus vs bos (gap) alanlari tespit eder ve adaylarini siralar. Kullanici "arastirma konusu/sorusu bulmak", "literatur bosluk taramasi", "bu konu calisilmis mi", "ozgunluk kontrolu" istediginde kullan. Klinik tip x AI/ML kesisiminde konu bulma icin ozellikle uygundur ama genel klinik arastirma konulariyla da calisir.
---

# Literatur Bosluk Taramasi

## Amac

Kullanicinin ilgilendigi klinik alan(lar)da ne kadar calisilmis oldugunu gostermek, hangi acilarin doymus/tekrarlanan sonuclar uretmis oldugunu, hangi acilarin az calisilmis oldugunu bulmak ve bunlardan somut, savunulabilir arastirma sorusu adaylari cikarmak.

## Girdi (kullanicidan/baglamdan topla)

- Ilgi alani/alanlari (genis olabilir, "takintim yok" da olabilir — bu durumda kullanicinin guclu yanlarindan/avantajlarindan (ozel hasta populasyonu, veri erisimi, klinik deneyim) yola cik)
- Kullanicinin kurumu/populasyonu hakkinda bilgi (hangi hasta gruplari one cikiyor, bu BM ozgunluk kaynagi olabilir)
- Varsa hedef dergi/kongre (yoksa onemli degil, genis dusun)

## Adimlar

1. **Arama araclarini kontrol et**: Su an baglı olan MCP connector'larini kontrola (PubMed, Consensus, Elicit, ClinicalTrials.gov, bioRxiv gibi). Hicbiri baglı degilse kullaniciya "bu arama araclarindan birini baglamak ister misin" diye sor; o da istemezse WebSearch ile ilerle — ama arama yapmadan asla "literatur boyle diyor" gibi bir iddiada bulunma.
2. **Genis tara**: Ilgi alanindaki ana kavramlari (hastalik/durum x yontem/teknoloji) birden fazla kombinasyonla ara. Tek bir dar sorguya guvenme; once genis, sonra daraltilmis sorgular dene (cok kisitlayici AND zincirleri 0 sonuc donebilir, sadelestir).
3. **Doygunluk/bosluk haritasi cikar**: Bulunan calismalari su eksenlerde siniflandir:
   - Populasyon/cografya (hangi ulkeler/saglik sistemleri temsil ediliyor, kullanicinin kendi populasyonu temsil ediliyor mu)
   - Yontem (klasik istatistik mi, hangi ML algoritmalari, dis validasyon var mi)
   - Sonuc tutarliligi (bulgular tekrar tekrar ayni mi cikiyor - orn. "ML, LR'den ustun degil" gibi doymus bir sonuc mu)
   - Outcome/zaman penceresi (kisa donem mi uzun donem mi, hangi outcome'lar hic calisilmamis)
4. **Adaylari uret**: En az 2-3 somut arastirma sorusu adayi cikar, her biri icin: (a) neden bosluk oldugu (hangi eksen bos), (b) kullanicinin mevcut avantajlariyla (veri/populasyon/zaman) ne kadar uyumlu oldugu, (c) tahmini ozgunluk/yayinlanabilirlik riski.
5. Kullaniciya hangi adayin ilgisini cektigini sor; birden fazlasi secilirse sentezleme imkanini da degerlendir.

## Cikti

`research/<slug>/00_gap_analysis.md` dosyasina yaz (slug yoksa kullanicidan iste veya konudan uret). Icerik:
- Taranan sorgular ve kullanilan kaynaklar (seffaflik icin)
- Bulunan ana calismalarin kisa ozeti (baslik, yil, populasyon, yontem, sonuc) hiperlinklerle
- Bosluk haritasi (yukaridaki eksenler)
- Siralanmis arastirma sorusu adaylari + gerekceleri

## Kalite kontrolu

- Her iddia bir kaynaga baglanmali; kaynaksiz "literaturde boyle" ifadesi kullanma.
- Tek bir arama motoruna guvenme; en az iki farkli kaynaktan (orn. PubMed + Consensus) capraz kontrol yap, sonuclar celisirse bunu belirt.
- "Hic calisilmamis" demek riskli bir iddiadir — bunun yerine "bulabildigim taramada X bulunamadi, ama terminoloji farkli indexlenmis olabilir" gibi temkinli ifade kullan.
