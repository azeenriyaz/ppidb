from flask import (render_template,
                Blueprint,
                send_from_directory,
                request,
                redirect,
                url_for,
                session,
                current_app
                )
from .constants import PPIConstants


PPIBP = Blueprint('PPIBP', __name__)

constants = PPIConstants()
routes = constants.routes
ui_text = constants.ui_text
util_fns = constants.utils_fns

@PPIBP.get(routes.Home.url)
def home():
    return render_template(routes.Home.template,
                            constants = constants,
                            routes = routes,
                            ui_text = ui_text,
                            page_title = routes.Home.title)

@PPIBP.get(routes.Browse.url)
def browse():
    return render_template(routes.Browse.template,
                            constants = constants,
                            routes = routes,
                            ui_text = ui_text,
                            page_title = routes.Browse.title)


@PPIBP.get(routes.Search.url)
def search():
    return render_template(routes.Search.template,
                            constants = constants,
                            routes = routes,
                            ui_text = ui_text,
                            page_title = routes.Search.title)

@PPIBP.get(routes.About.url)
def about():
    return render_template(routes.About.template,
                            constants = constants,
                            routes = routes,
                            ui_text = ui_text,
                            page_title = routes.About.title)

@PPIBP.get(routes.Table_view.url)
def table_view(table):
    table_df = constants.db.get_table_df(table)
    return render_template(routes.Table_view.template,
                            table_df = table_df,
                            constants = constants,
                            routes = routes,
                            ui_text = ui_text,
                            page_title = routes.Table_view.title)

@PPIBP.get(routes.Search_Result.url)
def search_result(table_select, column, term):
    result_df = constants.db.search_term_in_table(table=table_select, column_initials=column, term=term)
    if session.get('filter_dict') == True:
        result_df = constants.db.filter_dataframe(result_df, session['filter_dict'])
        session.pop('filter_dict', default=None)
    return render_template(routes.Table_view.template,
                            constants = constants,
                            routes = routes,
                            ui_text = ui_text,
                            table_df = result_df,
                            page_title = routes.Table_view.title)

@PPIBP.get(routes.download.url)
def download(filename):
    return send_from_directory(directory = routes.download.folder,
                                path = filename,
                                as_attachment=True)

@PPIBP.get(routes.Search_Term.url)
def searchCol():
    query_type = request.args['query_type']
    query_term = request.args['search']
    results = constants.db.searchCols(query_type, query_term)
    return results

@PPIBP.get(routes.Get_Search_Term.url)
def get_search_term():
    return render_template(routes.Get_Search_Term.template, constants = constants)

@PPIBP.get(routes.Form_submit.url)
def handle_form():
    form_dict = {
        'table-select': request.args.get('table-select'),
        'search-col-1-query-type': request.args.get('search-col-1-query-type'),
        'search-col-1-query-term': request.args.get('search-col-1-query-term')
    }
    session['filter_dict'] = util_fns.create_filter_dict(form_dict, request.args)
    return redirect(url_for('PPIBP.search_result', table_select=form_dict['table-select'], column = form_dict['search-col-1-query-type'], term = form_dict['search-col-1-query-term']))
