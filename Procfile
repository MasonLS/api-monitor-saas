web: gunicorn src.wsgi:app
worker: python src/monitor.py
release: python -c "print('Release phase: Database will be auto-created on first run')"
