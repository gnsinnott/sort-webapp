from flask import json, request, make_response, render_template, redirect, url_for, flash, jsonify, make_response, send_file, session
from datetime import datetime as dt, timedelta
from flask import current_app as app
from sqlalchemy.orm.query import LockmodeArg

from .models import db, Record, ScrapReasons, RecordSchema
from .forms import SearchForm, EditForm, NewScrap, EditScrap, BigEdit
import csv

from .log import log_this
import os.path

# Home page of website
@app.route("/")
def home():
    return render_template(
        'home.html',
        title="Elgin Sort Data Site",
        description="Portal to access Elgin sort data."
    )
# Generate new record, for testing purposes only
@app.route("/newrecord")
def new_record():
    # Create a user via query string parameters
    Employee = 'Number 9'
    if Employee:
        # Sample Data to create test records
        new_record = Record(
            Employee=Employee,
            StartTime=dt.now(),
            TableNumber=42,
            Job=90210,
            Part=9228008,
            GoodQuantity=125,
            Operation=20,
            CastDate=dt.now(),
            CastShift=2,
            EndTime=dt.now()
        )
        db.session.add(new_record)  # Adds new labor record to database
        db.session.commit()  # Commits all changes
    return make_response(f"{new_record} successfully created!")

# Search query form
# TODO Add more criteria filters
@app.route("/search", methods=['GET', 'POST'])
def search():
    form = SearchForm() 
    return render_template(
        'search.html',
        form=form,
        template="form-template"
    )

@app.route("/records", methods=['GET', 'POST'])
def records():
    criteria = {}
    # iterate over args and add it to criteria dictionary
    for key, value in request.args.items():
        criteria[key] = value
    # if no items added to criteria set all values to 0 and return limit to 20
    if len(criteria) == 0:
        returnLimit = 20
        startDateCriteria = "2021-01-01"
        endDateCriteria = dt.today().strftime('%Y-%m-%d')
        partCriteria = ""
        jobCriteria = ""
        employeeCriteria = "%"
    # else set each criteria to value sent
    else:
        returnLimit = -1
        if criteria['start_date'] != "" :
            startDateCriteria = criteria["start_date"]
        else:
            startDateCriteria = "2021-01-01"
        if criteria["end_date"] != "":
            endDateCriteria = dt.strptime(criteria["end_date"], '%Y-%m-%d') + timedelta(days = 1)
        else:
            endDateCriteria = dt.today() + timedelta(days = 1)
        partCriteria = criteria["part"]
        jobCriteria = criteria["job"]
        # employee criteria can't be blank "%" is used as wildcard for sql like searches
        if criteria["employee"] != "":
            employeeCriteria = criteria["employee"]
        else:
            employeeCriteria = "%"

    # query that only shows first 20 results
    records = Record.query.filter(
            Record.Obsolete == 0,
            Record.StartTime.between(startDateCriteria, endDateCriteria),
            Record.Part.startswith(partCriteria),
            Record.Employee.like(employeeCriteria),
            Record.Job.startswith(jobCriteria)).limit(returnLimit).all()

    # same query as above but includes all results, used for csv file download
    exportRecords = Record.query.filter(
        Record.Obsolete == 0,
        Record.StartTime.between(startDateCriteria, endDateCriteria),
        Record.Part.startswith(partCriteria),
        Record.Job.startswith(jobCriteria)).all()

    # create csv file with todays date, populate csv with query results for exportRecords
    # file created in downloads folder
    # add filename to session to allow download page to locate correct file
    session['filename'] = str(dt.now().strftime("%Y%m%d%H%M%S")) + ".csv"
    w_file = open(os.path.join("app/downloads",session.get('filename', None)), 'a')
    writer = csv.DictWriter(w_file, fieldnames=Record.__table__.columns.keys())
    writer.writeheader()
    # writes each row in query result to csv file
    for row in exportRecords:
        rowdict = row.__dict__
        rowdict.pop('_sa_instance_state', None)
        writer.writerow(rowdict)
    w_file.close()

    return render_template(
        'records.html',
        records=records
    )

# Show list of records that are active, where there is no EndTime
@app.route("/records/active", methods=['GET', 'POST'])
def active_records():
    records = Record.query.filter(
        Record.Obsolete == 0,
        Record.EndTime == None).all()
    return render_template(
        'active_records.html',
        records=records
    )

# Download of csv coresponding to filename passed thorugh session
@app.route("/records/download", methods=['GET', 'POST'])
def download_records():
    filename = session.get('filename', None)
    # serve file from downloads folder
    return send_file(os.path.join("downloads/",filename), mimetype='text/csv', attachment_filename=filename, as_attachment=True)

