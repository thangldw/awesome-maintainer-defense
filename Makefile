.PHONY: links render validate

links:
	python3 scripts/check_links.py

render:
	python3 scripts/render.py

validate:
	python3 scripts/validate.py
