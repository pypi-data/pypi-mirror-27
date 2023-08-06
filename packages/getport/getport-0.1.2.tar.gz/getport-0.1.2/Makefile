publish:
	pip install 'twine>=1.5.0'
	python setup.py sdist 
	twine upload dist/*
	rm -rf build dist .egg getport.egg-info
tests:
	pytest test
