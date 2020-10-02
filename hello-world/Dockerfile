from tiangolo/uvicorn-gunicorn-fastapi:python3.7
RUN pip install --no-cache-dir psycopg2
RUN pip install --no-cache-dir jinja2
copy main.py /app
Expose 8000