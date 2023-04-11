from .utils import PPIRoute

class Routes():
    def __init__(self):
        pass

    Home = PPIRoute("/","Home", "main/home.html")
    Search = PPIRoute("/search/","Search", "main/search.html")
    Browse = PPIRoute("/browse/","Browse", "main/browse.html")
    About = PPIRoute("/about/","About", "main/about.html")
    download = PPIRoute("/output/<path:filename>", "" , "" , folder = "output/")
    Table_view = PPIRoute("/view/<table>","View", "main/table.html")
    Form_submit = PPIRoute("/form_submit/","", "")
    Search_Result = PPIRoute("/view/search_result/<table_select>/<column>/<term>/", "View", "main/table.html")
    Search_Term = PPIRoute("/search_term/","","")
    Get_Search_Term = PPIRoute("/get_search_term","","modules/search_term.html")
