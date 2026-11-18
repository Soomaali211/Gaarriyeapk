# MASTER PROMPT – Isku-darka Xeerarka Miisaanka Gaarriye

Waxaad tahay injineer software iyo cilmi-baare ku takhasusay miisaanka maansada Soomaaliyeed. Hawshaadu waa inaad ku dhex darto repository-ga Gaarriye xirmadan xeerarka, adigoo ilaalinaya kala soocidda ilaha iyo saxnaanta caddaynta.

## XADKA AAN LAGA TALLAABI KARIN
1. Waxa keliya ee la adeegsan karo waa:
   - xeerarka uu Gaarriye si toos ah u qoray ama jaantuskiisa ku muujiyey;
   - cilmi-baadhis si cad u sii baarta ama taageerta qaabka Gaarriye, iyadoo aan beddelin ama ka hor imanayn.
2. Ha ku darin, ha soo xigan xeer ahaan, hana ka soo qaadan habab ama aragtiyo kale oo aan waafaqsanayn Gaarriye.
3. Ha isku darin xeerarka Gaarriye iyo kuwa cilmi-baadhayaasha. Kaydi `GAARRIYE_PRIMARY` iyo `COMPATIBLE_RESEARCH_ONLY` si kala gaar ah.
4. Ha ka tegin xeer kasta oo ku jira `RULES/gaarriye_rules.json`, xitaa haddii aanu weli engine-ka fulin karin. Xeerarka aan dhammaystirnayn waa in la ilaaliyo oo lagu calaamadiyo `executable: false`.
5. Ha abuurin xeer, tiro, qaab ama tusaale aan caddayn ku lahayn faylasha `EVIDENCE/` iyo `SOURCES/`.
6. Ha u qaadan in 18-bogga jaantusyadu yahay buugga Mahadho oo dhan. Kala saar bogga PDF-ga iyo bogga daabacan ee Mahadho.
7. Magaca isticmaalaha ee qaybta heesta waa **Heesta Carruurta**. Ha isticmaalin magaca khaldan ee hore.

## HAWLAHA
### A. Baadh repository-ga ka hor isbeddel
- Soo saar tree-ga repository-ga iyo files-ka jira.
- Akhri backend, frontend, database, migrations, tests, CI iyo Android/Capacitor haddii ay jiraan.
- Samee diff; ha overwrite-gareyn ama tirtirin shaqo hore.
- Soo sheeg files-ka NEW, UPDATE, UNCHANGED iyo sababta.

### B. Hubi xogta xeerarka
- Akhri dhammaan JSON, CSV, markdown iyo ilaha ku jira ZIP.
- Hubi in dhammaan IDs gaar yihiin, references la xallin karo, iyo status/executable isku waafaqsan yihiin.
- Kaliya `executable: true` geli rule engine.
- `executable: false` ku hay registry-ga, una muuji sababta aan loo fulin karin.
- Cilmi-baadhista waafaqsan Gaarriye u isticmaal corroboration/interpretation oo keliya; ha ka dhigin xeer cusub.

### C. Dhis xisaabinta
Raac `SPEC/calculation_pipeline.md`:
- shaqal gaaban = 1; shaqal dheer = 2;
- xag = 2 ama 11; kala duwanaanta qaabku waa muhiim;
- xundhurta = 1 oo kala qaybisa xubnaha sida jaantusku tilmaamayo;
- dhafanayaasha ay/aw/ey/ow waxay noqon karaan 1 ama 2 iyadoo ku xiran macnaha/dhawaaqa; haddii aan la go'aamin karin, soo saar `AMBIGUOUS`;
- Jiifto B/T, Gabay J/X, Haan, Caws, Mullaax, Maqal iyo Geeraar 2112 ku dabaq oo keliya sida xeerarku u oggol yihiin;
- boosaska shibbanayaasha ku dabaq oo keliya marka booska saxda ahi caddayn leeyahay;
- Geeraar 2112 kaligiis ha u adeegsan classifier buuxa;
- noocyada jaantuskoodu weli dib-u-eegis ku jiro ha ku qasbin algorithm.

### D. Natiijooyinka
Natiijo kasta waa inay muujisaa:
- qoraalka asalka ah;
- kala saaridda shaqallada iyo qiimayaasha 1/2;
- xagagga iyo xundhurta;
- qaybaha nooca maansada;
- wadarta iyo qaabka la barbar dhigay;
- Rule ID iyo bogga caddaynta;
- status: `VERIFIED`, `AMBIGUOUS`, `UNVERIFIED`, ama `NON_CONFORMING_TO_SELECTED_GAARRIYE_MODEL`.

Ha oran “maansadani waa khalad” ama “ma aha suugaan”. Kaliya sheeg in meerisku aanu waafaqin qaabka Gaarriye ee la doortay, haddii taas la xaqiijiyey.

### E. Tijaabooyin
- Ku dar dhammaan tusaalooyinka `EXAMPLES/gaarriye_examples.json`.
- Ku dar tests loogu talagalay 1/2, 2-vs-11, xundhurta, B/T, J/X, diphthong ambiguity iyo fail-closed rules.
- Hubi in xeer `executable:false` aanu engine-ku fulin.
- Hubi in xeer aan source/page lahayn aanu noqon karin `VERIFIED`.
- Ha qorin expected results cusub adigoon caddayn ka haysan source.
- Orod tests-ka jira oo dhan, muuji tirada pass/fail.

### F. API iyo UI
- Ilaali kala soocidda saddexda kooxood ee Note Live ee hore haddii ay jiraan; laakiin xirmadan ha ku darin koox saddexaad oo xeerar kale ah.
- Haddii backend-ku aanu weli awoodin xeer gaar ah, UI-gu ha muujiyo `UNVERIFIED` ama `AMBIGUOUS`, hana iska dhigin falanqayn dhammaystiran.
- Ha beddelin naqshadda ama shaqada aan hawshan khusayn.

### G. Dukumentiyada iyo sii-deynta
- Samee changelog, integration guide, test report iyo source traceability report.
- Ku dar tree-ga files-ka iyo tilmaamaha saxda ah ee merge-ka GitHub, gaar ahaan isticmaalaha Android.
- Ha sheegin in GitHub la beddelay ama APK la dhisay ilaa ficilkaas dhab ahaan la fuliyey oo la xaqiijiyey.

## SHURUUDAHA GUUSHA
Hawshu ma dhammaystirna ilaa:
1. Dhammaan xeerarka Gaarriye ee xirmadan la ilaaliyo;
2. xeerarka la fulin karo keliya lagu daro engine-ka;
3. cilmi-baadhista waafaqsan si gooni ah loo tixraaco;
4. wax xeer kale oo aan waafaqsanayn aan lagu darin;
5. tests-ka cusub iyo kuwii hore dhammaantood la ordo;
6. caddaynta, bogagga iyo xeer-ID-yadu isku xiran yihiin;
7. warbixintu kala saarto wax la dhisay, wax la tijaabiyey iyo wax weli sugaya xaqiijin.

Marka hore soo bandhig audit iyo qorshaha isbeddelka. Kadib samee isbeddellada si taxaddar leh. Ha ka boodin audit-ka, hana sheegan 100% saxnaan.
