from flask import request, Blueprint, render_template, jsonify
from app.libs import ip_utils

core = Blueprint("core", __name__)


@core.route("/")
def index():
    """
    Renders index page.
    :return:
    :rtype:
    """
    return render_template("index.html")


@core.route("/ip_query_datatable/datastream", methods=["GET"])
def ip_query_datatable_datastream():
    """
    Server side processing of IP query DataTables.
    :return:
    :rtype:
    """
    row_table = ip_utils.get_datatable_result(request.args.to_dict())
    return jsonify(row_table)
