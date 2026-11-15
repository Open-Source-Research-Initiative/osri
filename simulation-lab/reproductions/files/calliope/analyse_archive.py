#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Compare archived Table1 metrics. No model optimization occurs here."""
from pathlib import Path
import argparse,csv,io,json,zipfile,hashlib,collections
p=argparse.ArgumentParser();p.add_argument('--archive',type=Path);p.add_argument('--output',type=Path,default=Path('analysis-output'));a=p.parse_args()
if a.archive:
 with zipfile.ZipFile(a.archive)as z:data=z.read('slack-10/data/paper_metrics.csv')
else:data=Path(__file__).with_name('paper_metrics.csv').read_bytes()
expected_sha='2e01de18469c7b89fd6620d0e6423ca9fce29a99a37a8b48b0bf02ac962f1467'
assert hashlib.sha256(data).hexdigest()==expected_sha,'CSV differs from verified author archive'
limits={'storage_discharge_capacity':([0.03,11],[.005,.5]),'curtailment':([0,6],[.5,.5]),'biofuel_utilisation':([0,100],[.5,.5]),'average_national_import':([4,69],[.5,.5]),'electricity_production_gini':([.54,.74],[.005,.005]),'fuel_autarky_gini':([.64,.99],[.005,.005]),'ev_flexibility':([.52,.92],[.005,.005]),'heat_electrification':([4,100],[.5,.5]),'transport_electrification':([53,100],[.5,.5])}
rows=list(csv.DictReader(io.StringIO(data.decode())));group=collections.defaultdict(list)
for r in rows:group[r['metric']].append(float(r['paper_metrics']))
measurements={}
for k,(ref,tol)in limits.items():
 observed=[min(group[k]),max(group[k])];measurements[k]={'observed_range':observed,'published_rounded_range':ref,'rounding_tolerance':tol,'passed':all(abs(x-y)<=t for x,y,t in zip(observed,ref,tol))}
configs={r['spore']for r in rows}
report={'status':'analysed_saved_output','new_optimization':False,'source_doi':'10.5281/zenodo.6546817','paper_doi':'10.1016/j.joule.2022.05.009','rows':len(rows),'configurations':len(configs),'matches_published_441_configurations':len(configs)==441,'csv_sha256':expected_sha,'measurements':measurements,'all_ranges_match_rounding':all(x['passed']for x in measurements.values())}
a.output.mkdir(parents=True,exist_ok=True);(a.output/'comparison.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));assert report['matches_published_441_configurations']and report['all_ranges_match_rounding']
