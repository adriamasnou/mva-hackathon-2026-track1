#!/usr/bin/env python3
"""Render completed source-label recovery results as a static research figure."""
import argparse
import json
import math
from pathlib import Path


def main():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.colors import LogNorm
    import numpy as np
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--hg002',type=Path,required=True)
    ap.add_argument('--hg001',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args()
    arms=['original','half_missing','swapped','none']
    labels=['Original HPO','Half retained','Swapped HPO','No HPO']
    genes=['MTOR','KCNJ2','CTCF','LZTR1','INTS11','BCKDHB','DOCK8','COG8','SLC35C1','PAX4','ZIC3','OFD1']
    datasets=[json.loads(p.read_text()) for p in (a.hg002,a.hg001)]
    values=[];texts=[]
    for data in datasets:
        lookup={(r['gene'],r['arm']):r for r in data['all_case_results']}
        if len(lookup)!=48:raise ValueError('Expected all twelve cases and four arms')
        matrix=np.full((12,4),np.nan);annotations=[]
        for y,g in enumerate(genes):
            row=[]
            for x,arm in enumerate(arms):
                r=lookup[g,arm]
                if r['status']=='scored':
                    lo,hi=r['rank_min'],r['rank_max']
                    if not (isinstance(lo,int) and isinstance(hi,int) and 0<lo<=hi):raise ValueError('Invalid rank interval')
                    matrix[y,x]=hi;row.append(str(lo) if lo==hi else f'{lo}–{hi}')
                else:row.append('not scored' if r['status']=='not_scored' else 'run failed')
            annotations.append(row)
        values.append(matrix);texts.append(annotations)
    finite=[float(x) for v in values for x in v.flat if np.isfinite(x)]
    maxrank=max(finite or [10])
    vmax=max(10,10**math.ceil(math.log10(maxrank)))
    cmap=plt.get_cmap('viridis_r').copy();cmap.set_bad('#eeeeee')
    plt.rcParams.update({'font.family':'sans-serif','font.size':10})
    fig,axes=plt.subplots(1,2,figsize=(12.4,8.9),sharey=True)
    fig.subplots_adjust(left=.13,right=.88,bottom=.30,top=.83,wspace=.12)
    for panel,(ax,matrix,title) in enumerate(zip(axes,values,['Public HG002 background','Public HG001 background'])):
        artist=ax.imshow(matrix,norm=LogNorm(vmin=1,vmax=vmax),cmap=cmap,aspect='auto')
        ax.set_xticks(range(4),labels,rotation=25,ha='right')
        ax.set_yticks(range(12),genes)
        ax.set_title(title,fontweight='bold',pad=12)
        ax.axhline(8.5,color='white',linewidth=3)
        ax.axhline(9.5,color='white',linewidth=3)
        for y in range(12):
            for x in range(4):
                value=matrix[y,x]
                color='white' if np.isfinite(value) and value>vmax**.55 else '#172e37'
                ax.text(x,y,texts[panel][y][x],ha='center',va='center',color=color,fontsize=9)
        ax.tick_params(length=0)
        for spine in ax.spines.values():spine.set_visible(False)
    cax=fig.add_axes([.905,.29,.018,.5])
    fig.colorbar(artist,cax=cax,label='Conservative source-gene rank (log scale)')
    fig.suptitle('Public multi-case evaluation: every source label and phenotype arm',x=.5,y=.97,fontsize=16,fontweight='bold')
    fig.text(.13,.89,'Semi-synthetic inputs • Exomiser 15.1.0 / data 2512 • ClinVar filter-bypass whitelist disabled',fontsize=10)
    fig.text(.13,.065,'Primary comparison: nine autosomal source-label cases, with source qualifications retained.\n'
             'PAX4: disputed causal truth. ZIC3/OFD1: limited technical cases without X background.\n'
             'Cells show exact-score rank intervals; color uses the worst tied rank. Gray retains missing/unscored outcomes.\n'
             'Two backgrounds are paired tests, not twice as many independent disease cases. No clinical accuracy claim.\n'
             'COG8/SLC35C1, No HPO: best-scoring mode uses only one of two source alleles in both backgrounds.',
             fontsize=9,linespacing=1.6)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(a.output,dpi=180,facecolor='white')
    print(a.output)


if __name__=='__main__':main()
