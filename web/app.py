"""
Kaetlyn Gibson's Flask API.
"""

from flask import Flask, abort, render_template, send_from_directory
import os
import config

app = Flask(__name__)
forbidden_values = ("~", "//", "..")

@app.route("/")
def hello():
    return "UOCIS docker demo!\n"

@app.route("/<path:file_name>")
def find(file_name):
    fv_count = 0
    options = config.configuration()
    DOCROOT = options.DOCROOT
    source_path = os.path.join(options.DOCROOT, file_name)

    # checking: if page starts with (~ // ..)
    for val in forbidden_values:
        if val in file_name:
            fv_count += 1
    if fv_count > 0:
        # if 1 or more forbidden values present,
        # response: 403 forbidden
        abort(403)
    else:
        # checking: if name.html NOT in current directory
        if not os.path.isfile(source_path):
            # response: 404 not found
            abort(404)
        else:
            # file is in current directory
            # response: content of .html or .ccs file w/ proper http response
            return send_from_directory(DOCROOT, file_name), 200

@app.errorhandler(403)
def errForbidden(e):
    """ For 403: forbidden error message """
    return render_template('403.html'), 403

@app.errorhandler(404)
def errNotFound(e):
    """ For 404: not found error message"""
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