# Page that allows chaniging of all values in record
@app.route("/edit_record/<id>", methods=['POST', 'GET'])
def edit_record(id):
    # Retrive record from DB
    record = Record.query.get(id)
    rowdict = record.__dict__
    status = rowdict['Obsolete']
    # Populate edit_form with record
    edit_form = EditForm(obj=record)
    if edit_form.validate():
        edit_form.populate_obj(record)
        db.session.commit()
        return redirect(url_for('records'))
    # TODO Evaluate need or functionaly of this 
    with open('app/errors.txt', 'a') as errorFile:
        for key in edit_form.errors: 
            for value in edit_form.errors[key]:
                errorFile.write(key + ": " + value + "\n")


    return render_template(
        'edit_records.html',
        edit_form = edit_form,
        status = status,
        template = "form-template"
    )

#TODO evaluate deletion of this route
@app.route("/scrapreasons", methods=["POST", "GET"])
def scrapreasons():
    form = NewScrap()

    if form.validate_on_submit():
        new_reason = "\n" + request.form["scrap_reason"]
        with open('app/scrapreasons.txt', 'a') as file1:
            file1.write(new_reason)
        ScrapReasons.populate_table()
        return redirect("/scrapreasons")

    return render_template(
        'scrap_reasons.html',
        form = form,
        reasons = ScrapReasons.query.all()
        )

# API to retrive record by id number
@app.route("/api/v1/records/", methods=['GET'])
def api_id():
    # get id from args
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "No ID found"
    rs = RecordSchema()

    result = Record.query.get(id)
    try:
        log_this(rs.dump(result), "json.txt")
    except:
        log_this("rs dump fail", "json.txt")
    return jsonify(rs.dump(result))

# API to insert new record into database, accepts JSON data
@app.route("/api/v1/new_record", methods=['GET', 'POST'])
def upload_record():
    record_schema = RecordSchema()
    json_data = request.get_json()
    log_this(json_data, "json.txt")

    # Check if json data is recieved
    if not json_data:
        return {"message": "No input data provided", "error": True}

    # Set start time
    now = dt.now().strftime("%Y-%m-%d %H:%M:%S")
    json_data["StartTime"] = now

    # Convert json data into Record format as defined in models.py
    data = record_schema.load(json_data)
    new_record = Record()

    # Iterate through JSON data and assign each key value pair to matching key in new_record
    for key in data:
        new_record.__setattr__(key, data[key])

    # Commit new record to database
    db.session.add(new_record)
    db.session.commit()
    # Get ID of row created to be used in finalizing record
    id = new_record.id
    # Reply with JSON data including record ID
    return {"response" :"Record " + str(id) + " created", "error" : False, "index" : str(id)}

# API to complete a record, add scrap values and end time
@app.route("/api/v1/finish_record", methods=['GET', 'POST'])
def finish_record():
    json_data = request.get_json()
    log_this(json_data, "json.txt")
    # Retrieve record id from json_data and then delete it from json_data
    id = int(json_data['index'])
    json_data.pop("index")
    # Set End time
    now = dt.strptime(dt.now().strftime("%Y-%m-%d %H:%M:%S"),"%Y-%m-%d %H:%M:%S")
    json_data["EndTime"] = now
    # Select record from db
    record = Record.query.get(id)
    if not json_data:
        return{"message": "No input data provided"}
    # Iterate through JSON data and assign each key value pair to matching key in record
    for key in json_data:
        record.__setattr__(key, json_data[key])
    db.session.commit()   
    
    # Reply with convirmation of record update
    return{"response" : "Record " + str(id) + " updated", "error": False}

@app.route("/api/v1/delete_record", methods=['GET', 'POST'])
def delete_record():
    json_data = request.get_json()
    log_this("Delete", "json.txt")
    log_this(json_data, "json.txt")
    id = int(json_data["id"])
    record = Record.query.get(id)
    record.__setattr__('Obsolete', 1)
    db.session.commit()
    response = {"status": "true"}
    return response

@app.route("/api/v1/restore_record", methods=['GET', 'POST'])
def restore_record():
    json_data = request.get_json()
    log_this("Restore", "json.txt")
    log_this(json_data, "json.txt")
    id = int(json_data["id"])
    record = Record.query.get(id)
    record.__setattr__('Obsolete', 0)
    db.session.commit()
    response = {"status": "true"}
    return response
    

@app.route("/app/download", methods=['GET', 'POST'])
def app_downloads():
    return render_template(
        "downloads.html",
        title = "App Downloads"
    )
@app.route("/app/download/android", methods=['GET'])
def android_download():
    filename = 'app-release.apk'
    return send_file(os.path.join("android/latest/", filename), mimetype='application/vnd.android.package-archive', attachment_filename=filename, as_attachment=True)
