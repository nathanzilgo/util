install:
	pip install -r requirements.txt

clean:
	rm -rf dist/

lint:
	pylint src/ --fail-under=8

format:
	black src

test:
	pytest
