.PHONY: audit audit-evaluate audit-test distribution-test kit-test links metadata package pins quickstart-test render standalone test validate

audit:
	python3 scripts/install_kit.py audit .

audit-test:
	python3 scripts/test_auditor.py

audit-evaluate:
	python3 scripts/evaluate_auditor.py

kit-test:
	python3 scripts/test_install_kit.py

quickstart-test:
	python3 scripts/test_quickstart.py

test: audit-test kit-test quickstart-test

standalone:
	python3 scripts/build_standalone.py

package: standalone
	python3 -m build

distribution-test:
	python3 scripts/test_distribution.py

links:
	python3 scripts/check_links.py

metadata:
	python3 scripts/verify_metadata.py

pins:
	python3 scripts/verify_pins.py

render:
	python3 scripts/render.py
	python3 scripts/render_audit.py
	python3 scripts/evaluate_auditor.py

validate:
	python3 scripts/validate.py
