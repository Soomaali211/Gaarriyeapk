import json, csv, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class PackageTests(unittest.TestCase):
    def test_rule_ids_unique(self):
        data=json.loads((ROOT/'RULES/gaarriye_rules.json').read_text(encoding='utf-8'))
        ids=[r['id'] for r in data['rules']]
        self.assertEqual(len(ids),len(set(ids)))
    def test_all_rules_are_gaarriye_primary(self):
        data=json.loads((ROOT/'RULES/gaarriye_rules.json').read_text(encoding='utf-8'))
        self.assertTrue(all(r['class']=='GAARRIYE_PRIMARY' for r in data['rules']))
    def test_non_executable_rules_not_promoted(self):
        data=json.loads((ROOT/'RULES/gaarriye_rules.json').read_text(encoding='utf-8'))
        for r in data['rules']:
            if r['status'].endswith('REVIEW') or 'REVIEW' in r['status']:
                self.assertFalse(r['executable'],r['id'])
    def test_examples_have_sources(self):
        data=json.loads((ROOT/'EXAMPLES/gaarriye_examples.json').read_text(encoding='utf-8'))
        self.assertTrue(all(x.get('source')=='G-MAHADHO' and x.get('page') for x in data['examples']))
    def test_research_separate(self):
        data=json.loads((ROOT/'RULES/compatible_research.json').read_text(encoding='utf-8'))
        self.assertTrue(all(x['id'].startswith('R-') for x in data['sources']))
    def test_no_third_rule_class(self):
        data=json.loads((ROOT/'RULES/gaarriye_rules.json').read_text(encoding='utf-8'))
        self.assertEqual({r['class'] for r in data['rules']},{'GAARRIYE_PRIMARY'})
    def test_sources_registry(self):
        with (ROOT/'EVIDENCE/source_registry.csv').open(encoding='utf-8-sig') as f:
            rows=list(csv.DictReader(f))
        ids=[r['source_id'] for r in rows]
        self.assertEqual(len(ids),len(set(ids)))
    def test_verified_rules_have_evidence(self):
        data=json.loads((ROOT/'RULES/gaarriye_rules.json').read_text(encoding='utf-8'))
        for r in data['rules']:
            if r['status'].startswith('VERIFIED'):
                self.assertTrue(r.get('evidence'),r['id'])
if __name__=='__main__': unittest.main()
