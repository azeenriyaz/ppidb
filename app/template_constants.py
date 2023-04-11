template_tags = {
        'link' : {
            'main' : {
                'rel' : 'stylesheet',
                'href' : "{{ url_for('static',filename = 'css/main.css') }}",
            },
            'bootstrap' : {
                'rel' : 'stylesheet',
                'href' : 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css',
            },
            'DataTables' : {
                'rel' : 'stylesheet',
                'href': 'https://cdn.datatables.net/1.10.2/css/jquery.dataTables.min.css',
            },
            'apple-touch-icon' : {
                'rel': 'apple-touch-icon',
                'sizes': '180x180',
                'href' : "{{ url_for('static',filename = 'img/apple-touch-icon.png') }}",
            },
            'icon' : {
                'type': 'image/x-icon',
                'href' : "{{ url_for('static',filename = 'img/favicon.ico') }}",
            },
            'icon-32' : {
                'type': 'image/png',
                'sizes': '32x32',
                'href' : "{{ url_for('static',filename = 'img/favicon-32x32.png') }}",
            },
            'icon-16' : {
                'type': 'image/png',
                'sizes': '16x16',
                'href' : "{{ url_for('static',filename = 'img/favicon-16x16.png') }}",
            }
        },
        'meta' : {
            'viewport' : {
                'name' : 'viewport',
                'content' : 'width=device-width, initial-scale=1.0',
            },
            'description' : {
                'name' : 'description',
                'content' : 'This is a web server which renders the the Protein-Protein Interaction Database data in a user-friendly format.',
            },
            'keywords' : {
                'name' : 'keywords',
                'content' : 'Protein-Protein Interaction, Database, Web Server, Protein, Interaction',
            },
            'title' : {
                'name' : 'viewport',
                'content' : 'PPIDB',
            },
            'author' : {
                'name' : 'viewport',
                'content' : 'Azeen Riyaz',
            },
            'robots' : {
                'name' : 'viewport',
                'content' : 'index, follow',
            },
            'language' : {
                'name' : 'viewport',
                'content' : 'English',
            },
        }
    }

template_script_tags = {
        'script' : {
            'jquery' : {
                'src': 'https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js',
            },
            'bootstrap_bundle' : {
                'src': 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js',
            },
            'DataTables' :  {
                'src': 'https://cdn.datatables.net/1.10.2/js/jquery.dataTables.min.js',
            },
            'functions' : {
                'src' : "{{ url_for('static',filename = 'js/functions.js') }}",
            },
            'script' : {
                'src' : "{{ url_for('static',filename = 'js/script.js') }}",
            },
        },
}