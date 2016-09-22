import os
import os.path
import sqlite3
import sys
try:
    from modules.query_builder import QueryBuilder as qb
    from modules.arg_parser import parse_args
except ImportError:
    from mtg_lookup.modules.query_builder import QueryBuilder as qb
    from mtg_lookup.modules.arg_parser import parse_args
#from modules.print_facilities import print_results
data_db_file = 'mtg_lookup/data.db'

conn = sqlite3.connect(data_db_file)
qb.attach_connection(conn)

def do_search(s,results_page_string):
    sys.argv = [None]
    arr = s.split('|')
    for el in arr:
        sys.argv.append(el)
    parse_args()
    qb.make_query()
    arr = []
    for el in qb.cursor_results:
        s = el['NAME'] + '</br>' + el['TYPE'] + '\n' + el['CARD_TEXT'] + '</br>'
        arr.append(s)
    qb.reset_vars()
    return results_page_string.format('</br>'.join(arr))
