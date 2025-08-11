# Test runner script for Printerify backend (Windows version)

@echo off
echo Starting Printerify backend tests...

REM Run Django tests
echo Running Django tests...
python manage.py test api.tests

REM Run pytest tests (if any)
echo Running pytest tests...
pytest api/tests/ -v

REM Generate coverage report
echo Generating coverage report...
coverage run --source=. manage.py test api.tests
coverage report
coverage html

echo Tests completed. HTML coverage report available in htmlcov/ directory.