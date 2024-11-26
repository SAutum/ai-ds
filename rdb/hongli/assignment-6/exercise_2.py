import flask
import psycopg
from werkzeug.utils import escape

app = flask.Flask(__name__)


@app.route("/")
def index():
    return """
    <style>@keyframes colorful {
        0% {color: #f80}
        25% {color: #0f0}
        50% {color: #0ff}
        75% {color: #ff0}
        100% {color: #f80}
    }</style>
    <h1 style="animation:colorful 3s infinite;text-align:center;font-family:Arial">
    🌲🌲🌲Welcome to the Harz Online Shopping Analytics Platform!🌲🌲🌲</h1>"""


# Your solution goes here.
def connect_database():
    conn = psycopg.connect()
    cursor = conn.cursor()
    return conn, cursor


def construct_html_main_body(title, table):
    main_body = f"""<!DOCTYPE html>
            <html>
                <head>
                    <meta charset="utf-8">
                    <title>{title}</title>
                </head>
                <body>
                    <div class="container">
                        <div class="table">{table}</div>
                    </div>
                </body>
            </html>
            """
    return main_body


#### functions for returning first n rows of the requested table
@app.route("/table/<table_name>/<n>")
def show_n_rows(table_name, n):
    # connect to database
    conn, cursor = connect_database()

    return_404 = "404: I can't find the table you're looking for, or \
        your input number of rows is invalid"

    # check if the table and rows are valid
    if check_table_name(table_name, cursor):
        n = check_n(table_name, n, cursor)
        if n < 0:
            return return_404
    else:
        return return_404

    cursor.execute(f"""SELECT *
                       FROM {table_name}
                       LIMIT {n}""")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    # construct table
    table = f"<h2 style = 'text-algin:center;'>{table_name}</h2> <table><tr> "
    for column in columns:
        table += f"<td>{escape(column)}</td>"
    table += "</tr>"
    for row in rows:
        table += "<tr>"
        for item in row:
            table += f"<td>{escape(item)}</td>"
        table += "/<tr>"

    table += "</table>"

    return construct_html_main_body(table_name, table)


# check if the table name is allowed
def check_table_name(table_name, cursor):
    available_tables = ["product", "sale", "shop", "timestamp"]
    return (table_name in available_tables)


# check if number n is valid and if it exceeds the limit
def check_n(table_name, n, cursor):
    try:
        n = int(n)
    except ValueError:
        return -1
    # the table name is already checked
    cursor.execute("SELECT COUNT(*) FROM {}".format(table_name))
    total_n = cursor.fetchall()[0][0]

    if n > total_n:
        return -1
    else:
        return n


@app.route("/year-state")
def show_year_state_revenue():
    # there isn't any input from user or attribute value
    # I would say no need to consider SQL injection
    conn, cursor = connect_database()

    # prepare crosstab function
    conn.execute("CREATE EXTENSION IF NOT EXISTS tablefunc;")

    # prepare the columns for the pivot table
    query_columns = f"""
            SELECT DISTINCT
                year
            FROM
                timestamp
            ORDER BY
                year
            """
    cursor.execute(query_columns)
    columns = cursor.fetchall()
    column_text = 'ct ("state" TEXT '
    for column in columns:
        column_text += f', "{escape(column[0])}" FLOAT'
    column_text += " )"

    # Select year, state and calculate aggregated revenues
    query = """
            SELECT
                shop_id, timestamp_id, quantity * price AS revenue
            FROM
                sale
            JOIN
                product
            USING
                (product_id)
        """

    query = f"""
            SELECT
                timestamp_id, SUM(revenue) as revenue, state
            FROM
                shop
            JOIN
                ({query})
            USING
                (shop_id)
            GROUP BY
                state, timestamp_id
            """

    query = f"""
            SELECT
                state, year, SUM(revenue) AS aggregated_revenue
            FROM
                timestamp
            JOIN
                ({query})
            USING
                (timestamp_id)
            GROUP BY
                1, 2
            ORDER BY
                1, 2
        """

    query = f"""
            SELECT *
            FROM  crosstab('
            {query}',
            '{query_columns}'
            ) AS
            {column_text}
            """

    cursor.execute(query)
    rows = cursor.fetchall()

    # construct pivot table
    table = "<h2 style = 'text-algin:center;'>revenue per state per year</h2> <table><tr> "
    table += "<td> State </td>"
    for column in columns:
        table += f"<td>{escape(column[0])}</td>"
    table += "</tr>"
    for row in rows:
        table += "<tr>"
        for i, item in enumerate(row):
            if i != 0:
                table += f"<td>{escape(item)}&#8364;</td>"
            else:
                table += f"<td>{escape(item)}</td>"
        table += "/<tr>"

    table += "</table>"

    return construct_html_main_body("revenue per state per year", table)

if __name__ == "__main__":
    # app.run(host="127.0.0.1", port=5000)
    app.run(host="0.0.0.0", port=5000)
