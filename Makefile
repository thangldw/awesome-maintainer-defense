.PHONY: audit audit-evaluate audit-test distribution-test documentation-test kit-test links metadata package pilot-test pilot-verify pins quickstart-test render standalone test validate

PYPROJECT_BUILD ?= python3 -m build

audit:
	python3 scripts/install_kit.py audit .

audit-test:
	python3 scripts/test_auditor.py

documentation-test:
	python3 scripts/test_documentation.py

audit-evaluate:
	python3 scripts/evaluate_auditor.py

kit-test:
	python3 scripts/test_install_kit.py

quickstart-test:
	python3 scripts/test_quickstart.py

pilot-test:
	python3 scripts/test_pilot_bundle.py

pilot-verify:
	python3 scripts/verify_pilot_evidence.py

test: documentation-test audit-test kit-test quickstart-test pilot-test

standalone:
	python3 scripts/build_standalone.py

package: standalone
	$(PYPROJECT_BUILD)
	python3 scripts/build_plugin_bundle.py

distribution-test:
	python3 scripts/test_distribution.py
	python3 scripts/test_plugin_bundle.py

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
