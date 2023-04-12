from wtforms import StringField, SubmitField
from flask import render_template, render_template_string
import pandas as pd
from flask_wtf import FlaskForm
from uuid import uuid4

class PPISearchForm(FlaskForm):
    search_term = StringField('Search')
    submit = SubmitField("Submit")


class PPIUtils:
    @staticmethod
    def error_handler(e):
        return render_template("error.html", code=e)
    def create_filter_dict(self, form_dict, request_args):
        filter_dict = {}
        for key in request_args.keys():
            filter_dict[key] = request_args[key]
        dict_copy = dict(filter_dict)
        for key, value in form_dict.items():
            if key in dict_copy and dict_copy[key] == value:
                del dict_copy[key]
        filter_dict = Database.create_query_dict(self,dict_copy)
        
        return filter_dict
    
    def make_csv(self, df):
        filename = uuid4()
        file_url = f'downloads/{filename}'
        df.to_csv(file_url + ".csv")
        return file_url



class PPIRoute:
    def __init__(self, url, title, template):
        self.url = url
        self.title = title
        self.template = template


class PPIMessage:
    def __init__(self, message=None):
        self.message = message


class PPIUIMessage(PPIMessage):
    def __init__(self, message, ui_class):
        super().__init__(message)
        self.ui_class = ui_class


class PPIForm(FlaskForm):
    def __init__(self, form_data):
        super().__init__(form_data)

    @classmethod
    def from_request(cls, request):
        return cls(request.form)


class Database:
    def __init__(self, app):
        self.engine = app.__get_sql_engine__()
        self.table_names = self.engine.table_names()
        self.author_table_dict = {}
        
        self._build_author_table_dict()
        self.search_keys = list(pd.read_sql_table("non_redundant_data", con = self.engine))

    def get_table_df(self, table, limit=100):
        if limit == 'infinity':
            sql = f"select * from `{table}`;"
        else:
            sql = f"select * from `{table}` limit {limit};"
        return pd.read_sql(sql, con=self.engine)

    def _build_author_table_dict(self):
        authors = []
        for table in self.table_names:
            author = table[table.find("$")+1:table.find("_")].capitalize().replace("-", " ")
            if author not in authors:
                authors.append(author)
                self.author_table_dict[table[table.find("$")+1:table.find("_")]] = []
            for key in self.author_table_dict:
                if table[table.find("$")+1:table.find("_")] == key:
                    self.author_table_dict[table[table.find("$")+1:table.find("_")]].append({
                        f'{table[table.find("_")+1:].replace("_"," ").capitalize()}' : f'{table}'
                    })
    
    def searchCols(self, col, term):
        sql = f"select `{col}` from non_redundant_data where `{col}` like '%%{term}%%' limit 100;"
        if term == '':
            sql = f"select `{col}` from non_redundant_data limit 100;"
        vals = pd.read_sql(sql,con=self.engine)
        vals_list = vals[col].to_list()
        vals_list_upd = []
        for i in vals_list:
            vals_list_upd.extend(str(i).split('\n'))
            vals_list_upd.extend(str(i).splitlines(True))
        vals_result = []
        for i,val in enumerate(vals_list_upd):
            vals_result.append({
                'id': i,
                'text' : val
            })
        return vals_result
    
    def search_term_in_table(self, table, column_initials, term, limit = 1000):
        columns_query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{tbl}' AND COLUMN_NAME LIKE %s"
        # read only the necessary data from the database using a SQL query
        data_frames = []
        table_names_list = self.table_names
        if table != 'All Tables':
            table_names_list = [table]
        for tbl in table_names_list:
            columns = pd.read_sql_query(columns_query.format(tbl=tbl, col=column_initials), self.engine, params=('%'+column_initials+'%',))['COLUMN_NAME'].tolist()
            try:
                for col in columns:
                    if limit == 'infinity':
                        query = "SELECT * FROM {tbl} WHERE {col} LIKE %s"
                    else:
                        query = "SELECT * FROM {tbl} WHERE {col} LIKE %s LIMIT {limit}"
                    data = pd.read_sql_query(query.format(col=col, tbl=tbl, limit = limit), self.engine, params=('%'+term+'%',))
                    data_frames.append(data)
            except:
                # if the column is not found in the table, skip the table
                pass

        if data_frames:
            data = pd.concat(data_frames)
        else:
            data = pd.DataFrame()

        # return the result as a Pandas DataFrame
        # get the list of columns sorted by whether they are empty or not
        cols = data.columns.tolist()
        cols.sort(key=lambda x: data[x].isnull().sum())

        # reindex the DataFrame with the sorted column list
        data = data.reindex(columns=cols)

        return data
    
    def filter_dataframe(self, df, criteria):
        # Create an empty dataframe to store the filtered rows
        filtered_df = pd.DataFrame()

        # Loop through the criteria and filter the dataframe accordingly
        for column, value in criteria.items():
            filtered_df = filtered_df.append(df[df[column] == value])

    def create_query_dict(self, original_dict):
        query_dict = {}
        for key, value in original_dict.items():
            if 'type' in key:
                num = key.split('-')[2] # Extract the query type from the key
                query_dict[value] = original_dict[f'search-col-{num}-query-term'] # Use f-string to get the query term value
        return query_dict
    

class PPIUI():
    
    def __init__(self):
        pass

    def generate_tag_templates(self, template_tags, app, url_for):
        tag_templates = {}
        with app.app_context():
            for tag_name, tag_attrs in template_tags.items():
                tag_templates[tag_name] = []
                for attr_name, attr_values in tag_attrs.items():
                    tag_template = "<{tag}"
                    attr_template = " {attr}='{value}'"
                    tag_template = tag_template.format(tag=tag_name)
                    
                    for attr_name, attr_value in attr_values.items():
                        if '{{' in attr_value and '}}' in attr_value:
                            # Render the Jinja2 template here
                            attr_value = render_template_string(attr_value, url_for=url_for)
                        tag_template += attr_template.format(attr=attr_name, value=attr_value)
                    tag_template += "></{tag}>\n".format(tag=tag_name)
                    tag_templates[tag_name].append(tag_template)
                tag_templates[tag_name] = "".join(tag_templates[tag_name])
        return tag_templates
