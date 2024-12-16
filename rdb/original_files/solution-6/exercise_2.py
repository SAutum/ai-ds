import flask

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


# BEGIN_SOLUTION
import psycopg
from psycopg import sql
import html

tables = ["sale", "product", "shop", "timestamp"]


# Serve first n rows of a specific table
@app.route("/table/<table>/<int:n>")
def table(table, n):
    # Need to whitelist tables to prevent access to internal tables like
    # pg_shadow which contains password hashes.
    if table not in tables:
        # Need to escape table to prevent XSS
        return f"Table {html.escape(table)} not found", 404

    with psycopg.connect() as conn:
        with conn.cursor() as cursor:
            # Use the SQL module to safely build a query with variable table
            # https://www.psycopg.org/docs/sql.html
            # Note that there are internal PostgreSQL tables which you probably
            # do not want to show to users. It is still a good idea to only
            # allow a limited number of tables, so this alone is not sufficient.
            query = sql.SQL("SELECT * FROM {table} ORDER BY {table_id} LIMIT %s").format(
                table=sql.Identifier(table), table_id=sql.Identifier(table + "_id")
            )

            cursor.execute(query, (n,))
            headers = [desc[0] for desc in cursor.description]
            rows = list(cursor.fetchall())

    # Flask render templates automatically escape things for us.
    # Could also use html.escape instead, but then you would have to remember
    # to use it every time, which is unreliable.
    return flask.render_template("table.html", title=table, headers=headers, rows=rows)


# Show aggregated revenue for each year and state
@app.route("/year-state")
def slice_year_state():
    with psycopg.connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT year, state, SUM(sale.quantity * product.price) AS revenue
                FROM sale
                JOIN timestamp ON sale.timestamp_id = timestamp.timestamp_id
                JOIN shop ON sale.shop_id = shop.shop_id
                JOIN product ON sale.product_id = product.product_id
                GROUP BY year, state
                ORDER BY year, state
            """)

            # Reorder results for nicer displaying
            revenue = {(year, state): revenue for year, state, revenue in cursor.fetchall()}
            states = sorted(set(state for _, state in revenue))
            years = sorted(set(year for year, _ in revenue))
            rows = [[state] + [f"{revenue.get((year, state), 0):,} €" for year in years] for state in states]

    # Flask render templates automatically escape things for us.
    return flask.render_template(
        "table.html",
        title="revenue per state per year",
        headers=["State"] + years,
        rows=rows,
    )


# Serve static files
@app.route("/static/<path:path>")
def serve_static(path):
    return flask.send_from_directory("static", path)


# END_SOLUTION

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
