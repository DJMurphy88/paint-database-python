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

    database.connect()
    paints = database.getPaints()
    database.close()

    colours = []
    for paint in paints:
        if paint.paint_colour not in colours:
            colours.append(paint.paint_colour)

    return render_template('list.html', paints=paints, colours=colours)

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
    brand = request.values["brand"]

    database.connect()
    paint = Paint(paint_id, paint_name, paint_type, pot_amount, pot_status, paint_colour, hexcode, brand)
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

@app.route("/update", methods=["POST"])
def getUpdateData():
    paint_id = request.values["paintid"]
    paint_name = request.values["name"]
    paint_type = request.values["type"]
    pot_amount = int(request.values["amount"])
    pot_status = request.values["status"]
    paint_colour = request.values["colour"]
    hexcode = request.values["hexcode"]
    brand = request.values["brand"]

    print(f'id = {paint_id}')

    database.connect()
    database.updatePaint(paint_id, paint_name, paint_type, pot_amount, pot_status, paint_colour, hexcode, brand)
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
