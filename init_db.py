import sqlite3
from flask import Flask, render_template, request

PERSON_TABLE = "create table if not exists person" \
               " (id INTEGER PRIMARY KEY AUTOINCREMENT, " \
               "first_name TEXT NOT NULL, " \
               "last_name TEXT NOT NULL, " \
               "email TEXT UNIQUE NOT NULL, " \
               "lat FLOAT (10,6) NOT NULL, " \
               "lng FLOAT (10,6) NOT NULL, " \
               "address TEXT NOT NULL)"
CYCLE_TABLE = "create table if not exists cycle" \
              " (id INTEGER PRIMARY KEY AUTOINCREMENT, " \
              "model_name TEXT NOT NULL, " \
              "model_number TEXT NOT NULL, " \
              "stationId Integer NOT NULL, " \
              "address TEXT NOT NULL)"
STATION_TABLE = "create table if not exists station" \
                " (id INTEGER PRIMARY KEY AUTOINCREMENT, " \
                "station_name TEXT NOT NULL, " \
                "lat FLOAT (10,6) NOT NULL, " \
                "lng FLOAT (10,6) NOT NULL, " \
                "address TEXT NOT NULL)"
ADD_STATION = "INSERT into station(station_name,lat,lng,address) values (?,?,?,?)"
ADD_CYCLE = "INSERT into cycle(model_name,model_number,stationId,address) values (?,?,?,?)"

con = sqlite3.connect("smart_cycle.db")
print("Database opened successfully")
con.execute(PERSON_TABLE)
con.execute(CYCLE_TABLE)
con.execute(STATION_TABLE)
print("All tables created")
con.close()

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/add")
def add():
    return render_template("add.html")


@app.route('/savedetails', methods=['POST', 'GET'])
def saveDetails():
    msg = "message"
    if request.method == "POST":
        try:
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            email = request.form["email"]
            address = request.form["address"]
            with sqlite3.connect("smart_cycle.db") as con:
                cur = con.cursor()
                cur.execute("INSERT into person(first_name,last_name,email,address) values (?,?,?,?)",
                            (first_name, last_name, email, address))
                con.commit()
                msg = "Person Added Successfully"
        except:
            con.rollback()
            msg = "We cannot add the person to the list"
        finally:
            return render_template("success.html", msg=msg)
            con.close()


@app.route('/delete-record', methods=["POST"])
def deleterrecord():
    msg = "No Value"
    id = request.form["id"]
    with sqlite3.connect("smart_cycle.db") as con:
        try:
            cur = con.cursor()
            cur.execute("delete from person where id=?", id)
            msg = "record successfully deleted"
        except:
            msg = "cant be deleted"
        finally:
            return render_template("delete_record.html", msg=msg)
        con.close()


@app.route("/delete")
def delete():
    return render_template("delete.html")


@app.route("/view")
def view():
    con = sqlite3.connect("smart_cycle.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from person")
    row = cur.fetchall()
    return render_template("view.html", rows=row)


@app.route('/update-location')
def updatePersonLocation():
    msg = "Null value"
    lng = request.form["lng"]
    lat = request.form["lat"]
    id = request.form["id"]
    print(lng + " " + lat + " " + msg)
    with sqlite3.connect("smart_cycle.db") as con:
        try:
            cur = con.cursor()
            cur.execute(f"update from person set lnt = {lng}, lat = {lat}, where id={id}")
            msg = "record successfully updated"
        except:
            msg = "cant be updated"
        finally:
            return render_template("update_location_record.html", msg=msg)
        con.close()


@app.route("/update")
def update():
    return render_template("update_location.html")


# Cycle Endpoints
@app.route("/add-cycle")
def addCycle():
    return render_template("cycle/add_cycle.html")


@app.route('/savecycledetails', methods=['POST', 'GET'])
def saveCycleDetails():
    msg = "message"
    if request.method == "POST":
        try:
            model_name = request.form["model_name"]
            model_number = request.form["model_number"]
            stationId = request.form["stationId"]
            address = request.form["address"]
            with sqlite3.connect("smart_cycle.db") as con:
                cur = con.cursor()
                cur.execute("INSERT into cycle(model_name,model_number,stationId,address) values (?,?,?,?)",
                            (model_name, model_number, stationId, address))
                con.commit()
                msg = "Cycle Added Successfully"
        except:
            con.rollback()
            msg = "We cannot add the cycle to the list"
        finally:
            return render_template("cycle/success_cycle.html", msg=msg)
            con.close()


@app.route("/view-cycle")
def viewCycle():
    con = sqlite3.connect("smart_cycle.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from cycle")
    row = cur.fetchall()
    return render_template("cycle/view_cycle.html", rows=row)


@app.route('/delete-record-cycle', methods=["POST"])
def deleterecord():
    id = request.form["id"]
    with sqlite3.connect("smart_cycle.db") as con:
        try:
            cur = con.cursor()
            cur.execute("delete from cycle where id=?", id)
            msg = "record successfully deleted"
        except:
            msg = "cant be deleted"
        finally:
            return render_template("cycle/delete_cycle_record.html", msg=msg)
        con.close()


@app.route("/delete-cycle")
def deleteCycle():
    return render_template("cycle/delete_cycle.html")

@app.route('/update-cycle-location')
def updateCycleLocation():
    stationId = request.form["stationId"]
    id = request.form["id"]
    with sqlite3.connect("smart_cycle.db") as con:
        try:
            cur = con.cursor()
            cur.execute(f"update from cycle set stationId = {stationId}, where id={id}")
            msg = "record successfully updated"
        except:
            msg = "cant be updated"
        finally:
            return render_template("cycle/update_cycle_record.html", msg=msg)
        con.close()


@app.route("/update-cycle")
def updateCycle():
    return render_template("cycle/update_cycle.html")
# Station Endpoints
@app.route("/add-station")
def addStation():
    return render_template("station/add_station.html")


"station_name TEXT NOT NULL, " \
"lat FLOAT (10,6) NOT NULL, " \
"lng FLOAT (10,6) NOT NULL, " \
"address TEXT NOT NULL)"


@app.route('/save-station-details', methods=['POST', 'GET'])
def saveStationDetails():
    msg = "message"
    if request.method == "POST":
        try:
            station_name = request.form["station_name"]
            lat = request.form["lat"]
            lng = request.form["lng"]
            address = request.form["address"]
            with sqlite3.connect("smart_cycle.db") as con:
                cur = con.cursor()
                cur.execute("INSERT into station(model_name,model_number,stationId,address) values (?,?,?,?)",
                            (station_name, lat, lng, address))
                con.commit()
                msg = "Station Added Successfully"
        except:
            con.rollback()
            msg = "We cannot add the station to the list"
        finally:
            return render_template("station/success_station.html", msg=msg)
            con.close()


@app.route("/view-station")
def viewStation():
    con = sqlite3.connect("smart_cycle.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from station")
    row = cur.fetchall()
    return render_template("station/view_station.html", rows=row)


@app.route('/delete-record-station', methods=["POST"])
def deleterecordStation():
    id = request.form["id"]
    with sqlite3.connect("smart_cycle.db") as con:
        try:
            cur = con.cursor()
            cur.execute("delete from station where id=?", id)
            msg = "record succesfully deleted"
        except:
            msg = "cant be deleted"
        finally:
            return render_template("station/delete_station_record.html", msg=msg)
        con.close()


@app.route("/delete-station")
def deleteStation_template():
    return render_template("station/delete_station.html")


if __name__ == "__main__":
    app.run(debug=True)
