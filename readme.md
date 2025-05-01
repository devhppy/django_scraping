# List project tree
tree -a -I '__pycache__|*.pyc|*.pyo|*.sqlite3|*.log|*.env|*.DS_Store|node_modules|migrations|*venv|*ipynb*' -L 3

# Running celery
celery -A devhome worker --beat -l info
