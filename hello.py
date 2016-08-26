from flask import Flask, render_template
from flask.ext.pymongo import PyMongo


app = Flask(__name__)
mongo = PyMongo(app)


@app.route("/hello/<name>"  )
def hello(name=None):
    return render_template('hello.html')

#
# livereload server
#
from livereload import Server, shell
from formic import FileSet
from os import getcwd, path

def make_livereload_server(wsgi_app):
    server = Server(wsgi_app)

    watch_patterns = (
        "/**",
        "/templates/**"
    )


    build_cmd = "make"

    print "Livereload: Files are being watched and will be liver ealoaded:"

    cwd = getcwd()

    for pattern in watch_patterns:
        print "Pattern: ", pattern
        for filepath in FileSet(include=pattern):
            print "=>", path.relpath(filepath, cwd)
            server.watch(filepath, build_cmd)
        print

    return server


def main():
    # wire livereload to Flask via wsgi
    flask_wsgi_app = app.wsgi_app
    server = make_livereload_server(flask_wsgi_app)
    # serve application
    server.serve()

if __name__ == "__main__":
    main()
