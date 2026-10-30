"""Coverage metadata must preserve the distinction between review and verification."""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import maf_knowledge as knowledge

class CoverageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'evidence.md').write_text('evidence')
        self.full = {'release':'dotnet-1.24.0','date':'2026-10-12','evidence':'evidence.md'}
        self.data = {'schema_version':1,'full_verification':self.full.copy(),
          'last_assessed_release':{'release':'dotnet-1.26.0','date':'2026-10-24','evidence':'evidence.md'},
          'areas':[{'id':'sessions','full_verification':self.full.copy(),'delta_reviews':[
            {'from_release':'dotnet-1.24.0','to_release':'dotnet-1.26.0','date':'2026-10-24','evidence':'evidence.md','scope':'Deletion and Cosmos migration only'}]}]}
    def test_scoped_review_does_not_promote_full_verification(self):
        self.assertEqual(knowledge.coverage_errors(self.data,self.root),[])
        self.assertEqual(self.data['areas'][0]['full_verification']['release'],'dotnet-1.24.0')
    def test_future_calendar_year_is_accepted(self):
        self.data['last_assessed_release']['date']='2027-01-15'
        self.assertEqual(knowledge.coverage_errors(self.data,self.root),[])
    def test_invalid_records_are_errors_not_crashes(self):
        bads=[None,[],True,{'schema_version':True},self.data|{'areas':True}]
        for data in bads:
            with self.subTest(data=data): self.assertTrue(knowledge.coverage_errors(data,self.root))
    def test_invalid_date_tag_and_evidence_are_rejected(self):
        for key,value in [('date','2026-02-30'),('date','2026-1-1'),('release','1.26'),('evidence','../escape.md'),('evidence','missing.md')]:
            with self.subTest(key=key,value=value):
                data=copy.deepcopy(self.data); data['last_assessed_release'][key]=value
                self.assertTrue(knowledge.coverage_errors(data,self.root))
    def test_reversed_or_inflated_coverage_is_rejected(self):
        for mutate in [lambda d:d['last_assessed_release'].update(release='dotnet-1.23.0'),lambda d:d['areas'][0]['delta_reviews'][0].update(to_release='dotnet-1.23.0'),lambda d:d['areas'][0]['delta_reviews'][0].update(to_release='dotnet-1.27.0'),lambda d:d['areas'][0].update(delta_reviews='bad')]:
            data=copy.deepcopy(self.data); mutate(data)
            self.assertTrue(knowledge.coverage_errors(data,self.root))
    def test_load_reports_malformed_json_with_context(self):
        p=self.root/'coverage.json'; p.write_text('[]')
        with self.assertRaisesRegex(ValueError,'coverage'): knowledge.load_coverage(p)
    def test_release_comparison_is_numeric(self):
        self.assertGreater(knowledge.release_key('dotnet-1.10.0'),knowledge.release_key('dotnet-1.9.0'))
        with self.assertRaises(ValueError): knowledge.release_key('dotnet-1.2.0-preview')
    def test_delta_dates_must_fit_the_assessed_window(self):
        for value in ['2026-01-01','2027-01-01']:
            data=copy.deepcopy(self.data);data['areas'][0]['delta_reviews'][0]['date']=value
            self.assertTrue(knowledge.coverage_errors(data,self.root))
    def test_global_full_release_cannot_outrun_constituent_areas(self):
        data=copy.deepcopy(self.data)
        data['full_verification'].update(release='dotnet-1.26.0',date='2026-10-24')
        self.assertTrue(knowledge.coverage_errors(data,self.root))
    def test_individual_full_area_review_can_exceed_global_baseline(self):
        data=copy.deepcopy(self.data)
        data['areas'][0]['full_verification'].update(release='dotnet-1.26.0',date='2026-10-24')
        data['areas'][0]['delta_reviews']=[]
        self.assertEqual(knowledge.coverage_errors(data,self.root),[])
