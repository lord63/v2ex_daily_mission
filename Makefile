test:
	@py.test -v tests/;
	@py.test --pep8 tests/ v2ex_daily_mission/;

create:
	@python setup.py sdist bdist_wheel;

upload:
	@python setup.py sdist bdist_wheel upload;
