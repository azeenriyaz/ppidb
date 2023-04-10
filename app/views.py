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


@PPIBP.get(constants.Home.url)
def home():
    constants.tags_template = constants.generate_tag_templates(constants.template_tags, current_app, url_for)
    constants.tags_html = "".join(constants.tags_template.values())
    constants.tags_script_template = constants.generate_tag_templates(constants.template_script_tags, current_app, url_for)
    constants.tags_script_html = "".join(constants.tags_script_template.values())
    return render_template(constants.Home.template,
                            constants = constants,
                            page_title = constants.Home.title)

@PPIBP.get(constants.Browse.url)
def browse():
    return render_template(constants.Browse.template,
                            constants = constants,
                            page_title = constants.Browse.title)


@PPIBP.get(constants.Search.url)
def search():
    return render_template(constants.Search.template,
                            constants = constants,
                            page_title = constants.Search.title)

@PPIBP.get(constants.About.url)
def about():
    return render_template(constants.About.template,
                            constants = constants,
                            page_title = constants.About.title)

@PPIBP.get(constants.Table_view.url)
def table_view(table):
    table_df = constants.db.get_table_df(table)
    return render_template(constants.Table_view.template,
                            table_df = table_df,
                            constants = constants,
                            page_title = constants.Table_view.title)

@PPIBP.get(constants.Search_Result.url)
def search_result(table_select, column, term):
    result_df = constants.db.search_term_in_table(table=table_select, column_initials=column, term=term)
    if session.get('filter_dict') == True:
        result_df = constants.db.filter_dataframe(result_df, session['filter_dict'])
        session.pop('filter_dict', default=None)
    return render_template(constants.Table_view.template,
                            constants = constants,
                            table_df = result_df,
                            page_title = constants.Table_view.title)

@PPIBP.get(constants.download.url)
def download(filename):
    return send_from_directory(directory = constants.download.folder,
                                path = filename,
                                as_attachment=True)

@PPIBP.get(constants.Search_Term.url)
def searchCol():
    query_type = request.args['query_type']
    query_term = request.args['search']
    results = constants.db.searchCols(query_type, query_term)
    return results

@PPIBP.get(constants.Get_Search_Term.url)
def get_search_term():
    return render_template(constants.Get_Search_Term.template, constants = constants)

@PPIBP.route(constants.Form_submit.url, methods = ["GET", "POST"])
def handle_form():
    form_dict = {
        'table-select': request.args.get('table-select'),
        'search-col-1-query-type': request.args.get('search-col-1-query-type'),
        'search-col-1-query-term': request.args.get('search-col-1-query-term')
    }
    filter_dict = {}
    for key in request.args.keys():
        filter_dict[key] = request.args[key]
    dict_copy = dict(filter_dict)
    for key, value in form_dict.items():
        if key in dict_copy and dict_copy[key] == value:
            del dict_copy[key]
    filter_dict = constants.db.create_query_dict(dict_copy)
    session['filter_dict'] = filter_dict
    return redirect(url_for('PPIBP.search_result', table_select=form_dict['table-select'], column = form_dict['search-col-1-query-type'], term = form_dict['search-col-1-query-term']))
