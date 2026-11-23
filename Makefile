.PHONY: help setup sync doctor list \
        new-notebook new-paper new-post new-project new-data new-dataset new-model \
        preview render publish quarto-doctor \
        figures zip zip-all lint test

REPO := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
EL := cd $(REPO) && uv run --python 3.12 python -m el_lab.cli
QUARTO ?= $(shell command -v quarto 2>/dev/null || echo $(HOME)/.local/bin/quarto)

NAME ?=
DOMAIN ?= general

help:
	@echo "Economic Lab"
	@echo ""
	@echo "  make setup                 Install workspace"
	@echo "  make doctor                Health check"
	@echo "  make list                  List all plugins"
	@echo "  make new-post NAME=x       Quarto essay"
	@echo "  make new-notebook NAME=x   Theory notebook"
	@echo "  make new-paper NAME=x      Academic paper"
	@echo "  make preview               Quarto live preview"
	@echo "  make render                Build Quarto site to _site/"
	@echo "  make figures               Regenerate Solow–Swan essay figures"
	@echo "  make zip NAME=slug         Bundle post → bundles/<slug>.zip"
	@echo "  make zip-all               Bundle every Quarto post"
	@echo "  make publish               Publish to GitHub Pages"
	@echo "  make quarto-doctor         Quarto install check"

setup sync:
	cd $(REPO) && uv sync --all-groups

doctor:
	$(EL) doctor

list:
	$(EL) list

new-post:
	@test -n "$(NAME)" || (echo "NAME= required" && exit 1)
	$(EL) new post $(NAME) --domain $(DOMAIN)

new-notebook:
	@test -n "$(NAME)" || (echo "NAME= required" && exit 1)
	$(EL) new notebook $(NAME) --domain $(DOMAIN)

new-paper:
	@test -n "$(NAME)" || (echo "NAME= required" && exit 1)
	$(EL) new paper $(NAME) --domain $(DOMAIN)

new-project:
	@test -n "$(NAME)" || (echo "NAME= required" && exit 1)
	$(EL) new project $(NAME) --domain $(DOMAIN)

new-data:
	@test -n "$(NAME)" || (echo "NAME= required" && exit 1)
	$(EL) new data $(NAME) --domain $(DOMAIN)

new-dataset:
	@test -n "$(NAME)" || (echo "NAME= required" && exit 1)
	$(EL) new dataset $(NAME) --domain $(DOMAIN)

new-model:
	@test -n "$(NAME)" || (echo "NAME= required" && exit 1)
	$(EL) new model $(NAME) --domain $(DOMAIN)

quarto-doctor:
	@$(QUARTO) --version
	cd $(REPO) && $(QUARTO) check

preview:
	cd $(REPO) && $(QUARTO) preview

render:
	cd $(REPO) && $(QUARTO) render

figures:
	cd $(REPO) && uv run --python 3.12 python posts/solow-swan-tang-truong/scripts/generate_figures.py

zip:
	@test -n "$(NAME)" || (echo "NAME= required (post slug)" && exit 1)
	cd $(REPO) && uv run --python 3.12 python scripts/bundle_post.py $(NAME)

zip-all:
	cd $(REPO) && uv run --python 3.12 python scripts/bundle_post.py --all

publish:
	cd $(REPO) && $(QUARTO) publish gh-pages --no-prompt

lint:
	cd $(REPO) && uv run ruff check packages

test:
	cd $(REPO) && uv run pytest
