#!/bin/bash

# rm -rf pytest/reports/*

# Ensure required directories exist
mkdir -p pytest/reports/junit
mkdir -p pytest/reports/allure-results
mkdir -p pytest/reports/coverage
mkdir -p pytest/reports/pylint

# Run tests and generate reports
coverage run -m pytest --junitxml=pytest/reports/junit/junit-report.xml --html-report=pytest/reports/pytest-html-reporter-report.html  --html=pytest/reports/pytest-html-report.html
# --alluredir=pytest/reports/allure-results : ui had permissions issues when running in docker
coverage html -d pytest/reports/coverage/htmlcov
coverage xml -o pytest/reports/coverage/coverage.xml
pylint . > pytest/reports/pylint/report.txt
