#!/bin/bash

echo "Waiting for 60 seconds to allow SonarQube to start..."
sleep 60
sonar-scanner \
  -Dsonar.projectKey=DemoApp \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://sonarqube:9000 \
  -Dsonar.login=squ_af46316a3d95016df0434848976e577e66b0a90c
