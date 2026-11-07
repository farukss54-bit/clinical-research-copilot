# Turkey: ethics committee and KVKK reference

Use this file when the application is for a Turkish institution. It is orientation, **not legal advice**. **Nothing in this file was verified against current sources when it was written**, including the committee name, the law number and the Article 6 statement. Laws, regulations and committee formats change (provisions on special-category data and on cross-border transfer have been amended in recent years), so confirm everything with the institution's ethics committee secretariat and its data-protection contact before submitting. Items marked *(verify)* are the ones most likely to be out of date.

## Committee and forms

- Retrospective, observational, chart-review studies on humans typically go to the institution's **Non-Interventional Clinical Research Ethics Committee** (Turkish: *Girişimsel Olmayan Klinik Araştırmalar Etik Kurulu*). Training and research hospitals, university hospitals and some private hospitals have their own form and meeting calendar *(verify for your institution)*.
- Interventional drug/device studies follow different regulatory routes and are outside this skill.
- Many institutions also require administrative permission (for example from the hospital management) to access patient records for research *(verify)*.
- Forms are usually filled in **Turkish**. Write the application in Turkish if the institution requires it, and keep the clinical terms in their usual English/Latin form where physicians customarily do.

## Section headings (English → Turkish) for drafting

| English | Turkish |
|---|---|
| Purpose and background | Araştırmanın amacı ve gerekçesi |
| Research question / hypothesis | Araştırma sorusu / hipotez |
| Design | Araştırmanın türü ve tasarımı |
| Inclusion / exclusion criteria | Dahil edilme / dışlanma kriterleri |
| Data sources and variables | Veri kaynakları ve değişkenler |
| Sample size | Örneklem büyüklüğü |
| Data storage and de-identification / coding | Verilerin saklanması ve kodlanması (anonimleştirme yalnızca veri gerçekten anonimse) |
| Data protection | Kişisel verilerin korunması |
| Consent / waiver of consent | Aydınlatılmış onam / onam muafiyeti |
| Risks and mitigation | Riskler ve önlemler |
| Expected benefit | Beklenen fayda |

## Personal data law (KVKK, Law No. 6698)

- Health data is a **special category of personal data** (*özel nitelikli kişisel veri*) under Article 6, with stricter conditions for processing *(verify current text)*.
- Anonymized data is generally outside the scope of the law, and the law contains provisions for processing data for research and statistics once anonymized *(verify exact article and conditions with the data-protection contact)*. De-identified or pseudonymized data (a key still exists) is *not* the same as anonymized data.
- Consent: many retrospective, de-identified chart-review studies are handled with a waiver of consent, but the **committee and institutional policy decide**. Do not state that consent is "not needed"; write what the institution's decision process will be.
- Regulations specific to personal health data and to transfers abroad exist. Using cloud services or foreign-hosted LLM endpoints with patient-level data can raise cross-border transfer issues *(verify with the institution)*.

## Practical checklist

- Direct identifiers (name, national ID number, phone) are absent from the analysis dataset; a study-specific code is used and the linkage key is stored separately with restricted access.
- Free-text notes are never sent to external services unless the institution has approved it and the text is de-identified.
- The application states who has access, where data are stored, for how long, and how they are destroyed.
- If an LLM is used on notes, the application says where the model runs and what leaves the institution.
