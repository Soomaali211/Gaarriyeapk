# Xirmada Xeerarka Miisaanka – Gaarriye iyo Cilmi-baadhis waafaqsan

## Waxa xirmadani ka kooban tahay
Xirmadani waxay ka kooban tahay **xeerarka Gaarriye** iyo **tixraacyo cilmiyeed oo si cad u sii baaraya ama taageeraya qaabka Gaarriye oo keliya**. Kuma jiraan xeerar ka yimid habab kale oo aan la jaanqaadin.

## Faylasha
- `RULES/gaarriye_rules.json` – xeerarka Gaarriye iyo xaaladdooda.
- `RULES/compatible_research.json` – cilmi-baadhista waafaqsan Gaarriye; lama isku qasin xeerarkiisa.
- `EXAMPLES/gaarriye_examples.json` – tusaalooyinka Gaarriye ee leh bog tixraac.
- `SPEC/calculation_pipeline.md` – habka xisaabinta.
- `EVIDENCE/source_registry.csv` – diiwaanka ilaha.
- `EVIDENCE/diagram_inventory.md` – tusmada 18-ka jaantus.
- `SOURCES/PRIMARY/` – scans-kii Jannaayo ilaa Abriil 1976 ee la heli karay.
- `SOURCES/DIAGRAMS/` – 18-bogga jaantusyada Gaarriye.
- `PROMPT/MASTER_PROMPT.md` – amarka buuxa ee lagu dhexgelinayo repository-ga.
- `TESTS/` – tijaabooyinka hubinta xirmada.

## Xaaladda caddaynta
`VERIFIED` waxay ka dhigan tahay in qoraal/jaantus gaar ah la taageeray. Ma aha in dhammaan algorithm-ka noocaas la dhammeeyey. Xeer kasta wuxuu leeyahay `executable` boolean. Kaliya `executable: true` ayaa loo oggol yahay engine-ka; kuwa kale waa in loo soo bandhigaa xog/caddayn ama dib-u-eegis.

## Isku-darka GitHub
1. Soo dejiso ZIP-kan oo fur.
2. Ku dar faylasha repository-ga adigoo ilaalinaya folder names.
3. Haddii magac fayl isku mid ahi jiro, isbarbar dhig ka hor overwrite.
4. Ku dar `RULES/`, `EVIDENCE/`, `EXAMPLES/`, `SPEC/`, `SOURCES/` iyo `PROMPT/` sida folder cusub ama ku dar faylasha hoos yimaada folders jira.
5. Ha tirtirin ama beddelin xeerar hore ilaa la sameeyo diff iyo review.
6. Orod: `python -m pytest -q` gudaha `TESTS/` ama ku dar tests-ka repo-ga.
7. Ka hor engine integration, xaqiiji in backend-ku akhriyo `gaarriye_rules.json` oo uu kaliya fuliyo `executable: true`.

## Xaddidaad
Qaybo ka mid ah jaantusyada Baarcadda, Kabadaha, Xerta Herimaahee waxay u baahan yihiin transkribshan muuqaal oo dheeraad ah. Xeerarkaas lama qarin, laakiin si been ah looma saydhinayo inay diyaar u yihiin xisaabin otomaatig ah.
