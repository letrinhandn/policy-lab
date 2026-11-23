# AGENTS.md — Economic Lab

Read this first. This repo is a knowledge vault for economic theory, published via Quarto.

## Mental model

```
POSTS (Quarto)                 BUNDLES                 NOTEBOOKS / PAPERS / MODELS
posts/<slug>/                  bundles/<slug>.zip
  index.qmd                      (qmd + figures + scripts + config)
  figures/
  scripts/
  config.yaml
```

One CLI: `python -m el_lab.cli` (alias `el` after `uv sync`)

## Commands

```bash
make setup
make doctor
make list
make new-post NAME=harrod-domar DOMAIN=growth
make preview
make render
make zip NAME=<slug>
make zip-all
make publish
```

## Directory contract

| Path | Purpose | Required |
|------|---------|----------|
| `posts/<slug>/` | Quarto essay | `config.yaml`, `index.qmd` |
| `posts/<slug>/figures/` | Essay figures | optional |
| `posts/<slug>/scripts/` | Regen / helper code | optional |
| `bundles/<slug>.zip` | Complete downloadable pack | regenerate via `make zip` |
| `notebooks/<slug>/` | Theory notebooks | `config.yaml` |
| `papers/<slug>/` | Academic paper | `config.yaml` |
| `models/<slug>/` | Model card | `config.yaml` |

Slug rules: kebab-case, lowercase, no leading `_`.

## Publishing

- Essays use Quarto (`index.qmd`), not Substack.
- Insert figures with `![caption](figures/...){#fig-x-y width="100%"}` next to the italic *Hình …* line.
- Keep placeholders `> *[Thiếu ảnh…]*` until the screenshot is ready.

## Anti-patterns

- Hardcode `artifacts/` paths
- Commit `.env` or large raw data dumps
- Mix live trading systems into this theory vault
