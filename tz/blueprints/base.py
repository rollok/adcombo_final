# -*- coding: utf-8 -*-
from flask import Blueprint, request, session, redirect, url_for, render_template

import psycopg2
import psycopg2.extras


# create our blueprint :)    
bp = Blueprint('tz', __name__)

def db_execute(query, **kwargs):
    """
      postgres://postgres:mysecretpassword@172.17.0.2:5432/postgres
    """
    error = None
    try:
        if 'db_url' in session:
            conn = psycopg2.connect(session['db_url'])
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(query, kwargs)
            rows = cur.fetchall()
            return error, [dict(row) for row in rows]

        return error, []
    except Exception as e:
        error = "I am unable to connect to the database %s" % str(e)
        return error, []

@bp.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        session['db_url'] = request.form['db_url']
        return redirect(url_for('tz.index'))

    #toDo rename
    error, table_indexes = db_execute(
        """
        SELECT table_name from information_schema.tables
        WHERE table_schema = 'public'
        """
    )

    return render_template(
        'index.html',
        table_indexes=table_indexes,
        error=error,
    )

@bp.route('/table_info/<table_name>')
def table_info(table_name):
    error, rows = db_execute(
        """
        SELECT column_name, column_default, data_type from information_schema.columns
        WHERE table_name = %(table_name)s
        """,
        table_name=table_name
    )
    return render_template(
        'list_of_dict.html',
        error=error,
        rows=rows,
    )

@bp.route('/table_indexes/<table_name>')
def table_indexes(table_name):
    error, rows = db_execute(
        """
        SELECT schemaname, tablename, indexname, indexdef from pg_indexes
        WHERE tablename = %(table_name)s
        """,
        table_name=table_name
    )

    return render_template(
        'list_of_dict.html',
        error=error,
        rows=rows,
    )

@bp.route('/table_constraint/<table_name>')
def table_constraint(table_name):
    error, rows = db_execute(
        """
        SELECT conname, contype
        FROM pg_constraint
        WHERE conrelid = (
            SELECT oid
            FROM pg_class
            WHERE relname LIKE %(table_name)s
        )
        """,
        table_name=table_name
    )
    return render_template(
        'list_of_dict.html',
        error=error,
        rows=rows,
    )


@bp.route('/table_relations/<table_name>')
def table_relations(table_name):
    error, rows = db_execute(
        """
        SELECT
          (SELECT r.relname FROM pg_class r where r.oid = c.conrelid) AS table,
          (SELECT array_agg(attname) FROM pg_attribute
           WHERE attrelid = c.conrelid and ARRAY[attnum] <@ c.conkey) AS col,
          (SELECT r.relname FROM pg_class r WHERE r.oid = c.confrelid) AS ftable
        FROM pg_constraint c
        WHERE c.confrelid = (
            SELECT oid FROM pg_class WHERE relname = %(table_name)s
        )
        """,
        table_name=table_name
    )
    return render_template(
        'list_of_dict.html',
        error=error,
        rows=rows,
    )


@bp.route('/db_funcs_info')
def db_funcs_info():
    error, rows = db_execute(
        """
        SELECT  p.proname
        FROM    pg_catalog.pg_namespace n
        JOIN    pg_catalog.pg_proc p
        ON      p.pronamespace = n.oid
        WHERE   n.nspname = 'public'
        """
    )
    return render_template(
        'functions.html',
        error=error,
        rows=rows,
    )
