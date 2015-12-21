

test:
	python -m unittest discover

coverage:
	coverage run --source app -m unittest discover 
	coverage report -m

clean:
	rm -rf .coverage
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d | xargs rm -fr
