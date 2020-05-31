test:
	pytest --tb=short -v

test-fast:
	pytest -k "not test_functional" --tb=short
