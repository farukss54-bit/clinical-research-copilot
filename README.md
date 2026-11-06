# clinical-research-copilot

Klinik arastirma tasariminin **literatur boslugu taramasindan etik kurul basvurusu ve yayin/dergi secimine kadar** olan adimlarinda rehberlik eden bir Claude Code plugin'i. Ozellikle klinik tip ile AI/ML'in kesistigi calismalar icin optimize edilmistir, ama genel klinik arastirma tasarimi icin de kullanilabilir.

Konusma/arayuz dili **Turkce**; SAP ve makale taslagi gibi uluslararasi yayina yonelik akademik ciktilar **Ingilizce**, etik kurul basvurusu gibi yerel-kurumsal belgeler Turkce uretilir.

## Icerik

| Klasor | Icerik |
|---|---|
| `agents/` | `research-advisor` (ana koordinator) + `biostatistics-reviewer`, `ethics-drafter`, `methodology-critic` (alt-agent'lar) |
| `skills/` | 8 skill: `literature-gap-scan`, `hypothesis-formulation`, `study-design-feasibility`, `sample-size-power`, `data-dictionary-crf`, `sap-builder`, `ethics-application`, `journal-manuscript` |
| `hooks/` | Yumusak (engellemeyen) hatirlaticilar: proje durumu ozeti, bir sonraki adim onerisi, KVKK/hassas veri uyarisi |

## Proje yapisi (konvansiyon)

Her arastirma projesi, calistigin dizinde `research/<calisma-slug>/` altinda numarali fazlarla ilerler:

```
research/<calisma-slug>/
  00_gap_analysis.md
  01_hypothesis.md
  02_design_feasibility.md
  03_sample_size.md
  04_data_dictionary.md
  05_sap.md
  06_ethics_application.md
  07_manuscript_plan.md
```

Birden fazla calismayi paralel yurutebilirsin (her biri kendi `<calisma-slug>` klasorunde). `research-advisor` agent'i bu dosyalara bakarak hangi fazda oldugunu kendi anlar.

## Kurulum

**Yerel (kisisel) kullanim:**
```
/plugin install /path/to/clinical-research-copilot
```
(veya Claude Code'un guncel plugin kurulum komutuyla — surumler arasinda komut adi degisebilir, `/plugin` ile baslayan komutlari kontrol et.)

**Daha genis dagitim (GitHub uzerinden):**
1. Bu klasoru bir GitHub reposuna push et.
2. Baska bir kullanici: `/plugin marketplace add <github-url>` ile bu repoyu (kendi `.claude-plugin/marketplace.json` dosyasi sayesinde) bir marketplace olarak ekler.
3. Ardindan `/plugin install clinical-research-copilot` ile plugin'i kurar.

> Not: Plugin/marketplace dosya semasi Claude Code surumleriyle degisebilir. Kurulumda hata alirsan, kullandigin surumun guncel plugin dokumantasyonuna gore `plugin.json`/`marketplace.json` alanlarini dogrula.

## Literatur/veri araclari (connector) stratejisi

Skill'ler calisirken once su an baglı olan MCP connector'larini (PubMed, Consensus, Elicit, ClinicalTrials.gov, bioRxiv vb.) kullanmayi dener. Bu connector'lar hesabina ozgudur ve plugin icine gomulu degildir — baska bir kullanicida/makinede otomatik gelmez. Baglı degillerse skill'ler once bunu baglamani onerir, istemezsen web aramasina (WebSearch) duser. Yani plugin, connector'lar olmadan da calisir ama literatur taramasi daha sinirli olur.

## Hook davranisi

Tum hook'lar **yumusaktir**: hicbir islemi engellemez, sadece bilgilendirici mesaj yazdirir.

- `SessionStart`: `research/*/` projelerin varsa hangi fazda oldugunu ozetler.
- `PostToolUse` (Write/Edit): ilgili faz dosyasi yazildiginda bir sonraki adimi onerir; dosya adi hasta/saglik verisi izlenimi veriyorsa KVKK hatirlatmasi yapar.

Hook script'leri `python3` gerektirir (standart kutuphane disinda bagimlilik yoktur).

## Onemli sinirlamalar

- Bu plugin **hukuki veya istatistiksel danismanligin yerine gecmez**. Etik kurul/KVKK ciktilari her zaman "taslak" olarak isaretlenir ve kurumsal/hukuki teyit gerektirir; orneklem/SAP ciktilari bir biyoistatistikci tarafindan gozden gecirilmelidir (`biostatistics-reviewer` bunun otomatik bir yerine gecmesi degil, ilk-gecis bir kontroldur).
- Serbest metinden AI-destekli veri cikarimi onerilirse, mutlaka bir manuel dogrulama alt-ornegiyle birlikte kullanilmalidir.
- Plugin hic bir yere otomatik veri gondermez/yuklemez; sadece yerel markdown belgeleri uretir.
