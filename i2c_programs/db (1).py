import sqlite3

import click
from flask import current_app, g
from datetime import datetime, timedelta


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def insert(table, data):
    db = get_db()
    sql = "INSERT INTO {} (`{}`) VALUES ({})".format(table, "`,`".join([key for key in data.keys()]),
                                                     ",".join(['?' for key in data.keys()]))
    db.execute(sql, tuple([value for value in data.values()]))
    db.commit()
    print("data inserted")


def update(table, data, where):
    db = get_db()
    sql = "UPDATE {} SET {} WHERE {}".format(table, ",".join(["`{}`='{}'".format(k, v) for k, v in data.items()]),
                                             ",".join(["`{}`='{}'".format(key, value) for key, value in where.items()]))
    db.execute(sql)
    db.commit()
    print("data updated")


def select(table, columns=["*"], where=None):
    db = get_db()
    cur = db.cursor()
    sql = "SELECT {} FROM {}".format(",".join(columns), table)
    if where:
        sql = "{} WHERE {}".format(sql, ",".join(["`{}`='{}'".format(key, value) for key, value in where.items()]))
    data = cur.execute(sql)
    data = data.fetchall()
    if len(data) == 0:
        return None
    if len(columns) == 1 and columns[0] == "*":
        columns = get_columns(table)
    rows = []
    for row in data:
        for key, column in enumerate(columns):
            rows.append((column, row[key]))
    return dict(rows)


def select_one(table, columns=["*"], where=None):
    db = get_db()
    cur = db.cursor()
    sql = "SELECT {} FROM {}".format(",".join(columns), table)
    if where:
        sql = "{} WHERE {}".format(sql, ",".join(["`{}`='{}'".format(key, value) for key, value in where.items()]))
    data = cur.execute(sql)
    row = data.fetchone()
    if row is None:
        return None
    if len(columns) == 1 and columns[0] == "*":
        columns = get_columns(table)
    rows = []
    for key, column in enumerate(columns):
        rows.append((column, row[key]))
    return dict(rows)


def get_columns(table):
    db = get_db()
    cur = db.cursor()
    sql = "pragma table_info({});".format(table)
    data = cur.execute(sql)
    return [row[1] for row in data.fetchall()]


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    insert("sys_config", {
        "as_uid": "123654789",
        "systemId": "9874563210123654789",
        "deviceName": "eNose",
        "firmwareVersion": "V1.1.2023",
        "as_validityKey": datetime.utcnow() + timedelta(days=90),
        "createdAt": datetime.utcnow()
    })


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
