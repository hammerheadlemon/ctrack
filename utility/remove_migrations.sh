#!/usr/bin/env bash

echo "Removing migrations from all migrations directories, except in .venv..."
 
find . -path "*/migrations/*.py" -not -name "__init__.py" -not -path "./.venv/*" -delete
find . -path "*/migrations/*.pyc" -not -path "./.venv/*"   -delete
find . -path "*/migrations/__pycache__" -not -path "./.venv/*"  -delete
