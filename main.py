import database
from objects import Paint
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/")
def index():
    database.connect()
    database.checkDatabase()

    count = database.getCount()
    colours = database.getColours()
    low = database.getLow()
    depleted = database.getDepleted()
    missing = len(depleted)

    database.close()

    return render_template("index.html", count=count, colours=colours, missing=missing, low=low, depleted=depleted)

@app.route("/list", methods=["GET"])
def paintList():
    sort = request.args.get("sort")

    database.connect()
    paints = database.getPaints()
    database.close()

    return render_template('list.html', paints=paints, sort=sort)

@app.route("/submission")
def submission():
    return render_template("submission.html")

@app.route("/submission", methods=["POST"])
def getAddData():
    paint_id = request.values["paintid"]
    paint_name = request.values["name"]
    paint_type = request.values["type"]
    pot_amount = int(request.values["amount"])
    pot_status = request.values["status"]
    paint_colour = request.values["colour"]
    hexcode = request.values["hexcode"]

    database.connect()
    paint = Paint(paint_id, paint_name, paint_type, pot_amount, pot_status, paint_colour, hexcode)
    database.addPaint(paint)
    database.close()

    return redirect("list")

@app.route("/update", methods=["GET"])
def update():
    if request.method == "GET":
        paint_id = request.args.get("paintid")
        database.connect()
        paint = database.getPaint(paint_id)
        database.close()

        return render_template("update.html", paint=paint)

@app.route("/update", methods=["GET", "POST"])
def getUpdateData():
    paint_id = request.args.get("paintid")
    database.connect()

    paint_name = request.values["name"]
    paint_type = request.values["type"]
    pot_amount = int(request.values["amount"])
    pot_status = request.values["status"]
    paint_colour = request.values["colour"]
    hexcode = request.values["hexcode"]

    database.updatePaint(paint_id, paint_name, paint_type, pot_amount, pot_status, paint_colour, hexcode)
    database.close()

    return redirect("list")

@app.route("/delete", methods=["GET", "POST"])
def delete():
    paint_id = request.args.get("paintid")

    database.connect()
    paint = database.getPaint(paint_id)
    database.deletePaint(paint_id)
    database.close()

    return redirect("list")
