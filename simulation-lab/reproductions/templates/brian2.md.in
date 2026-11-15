# Brian 2: the paper's eye-movement model

Run the author model behind Figure 3 of [Stimberg, Brette and Goodman (2019)](https://doi.org/10.7554/eLife.47314), using the paper-version Brian 2.2.2.1 and Python 3.6. The [author repository](https://github.com/brian-team/brian2_paper_examples/tree/73045cd61322e923e96883dc97c0848154f79f8c) supplies the MIT/CC-BY licensed notebook. All eight model cells run unchanged; the final Plotly presentation cell is omitted and outputs are exported instead.

## Repeat the run

Use an isolated environment and a new output directory. `environment.yml` reconstructs the model stack; it omits the author's notebook/UI dependencies, and NumPy1.16.4 is an explicit reconstruction choice because the original environment did not pin NumPy. `environment-explicit.txt` records the exact tested Linux environment.

```sh
micromamba create -y -p ./env -f environment.yml
./env/bin/python fetch_sources.py
./env/bin/python run_brian_historical.py --output ./run
./env/bin/python compare_brian.py --run ./run --output ./comparison
```

The notebook uses seed79620,20 retinal neurons,2 motor neurons,a0.1ms timestep and10seconds. Both the article's Figure3c and author notebook use `tau_object=500*ms`. Retained full output includes100000 position samples and spike times/indices. The compact positions file retains every100th sample; comparison-points.csv contains the actual158 compared points.

## What matched

The historical model gave2406 retinal spikes and56/51 motor spikes. Repeated historical runs were array-identical. Compared with the previous modern Brian2.9.0 run, eye positions were identical and maximum object-position difference was1.1e-15.

Exploratory digitization of the paper's Figure3b gave the following results in the author's position units:

| Trace | RMSE | Maximum absolute error |
| --- | ---: | ---: |
| Eye | 0.0342156 | 0.100732 |
| Object | 0.0195218 | 0.0527203 |

The exploratory bounds were RMSE<=0.08 and maximum<=0.15, allowing for line thickness, JPEG pixels, time calibration and manual extraction. Figure labels left/right correspond to-1/+1 in the author's plotting code. The comparison is at raster resolution; it does not compare every spike or the entire article.

These bounds and the image region were chosen/refined after prior modern output and a first historical run existed. The first extraction accidentally included legend text and failed; its data and comparison are retained. Revision2 excludes that legend region without changing the model or bounds. A later deterministic rerun does not make this a prospective analysis. An initial manual50ms reading was also corrected by direct figure inspection to500ms; see source-reading-correction.json. The downloadable source figure is an open-access reference under the article's Creative Commons attribution terms.

**Status:** Author code executed, with an exploratory paper-figure comparison. Human scientific review of the pixel calibration and interpretation is pending. See comparison.json, the source manifest, original notebook/model-cell hashes and run record.
