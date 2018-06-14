PORT=8080

init-prod:
	pip install -r requirements/prod.txt

init-dev:
	pip install -r requirements/dev.txt

gen-doc:
	doxygen conf.py
	cd docs/code/html && python -m http.server $(PORT)