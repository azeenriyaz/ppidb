from wtforms import StringField, SubmitField
from flask import render_template
import pandas as pd
from flask_wtf import FlaskForm

class PPISearchForm(FlaskForm):
    search_term = StringField('Search')
    submit = SubmitField("Submit")


class PPIUtils:
    @staticmethod
    def error_handler(e):
        return render_template("error.html", code=e)


class PPIRoute:
    def __init__(self, url, title, template, **kwargs):
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

    def get_table_df(self, limit=100):
        sql = f"select * from `{self.table_name}` limit {limit};"
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
    
    def search_term_in_table(self, table, column_initials, term):
        columns_query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{tbl}' AND COLUMN_NAME LIKE %s"
        # read only the necessary data from the database using a SQL query
        data_frames = []
        table_names_list = self.table_names
        if table != 'all':
            table_names_list = [table]
        for tbl in table_names_list:
            columns = pd.read_sql_query(columns_query.format(tbl=tbl, col=column_initials), self.engine, params=('%'+column_initials+'%',))['COLUMN_NAME'].tolist()
            try:
                for col in columns:
                    query = "SELECT * FROM {tbl} WHERE {col} LIKE %s LIMIT 1000"
                    data = pd.read_sql_query(query.format(col=col, tbl=tbl), self.engine, params=('%'+term+'%',))
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
