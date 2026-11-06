---
name: hypothesis-formulation
description: Literatur bosluk taramasindan cikan aday konuyu, test edilebilir bir arastirma sorusuna (PICO/PICOT formati) ve acik H0/H1 hipotezlerine donusturur. Kullanici "hipotez olustur", "arastirma sorusunu netlestir", "PICO" dedi mi ya da gap-scan tamamlandiktan sonra dogal bir sonraki adim oldugunda kullan.
---

# Hipotez ve Arastirma Sorusu Formulasyonu

## Amac

Genis/bulanik bir konu adayini, tasarimi ve analizi belirleyecek kadar KESKIN bir soruya indirmek.

## Girdi

`research/<slug>/00_gap_analysis.md` (varsa) ve kullanicinin secimi/onceligi.

## Adimlar

1. Secilen aday(lar)i PICO(T) formatina don:
   - **P (Population)**: tam olarak kim? (yas araligi, tani kriteri, ED'ye basvuru yolu, haric tutulanlar)
   - **I/E (Intervention/Exposure)**: ne olculuyor/uygulaniyor? (orn. bir ML modeli, bir gecikme suresi, bir klinik ozellik)
   - **C (Comparison)**: neye kiyasla? (klasik skala, baska model, baska grup — "karsilastirmasiz" bir prediction model calismasi da gecerlidir ama bunu acikca belirt)
   - **O (Outcome)**: tam olarak ne, hangi zaman penceresinde olculecek? (ornegin "taburculuk mRS", "hastane-ici mortalite", "72 saatlik revizit")
   - **T (Time, varsa)**: takip suresi
2. Birincil arastirma sorusunu TEK cumleyle yaz. Ikincil sorular varsa ayrica listele ama birinciyi net tut.
3. Test edilebilir hipotezleri yaz: H0 (fark/iliski yok) ve H1 (beklenen yon, varsa). ML prediction model calismalarinda klasik H0/H1 yerine "birincil performans hedefi" (orn. "AUC >= 0.75" ya da "model X, klasik skala Y'den anlamli derecede daha iyi ayirt eder") tanimlanabilir — hangisinin uygun oldugunu calisma tipine gore sec ve nedenini belirt.
4. Soruyu gap-analysis'teki bosluga ACIKCA baglayan 2-3 cumlelik bir gerekce yaz ("bu soru onemli cunku X calismasi Y'yi gostermis ama Z populasyonunda/aciyla hic bakilmamis").
5. Olculebilirlik kontrolu: her terimin (outcome, exposure) somut, HBYS'den/kayitlardan cikarilabilir bir karsiligi var mi? Yoksa sorunu yeniden ifade et veya kullaniciyi uyar.

## Cikti

`research/<slug>/01_hypothesis.md`:
- PICO(T) tablosu
- Birincil arastirma sorusu (tek cumle)
- Ikincil sorular (varsa)
- H0/H1 veya performans hedefi
- Gap-analysis baglantisi/gerekcesi
- Olculebilirlik notlari (hangi degiskenin nereden gelecegi hakkinda ilk izlenim — detayli fizibilite bir sonraki fazda)

## Kalite kontrolu

- Soru tek bir birincil outcome'a indirgenmis mi (birden fazla birincil outcome, analiz planini ve orneklem hesabini karmasiklastirir)?
- Zaman penceresi acik mi (orn. "mortalite" tek basina yetersiz, "hastane-ici mortalite" veya "30 gunluk mortalite" gibi netlestir)?
- Kullanicinin daha once belirttigi kisitlar (orn. "90 gun takip imkansiz") hipotezle celisiyor mu — celisiyorsa simdi yakala, sonraki fazda degil.
