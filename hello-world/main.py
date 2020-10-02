import os
import platform
from datetime import datetime

import psycopg2
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# class RequestFormat(BaseModel):
#     address: str
#     hostname: str
#     url: str
#     time: str


def log_data(request: Request):
    conn = psycopg2.connect(host=os.environ['POSTGRES_HOST'],
                            database=os.environ['POSTGRES_DB'],
                            user=os.environ['POSTGRES_USER'],
                            password=os.environ['POSTGRES_PASSWORD'])
    cur = conn.cursor()
    keys = ["ip", "host", "requested_at", "path"]
    data = {
        "ip": request.client.host,
        "host": platform.node(),
        "path ": request.url.path,
        "requested_at": str(datetime.now())
    }
    print(data)
    values = [data.get(key, None) for key in keys]

    cmd = """INSERT INTO requests ( %s, %s, %s, %s) VALUES(
                  ' %s',
                    '%s',
                    '%s',
                    '%s'
                );""" % tuple(keys + values)
    print(cmd)
    cur.execute(cmd)
    conn.commit()
    cur.execute("select * from requests order by id desc limit 25;")
    last_25_data = [dict((cur.description[i][0], value)
                         for i, value in enumerate(row)) for row in cur.fetchall()]
    col_names = [cn[0] for cn in cur.description]
    cur.close()
    return col_names, last_25_data


@app.get("/")
def read_root(request: Request, response_class=HTMLResponse):
    header, data = log_data(request)
    return templates.TemplateResponse("item.html", {"items": data, "headers": header, "request": request})  # noqa
