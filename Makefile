.PHONY: kit-test links metadata pins render standalone validate

kit-test:
	python3 scripts/test_install_kit.py

standalone:
	python3 scripts/build_standalone.py

links:
	python3 scripts/check_links.py

metadata:
	python3 scripts/verify_metadata.py

pins:
	python3 scripts/verify_pins.py

render:
	python3 scripts/render.py
	python3 scripts/render_audit.py

validate:
	python3 scripts/validate.py
