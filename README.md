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

**Yerel gelistirme / deneme (tek oturumluk):**
```
claude --plugin-dir /path/to/clinical-research-copilot
```

**Kalici kurulum (marketplace uzerinden):**
```
/plugin marketplace add /path/to/clinical-research-copilot      # veya GitHub: <kullanici>/<repo>
/plugin install clinical-research-copilot@clinical-research-copilot-marketplace
```

Kurulum sonrasi `claude plugin validate .` ile manifest dogrulanabilir.

**Koordinator agent'i ana agent olarak calistir:** alt-agent'lar baska alt-agent cagiramaz, bu yuzden
`research-advisor` hakem agent'larini (methodology-critic, biostatistics-reviewer, ethics-drafter) ancak ana
agent olarak calisirsa cagirabilir:
```
claude --agent clinical-research-copilot:research-advisor
```
Skill'ler (`/clinical-research-copilot:sample-size-power` vb.) ise normal oturumda dogrudan kullanilabilir.

## Literatur/veri araclari (connector) stratejisi

Skill'ler calisirken once su an baglı olan MCP connector'larini (PubMed, Consensus, Elicit, ClinicalTrials.gov, bioRxiv vb.) kullanmayi dener. Bu connector'lar hesabina ozgudur ve plugin icine gomulu degildir — baska bir kullanicida/makinede otomatik gelmez. Baglı degillerse skill'ler once bunu baglamani onerir, istemezsen web aramasina (WebSearch) duser. Yani plugin, connector'lar olmadan da calisir ama literatur taramasi daha sinirli olur.

## Hook davranisi

Tum hook'lar **yumusaktir**: hicbir islemi engellemez, sadece Claude'a bilgi ekler.

- `SessionStart`: `research/*/` projelerin varsa hangi fazda oldugunu ozetler.
- `PostToolUse` (Write/Edit): ilgili faz dosyasi yazildiginda bir sonraki adimi onerir; yol/dosya adi hasta verisi izlenimi veriyorsa (`hasta`, `patient`, `hbys`, `ehr`, `vaka`... + csv/xlsx/json vb.) KVKK hatirlatmasi ekler. Bu kontrol yalnizca Claude'un yazdigi dosyalara bakar; `Bash` ile uretilen veya zaten diskte duran veriyi yakalamaz.

Hook'lar `hooks/run.sh` uzerinden `python3`, `python` veya `py -3` yorumlayicilarindan calisan ilkini kullanir (Windows'ta `python3` genellikle Microsoft Store kisayoludur; bu yuzden her aday once denenir). Hicbiri yoksa hook sessizce atlanir. Windows'ta `sh` icin Git for Windows (Git Bash) gerekir. Standart kutuphane disinda bagimlilik yoktur.

## Onemli sinirlamalar

- Bu plugin **hukuki veya istatistiksel danismanligin yerine gecmez**. Etik kurul/KVKK ciktilari her zaman "taslak" olarak isaretlenir ve kurumsal/hukuki teyit gerektirir; orneklem/SAP ciktilari bir biyoistatistikci tarafindan gozden gecirilmelidir (`biostatistics-reviewer` bunun otomatik bir yerine gecmesi degil, ilk-gecis bir kontroldur).
- Serbest metinden AI-destekli veri cikarimi onerilirse, mutlaka bir manuel dogrulama alt-ornegiyle birlikte kullanilmalidir.
- Plugin kendisi herhangi bir yere veri yuklemez ve yalnizca yerel markdown belgeleri uretir. **Ancak** Claude'un okudugu her dosya ve yazdiginiz her istem modele (Anthropic API) gonderilir. Hasta duzeyi veriyi, kurumunuzun onayi ve kimliksizlestirme olmadan Claude'a okutmayin; bu plugin'in hook'lari bunu teknik olarak engellemez, yalnizca hatirlatir.
