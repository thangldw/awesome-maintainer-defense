.PHONY: links metadata render validate

links:
	python3 scripts/check_links.py

metadata:
	python3 scripts/verify_metadata.py

render:
	python3 scripts/render.py
	python3 scripts/render_audit.py

validate:
	python3 scripts/validate.py
