

test:
	python -m unittest discover

coverage:
	coverage run --source app -m unittest discover 
	coverage report -m

clean:
	rm -rf .coverage
	rm -rf *.pyc
