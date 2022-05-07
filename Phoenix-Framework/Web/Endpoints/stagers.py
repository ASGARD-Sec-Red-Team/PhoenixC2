from Utils import *
from Web.Endpoints.authorization import authorized, admin
from Creator import get_stager, create_stager

stagers = Blueprint("stagers", __name__, url_prefix="/stagers")


@stagers.route("/", methods=["GET"])
@authorized
def index():
    return render_template("stagers.html")


@stagers.route("/add", methods=["POST"])
@authorized
def post_add():
    """Add a stager
    Request Body Example:
    {
        "listener": "1",
        "name": "Test Stager1"
    }
    """
    # Get Form Data
    listener_id = request.form.get("listener")
    name = request.form.get("name")

    # Check if Data is Valid
    if not listener_id or not name:
        abort(400, "Missing required data")

    # Create Stager
    try:
        create_stager(name, listener_id)
    except Exception as e:
        return str(e)
    else:
        log(f"Created Stager {name} with Listener {listener_id}", "success")
        return f"Stager {name} created"


@stagers.route("/remove", methods=["DELETE"])
@authorized
def delete_remove():
    """Remove a stager
    \nRequest Args Example:
    \nhttp://localhost:8080/stagers/remove?id=1
    """

    # Get Request Data
    id = request.args.get("id")
    try:
        id = int(id)
    except ValueError:
        return "Invalid ID", 400

    # Check if Stager exists
    curr.execute("SELECT * FROM Stagers WHERE ID = ?", (id,))
    if not curr.fetchone():
        return f"Stager with ID {id} does not exist", 404
    curr.execute("DELETE FROM Stagers WHERE ID = ?", (id,))
    conn.commit()
    log(f"Deleted Stager with ID {id}", "info")
    return f"Removed Stager with ID {id}"


@stagers.route("/edit", methods=["PUT"])
@authorized
def put_edit():
    """Edit a stager
    Request Body Example:
    {
        "id": "1",
        "change": "name",
        "value": "Test Stager1"
    }"""

    # Get Request Data
    change = request.form.get("change")
    id = request.form.get("id")
    value = request.form.get("value")

    # Check if Data is Valid
    if not change or not value or not id:
        abort(400, "Missing required data")

    try:
        id = int(id)
    except ValueError:
        return abort(400, "Invalid ID")

    # Check if Stager exists
    curr.execute("SELECT * FROM Stagers WHERE ID = ?", (id,))
    if not curr.fetchone():
        return f"Stager with ID {id} does not exist", 404

    log("Edited {change} to {value} for Stager with ID {id}", "sucess")
    # Change Stager
    if change == "name":
        curr.execute("UPDATE Stagers SET Name = ? WHERE ID = ?", (value, id))
        conn.commit()
        return f"Changed Stager with ID {id} to {value}"
    else:
        return f"Invalid Change", 400


@stagers.route("/download", methods=["GET"])
@authorized
def post_download():
    """Download a stager
    \nRequest Args Example:
    \nhttp://localhost:8080/stagers/download?id=1&encoding=base64&random_size=True&timeout=5000&format=py&delay=10
    """
    # Get Request Data
    id = request.args.get("id")
    encoding = request.args.get("encoding")
    random_size = request.args.get("random_size")
    timeout = request.args.get("timeout")
    format = request.args.get("format")
    delay = request.args.get("delay")

    # Check if Data is Valid
    if not id or not encoding or not random_size or not timeout or not format or not delay:
        abort(400, "Missing required data")
    try:
        id = int(id)
    except ValueError:
        return "Invalid ID", 400
    try:
        timeout = int(timeout)
    except ValueError:
        return "Invalid Timeout", 400
    try:
        delay = int(delay)
    except ValueError:
        return "Invalid Delay", 400
    # Check if Stager exists
    curr.execute("SELECT * FROM Stagers WHERE ID = ?", (id,))
    if not curr.fetchone():
        return f"Stager with ID {id} does not exist", 404

    # Get Stager
    try:
        stager = get_stager(id, encoding, True if random_size.lower(
        ) == "true" else False, timeout, format, delay)
    except Exception as e:
        return str(e), 400
    else:
        if format == "py":
            return stager
        elif format == "exe":
            with open("stager.exe", "wb") as f:
                f.write(stager)

            return send_file("/tmp/stager.exe", as_attachment=True, download_name=f"stager.exe")


@stagers.route("/list", methods=["GET"])
@authorized
def get_list():
    """Get a list of stagers"""
    curr.execute("SELECT * FROM Stagers")
    stgers = curr.fetchall()
    data = []
    for stger in stgers:
        data.append(
            {"id": stger[0], "name": stger[1], "listener": stger[2]})
    return jsonify(data)