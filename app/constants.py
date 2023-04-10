from .utils import PPIRoute, Database
from .template_constants import template_tags, template_script_tags
from flask_app import PPIApp
from flask import render_template_string

class PPIConstants():
    Home = PPIRoute("/","Home", "main/home.html")
    Search = PPIRoute("/search/","Search", "main/search.html")
    Browse = PPIRoute("/browse/","Browse", "main/browse.html")
    About = PPIRoute("/about/","About", "main/about.html")
    download = PPIRoute("/output/<path:filename>", "" , "" ,folder = "output/")
    Table_view = PPIRoute("/view/<table>","View", "main/table.html")
    Form_submit = PPIRoute("/form_submit/","", "")
    Search_Result = PPIRoute("/view/search_result/<table_select>/<column>/<term>/", "View", "main/table.html")
    Search_Term = PPIRoute("/search_term/","","")
    Get_Search_Term = PPIRoute("/get_search_term","","modules/search_term.html")


    navbar_routes = ['Browse', 'Search', 'About']
    about_details = {
        'name' : 'Rawal Genomics Lab',
        'address' : '316, Third floor, J3 block',
        'email' : 'kamal.rawal@gmail.com',
        'university' : 'Amity University, Noida'
    }
    copyright = "Copyright"
    software_title = 'PPIDB'
    landing_title = 'Protein-Protein Interaction Database'
    landing_message = 'These are specific physical or functional contacts between proteins that occur in any biological context as a result of molecular docking and occurrence. Such PPI networks can provide a complementary view to the biological pathways that enclose the corresponding proteins.'

    select_database_msg = "Select Database"

    def __init__(self):
        pass
    template_tags = template_tags
    template_script_tags = template_script_tags
    def generate_tag_templates(self, template_tags, app, url_for):
        tag_templates = {}
        with app.app_context():
            for tag_name, tag_attrs in template_tags.items():
                tag_templates[tag_name] = []
                for attr_name, attr_values in tag_attrs.items():
                    tag_template = "<{tag}"
                    attr_template = " {attr}='{value}'"
                    tag_template = tag_template.format(tag=tag_name)
                    tag_template += attr_template.format(attr='name', value=attr_name)
                    for attr_name, attr_value in attr_values.items():
                        if '{{' in attr_value and '}}' in attr_value:
                            # Render the Jinja2 template here
                            attr_value = render_template_string(attr_value, url_for=url_for)
                        tag_template += attr_template.format(attr=attr_name, value=attr_value)
                    tag_template += "></{tag}>\n".format(tag=tag_name)
                    tag_templates[tag_name].append(tag_template)
                tag_templates[tag_name] = "".join(tag_templates[tag_name])
        return tag_templates




    db = Database(PPIApp())
