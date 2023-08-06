from flask import Flask, jsonify, request
from flask_cors import CORS
from pyhive import hive
from werkzeug.debug import get_current_traceback
from flask import make_response
from functools import wraps, update_wrapper
from datetime import datetime

def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return update_wrapper(no_cache, view)

app = Flask(__name__)

# Needed if front-end is not hosted by flask
CORS(app)

def connect_to_spark(request):
    spark_host = request.args.get('host',default='0.0.0.0',type=str)
    spark_port = request.args.get('port',default=10000,type=int)
    conn = hive.Connection(host=spark_host,port=int(spark_port))
    return conn

@app.route('/')
@nocache
def index():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
@nocache
def all_other_routes(path):
    return app.send_static_file(path)


def describe_table(connection, tableName):
    """return the name and datatype of each column in table"""

    def get_columndefs(rows):
        partition_def=False
        partition_columns=[]
        columns={}
        for row in rows:
            if row['col_name'] in ["# Partition Information", "# col_name"]:
                partition_def=True
            elif partition_def==False:
                columns[row['col_name']] = row['data_type']
            else:
                partition_columns.append(row["col_name"])
        return columns,partition_columns

    result = read_sql('describe ' + tableName, connection)
    columns,partition_columns = get_columndefs(result)
    return {'name':tableName,'columns':columns,'partitionColumns':partition_columns}

@app.route('/tables')
@nocache
def get_tables():
    conn = connect_to_spark(request)

    def get_catalog(connection):
        result = read_sql('show tables',connection)
        tables = map(lambda r : r['tableName'],result)
        return tables


    tables = get_catalog(conn)
    return jsonify([describe_table(conn,t) for t in tables])

@app.route('/columns/<string:table>/<string:columns>')
@nocache
def get_analyzed_columns(table,columns):
    conn = connect_to_spark(request)
    def analyze_columns(connection,table,cols):
        cols = list(map(lambda c : '`' + c + '`',cols))
        df = pd.read_sql('analyze olap table ' + table + ' 100 percent columns ' + ','.join(cols),connection)
        # get only relevant columns
        df = df[['ColumnName','Type','Distinct Count','Count',"PercentMissing", "PercentUnique"]]
        # rename the columns as expected by client
        df.columns = ['name','type','distinct_count','count',"percent_missing","percent_unique"]
        json_rows = df.to_dict(orient='record')
        return json_rows

    columns_list = columns.split(',')

    return jsonify(analyze_columns(conn,table,columns_list))


def read_sql(sql, conn):
    cursor = conn.cursor()
    cursor.execute(sql)
    header = list(map(lambda l : l[0],cursor.description))
    rows = cursor.fetchall()
    dicts = list(map(lambda r: dict(zip(header,r)),rows))
    return dicts

@app.route('/sql/<string:sql>')
@nocache
def do_sql(sql):

    conn = connect_to_spark(request)
    format = request.args.get('format',default='json',type=str)
    base64 = request.args.get('base64', default=False, type=bool)

    if base64:
        import base64
        sql = base64.b64decode(str(sql)).decode().replace('\n', ' ')
        app.logger.info("running decoded SQL: " + str(sql) )
    else:
        app.logger.info("running SQL: " + str(sql) )


    try:
        result = read_sql(sql,conn)
    except hive.OperationalError as e:
        app.logger.error('Operational Error: %s', e)
        msg = e.args[0].status.errorMessage
        trace = e.args[0].status.infoMessages
        return generate_error(msg, code=400, trace=trace)
    except hive.DatabaseError as e:
        app.logger.error('Database Error: %s', e)
        return generate_error(e, code=400)
    except Exception as e:
        app.logger.error('Exception: ' + repr(e))
        return generate_error(e)
    else:
        if format=='json':
            return jsonify(result)
        else:
            return jsonify(message="Result format '{}' is not supported".format(format))

@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error('Server Error: %s', (error))
    return generate_error(error)

def generate_error(error,code = 500,trace = []):
    if trace == []:
        trace = list(get_current_traceback(skip=1, show_hidden_frames=True,ignore_system_exceptions=False).generate_plaintext_traceback())
    return jsonify(message=repr(error),stacktrace=trace), code
