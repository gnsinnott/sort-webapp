from flask import request, make_response, render_template, redirect, url_for, flash, jsonify, make_response
from datetime import datetime as dt
from flask import current_app as app

from .models import db, Record, ScrapReasons, RecordSchema
from .forms import SearchForm, EditForm, NewScrap, EditScrap, BigEdit

import csv
from io import StringIO

def totalScrap(id):
    record = Record.query.get(id)
    total = record.Assembly + record.BadThreads
    print(total)

@app.route("/")
def home():
    return render_template(
        'home.html',
        title="Elgin Sort Data Site",
        description="Portal to access Elgin sort data."
    )

@app.route("/newrecord")
def new_record():
    # Create a user via query string parameters
    Employee = 'greg'
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
            CastShift=2
        )
        db.session.add(new_record)  # Adds new User record to database
        db.session.commit()  # Commits all changes
    return make_response(f"{new_record} successfully created!")

@app.route("/info")
def info():
    return("Hello World")

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
    dateCriteria = request.args.get('date') #Date sent in args, should add other search criteria
    partCriteria = request.args.get('part')
    jobCriteria = request.args.get('job')
    if not partCriteria:
        partCriteria = ""
    if not dateCriteria:
        dateCriteria = "2021" # If no date arg use 2021, should maybe only show active???
    if not jobCriteria:
        jobCriteria = ""

    memoryString = StringIO() #object in memory not on disk
    write = csv.writer(memoryString)
    records = Record.query.filter(
            Record.StartTime.startswith(dateCriteria),
            Record.Part.startswith(partCriteria),
            Record.Job.startswith(jobCriteria)).limit(20).all()
    exportRecords = Record.query.filter(
            Record.StartTime.startswith(dateCriteria),
            Record.Part.startswith(partCriteria),
            Record.Job.startswith(jobCriteria)).all()
    write.writerows(records)
    response = make_response(memoryString.getvalue())
    response.headers['Content-Disposition'] = 'attachment, filename=report.csv'
    response.headers['Content-type'] = "text/csv"
    return response()
    print (type(records))
    return render_template(
        'records.html',
        records=records
    )

@app.route("/edit_record/<id>", methods=['POST', 'GET'])
def edit_record(id):
    record = Record.query.get(id)
    
    edit_form = EditForm(obj=record)

    if edit_form.is_submitted():
        print("submitted")
    if edit_form.validate():
        print("valid")
        edit_form.populate_obj(record)
        db.session.commit()
        return redirect("/records")
    
    print(edit_form.errors)


    return render_template(
        'edit_records2.html',
        edit_form = edit_form,
        template = "form-template"
    )

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

@app.route("/api/v1/records/", methods=['GET'])
def api_id():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "No ID found"

    rs = RecordSchema()

    result = Record.query.get(id)
    return jsonify(rs.dump(result))
    
@app.route("/api/v1/new_record", methods=['GET', 'POST'])
def upload_record():
    record_schema = RecordSchema()
    json_data = request.get_json()
    if not json_data:
        return {"message": "No input data provided"}
    data = record_schema.load(json_data)
    employee = data["Employee"]
    starttime = data["StartTime"]
    tablenumber = data["TableNumber"]
    job = data["Job"]
    part = data["Part"]
    GoodQuantity = data["GoodQuantity"]

    new_record = Record(Employee=employee, StartTime=starttime, TableNumber=tablenumber, Job=job, Part=part, GoodQuantity=GoodQuantity)
    employee = data['Employee']
    db.session.add(new_record)
    db.session.commit()
    return employee

@app.route("/api/v1/finish_record", methods=['GET', 'POST'])
def finish_record(id):
    record_schema = RecordSchema()
    record = Record.query.get(id)
    json_data = request.get_json()
    if not json_data:
        return{"message": "No input data provided"}
    data = record_schema.load(json_data)
    

    return "Hello"
