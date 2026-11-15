# SPDX-License-Identifier: MIT
"""Plot retained numerical outputs; run in a modern matplotlib environment."""
from pathlib import Path
import csv,json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parent;out=root/'public_outputs'
rows=list(csv.DictReader((out/'learning-curve.csv').open()))
fig,ax=plt.subplots(figsize=(7,4))
ax.plot([int(r['timesteps_total']) for r in rows],[float(r['episode_reward_mean']) for r in rows],color='#123B5D',linewidth=1.8)
ax.axhline(-.02,color='#A33D2B',linestyle='--',linewidth=1.2,label='Source stopping criterion')
ax.set_xlabel('Environment steps');ax.set_ylabel('Mean episode reward');ax.legend(frameon=False);ax.grid(alpha=.15)
fig.tight_layout();fig.savefig(out/'training-curve.png',dpi=180);plt.close(fig)
s=json.loads((out/'summary.json').read_text());data=s['final_evaluations'];x=range(len(data));fig,ax=plt.subplots(figsize=(7,4))
ax.bar([i-.18 for i in x],[100*d['author_success_count']/d['count'] for d in data],width=.36,color='#123B5D',label='Author reward threshold')
ax.bar([i+.18 for i in x],[100*d['strict_success_count']/d['count'] for d in data],width=.36,color='#C47733',label='All constraints satisfied')
ax.axhline(96.3,color='#A33D2B',linestyle='--',linewidth=1.2,label='Paper Table II: 963/1000')
ax.set_xticks(list(x),[str(d['evaluation_seed']) for d in data]);ax.set_xlabel('Evaluation seed (20 targets each)');ax.set_ylabel('Targets reached (%)');ax.set_ylim(0,105);ax.legend(frameon=False,fontsize=8,loc='lower center',bbox_to_anchor=(.5,1.02));ax.grid(axis='y',alpha=.15)
fig.tight_layout();fig.savefig(out/'heldout-success.png',dpi=180);plt.close(fig)
