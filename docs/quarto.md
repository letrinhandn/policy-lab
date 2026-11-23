# Quarto publishing

## Workflow

```bash
make new-post NAME=your-slug DOMAIN=growth
# write posts/<slug>/index.qmd
# put images in posts/<slug>/figures/
make preview
make render
make publish
```

## Figure pattern

```markdown
![Caption text](figures/hinh-2-1.png){#fig-2-1 width="100%"}

*Hình 2.1. Caption text*
```

Until a figure is ready, keep:

```markdown
> *[Thiếu ảnh minh họa Hình X.Y trong bản sao chép]*

*Hình X.Y. …*
```

## Install

Quarto CLI on `PATH`, or `~/.local/bin/quarto`.
