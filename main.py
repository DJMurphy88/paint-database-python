import database
from objects import Paint, Project
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/")
def index():
    database.connect()
    database.checkDatabasePaints()

    count = database.getCount()
    colours = database.getColours()
    low = database.getLow()
    depleted = database.getDepleted()
    missing = len(depleted)

    database.close()

    return render_template("index.html", count=count, colours=colours, missing=missing, low=low, depleted=depleted)

@app.route("/paints", methods=["GET"])
def paintList():

    database.connect()
    paints = database.getPaints()
    database.close()

    colours = []
    for paint in paints:
        if paint.paint_colour not in colours:
            colours.append(paint.paint_colour)

    return render_template('paintlist.html', paints=paints, colours=colours)

@app.route("/paintsubmission")
def paintsubmission():
    return render_template("paintsubmission.html")

@app.route("/paintsubmission", methods=["POST"])
def getAddPaint():
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

    return redirect("paints")

@app.route("/paintupdate", methods=["GET"])
def paintupdate():
    if request.method == "GET":
        paint_id = request.args.get("paintid")
        database.connect()
        paint = database.getPaint(paint_id)
        database.close()

        return render_template("paintupdate.html", paint=paint)

@app.route("/paintupdate", methods=["POST"])
def getPaintData():
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

    return redirect("paints")

@app.route("/paintdelete", methods=["GET", "POST"])
def paintdelete():
    paint_id = request.args.get("paintid")

    database.connect()
    paint = database.getPaint(paint_id)
    database.deletePaint(paint_id)
    database.close()

    return redirect("list")

@app.route("/projects", methods=["GET"])
def projectList():

    database.connect()
    projects = database.getProjects()
    database.close()

    return render_template('projectlist.html', projects=projects)

@app.route("/projectsubmission", methods=["GET"])
def getAddProject():
    project_name = request.values["name"]
    project_system = request.values["system"]

    database.connect()
    project = Project(project_name, project_system)
    database.addProject(project)
    database.close()

    return redirect("projects")

@app.route("/projectupdate", methods=["GET"])
def projectUpdate():
    pass

@app.route("/projectupdate", methods=["POST"])
def getProjectData():
    pass

@app.route("/projectdelete", methods=["GET", "POST"])
def projectDelete():
    pass
