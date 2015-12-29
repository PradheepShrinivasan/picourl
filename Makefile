test:
	python -m unittest discover
	
env:
	sudo easy_install pip && \
	pip install virtualenv && \
	virtualenv env && \
	. venv/bin/activate && \
	make deps

activate:
	(\
	venv/bin/activate \
	)

deps:
	pip install -r requirements.txt --use-mirrors



coverage:
	coverage run --source app -m unittest discover 
	coverage report -m

clean:
	rm -rf .coverage
	rm -rf .coverage
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d | xargs rm -fr
