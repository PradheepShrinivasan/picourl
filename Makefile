test:
	python3 -m unittest discover
	
env:
	pip3 install virtualenv && \
	virtualenv env && \
	. venv/bin/activate && \
	make deps

activate:
	. venv/bin/activate 

deps:
	pip3 install -r requirements.txt 

coverage:
	coverage3 run --source app -m unittest discover 
	coverage3 report -m

clean:
	rm -rf .coverage
	rm -rf .coverage
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d | xargs rm -fr
