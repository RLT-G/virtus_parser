.PHONY: run migrate makemigrations shell test superuser install req freeze lint format

# =======================================
#  ENV
# =======================================

VENV=.venv
PY=$(VENV)/bin/python
PIP=$(VENV)/bin/pip
DJ=$(PY) manage.py

# =======================================
#  SETUP
# =======================================

install:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

req:
	$(PIP) install -r requirements.txt

freeze:
	$(PIP) freeze > requirements.txt

# =======================================
#  SERVER
# =======================================

run:
	$(DJ) runserver 0.0.0.0:8000

# =======================================
#  DB
# =======================================

migrate:
	$(DJ) migrate

makemigrations:
	$(DJ) makemigrations

superuser:
	$(DJ) createsuperuser

# =======================================
#  DEV
# =======================================

shell:
	$(DJ) shell

test:
	$(DJ) test
