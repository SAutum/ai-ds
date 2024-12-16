import flask
import psycopg
from html import escape

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
DATABASE_URL = "postgresql://postgres:123456@127.0.0.1:5432/postgres"

@app.route("/table/<tablename>/<int:n>")
def get_table_data(tablename,n):
    try:
        # check the table name
        if not tablename.isidentifier():
            return "Invalid tablename",400
        # build the connection
        with psycopg.connect(DATABASE_URL) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_name = %s""",(tablename,))
                if not cursor.fetchone():
                    return "Table does not exist",400
        
                # query the table
                query = f"SELECT * FROM {tablename} LIMIT %s;"
                cursor.execute(query,(n,))
                rows = cursor.fetchall()
        
                # get the column
                columns = [desc[0] for desc in cursor.description]
        
            # return data
            html = "<table border='1'>"
            html += "<tr>" + "".join([f"<th>{escape(col)}</th>" for col in columns]) + "</tr>"
            for row in rows:
                html += "<tr>" +"".join([f"<td>{escape(str(cell))}</td>" for  cell in row]) + "</tr>"
            html += "</table>"
            return html
            
    except Exception as e:
        return escape(str(e)), 400
# b)
@app.route("/year-state")
def year_state():
    try:
        with psycopg.connect(DATABASE_URL) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                SELECT timestamp.year AS year, shop.state AS state, SUM(product.price * sale.quantity) AS revenue 
                FROM sale 
                JOIN product ON sale.product_id = product.product_id 
                JOIN shop ON sale.shop_id = shop.shop_id 
                JOIN timestamp ON sale.timestamp_id = timestamp.timestamp_id 
                GROUP BY timestamp.year, shop.state ORDER BY timestamp.year, shop.state;
                """)
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                
            html = "<table border='1'>"
            html += "<tr>" + "".join([f"<th>{escape(col)}</th>" for col in columns]) + "</tr>"
            for row in rows:
                html += "<tr>" +"".join([f"<td>{escape(str(cell))}</td>" for  cell in row]) + "</tr>"
            html += "</table>"
            return html
            
    except Exception as e:
        return escape(str(e)), 400


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
