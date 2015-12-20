

test:
	python -m unittest discover

coverage:
	coverage run --source app -m unittest discover 
	coverage report -m

clean:
	rm .coverage
	rm -rf *.pyc
