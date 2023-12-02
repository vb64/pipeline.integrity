python -m flake8 pipeline_integrity
python -m flake8 tests/test
python -m pydocstyle pipeline_integrity
python -m pydocstyle --match='.*\.py' tests/test
python -m pylint --rcfile .pylintrc2 pipeline_integrity
python -m pylint --rcfile .pylintrc2 tests/test
pytest --cov=pipeline_integrity --cov-report term:skip-covered --durations=5 tests
