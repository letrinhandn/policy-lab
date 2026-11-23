# Post bundles

Complete zip for each Quarto essay: `qmd` + figures + scripts + config.

```bash
make zip NAME=solow-swan-tang-truong   # one post
make zip-all                           # every posts/*/index.qmd
```

Output: `bundles/<slug>.zip`  
Inside the zip, files live under `<slug>/` (with `BUNDLE.txt` manifest).
