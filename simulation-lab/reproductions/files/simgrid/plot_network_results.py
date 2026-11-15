from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parent
j=json.loads((root/'ns3-output/comparison.json').read_text())
fig,axes=plt.subplots(1,3,figsize=(10,3.2),layout='constrained')
labels=['Default,2','Unison,2','Default,4','Unison,4']
for ax,metric,title,unit in zip(axes,['fct_ms','rtt_ms','throughput_mbps'],['Flow completion','Round trip','Flow throughput'],['ms','ms','Mbps']):
 rows=[r for r in j['table_comparison'] if r['metric']==metric]
 ax.plot(range(4),[r['reference'] for r in rows],'o',color='black',label='Paper Table2',markersize=7)
 ax.plot(range(4),[r['observed'] for r in rows],'+',color='#007a9f',label='Local author code',markersize=8,markeredgewidth=1.6)
 ax.set_xticks(range(4),labels,rotation=30,ha='right');ax.set_ylabel(unit);ax.set_title(title);ax.grid(axis='y',alpha=.2)
axes[-1].legend(fontsize=8)
for suffix in ['png','svg']:fig.savefig(root/('ns3-output/table2-comparison.'+suffix),dpi=180)
plt.close(fig)
j=json.loads((root/'simgrid-output/comparison.json').read_text());fig,axes=plt.subplots(1,2,figsize=(8.5,3.2),layout='constrained')
for version,color in [('3.10','#1f4568'),('3.36','#00867c')]:
 rows=[r for r in j['performance_summaries'] if r['version']==version];x=[r['tasks']/1000 for r in rows]
 for ax,key,scale,title,ylabel in [(axes[0],'elapsed',1,'Wall time','s'),(axes[1],'max_rss',1024,'Peak resident memory','MiB')]:
  unit='seconds' if key=='elapsed' else 'kib'
  mean=[r[key+'_mean_'+unit]/scale for r in rows];lo=[r[key+'_min_'+unit]/scale for r in rows];hi=[r[key+'_max_'+unit]/scale for r in rows]
  ax.errorbar(x,mean,yerr=[[a-b for a,b in zip(mean,lo)],[b-a for a,b in zip(mean,hi)]],fmt='o-',capsize=4,label='SimGrid '+version,color=color)
  ax.set_title(title);ax.set_xlabel('Workunits (thousands)');ax.set_ylabel(ylabel);ax.grid(alpha=.2)
axes[1].legend(fontsize=8)
for suffix in ['png','svg']:fig.savefig(root/('simgrid-output/figure13-endpoints.'+suffix),dpi=180)
print(matplotlib.__version__)
