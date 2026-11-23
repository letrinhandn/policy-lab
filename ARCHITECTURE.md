# Architecture

```
Makefile + el CLI + Quarto
        |
   filesystem plugins          packages
   posts notebooks papers      el-core
   models data datasets        el-lab
        |
   _site/ (Quarto build)     artifacts/ (gitignored)
```

Publishing: `_quarto.yml` website listing `posts/*/index.qmd`.
