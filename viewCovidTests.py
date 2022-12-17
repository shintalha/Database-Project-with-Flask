from flask import render_template, flash, request
from werkzeug.utils import redirect
from datetime import datetime,date
import numpy as np

from model.covid_tests import *

def tests_page(id = -1):
    page_id = int(request.args.get('page')) if request.args.get('page') is not None else 1
    loc_name = request.args.get('loc_name') if request.args.get('loc_name') is not None else "?"
    date = request.args.get('date') if request.args.get('date') is not None else "?"
    end_date = request.args.get('end_date') if request.args.get('end_date') is not None else "?"
    covid_tests = CovidTests()
    if id != -1:
        covid_tests.delete(int(id))
        
    #page_id = 1
    #loc_name = "Antigua_and_Barbuda"
    #date = "2020-03-13"
    #end_date = "?"
        
    loc_name = loc_name.replace("_"," ")
    
    loc_names = covid_tests.get_location_names()
    offset = (page_id-1)*50
    paginationValues = (page_id-1,page_id,page_id+1) if (page_id)>1 else (1,2,3)
    covid_data = np.array(covid_tests.read(50,offset,loc_name,date,end_date))
    while(covid_data.size == 0):
        if offset == 0:
            covid_data = np.zeros([1, len(covid_tests.columns)], dtype='str')
            break
        offset = 0
        covid_data = np.array(covid_tests.read(50,offset,loc_name,date,end_date))
            
    start_dates = covid_tests.get_dates(loc_name)
    headers = covid_tests.columns

    del covid_tests
    return render_template("tests/tests.html", table_headers=headers, table_rows = covid_data[:,0:9], \
        paginationValues=paginationValues, locations = loc_names, dates = start_dates) 

def add_tests_page():
    covid_test = CovidTests()
    message = "empty"

    if request.method == "POST":   
        location_id = request.form["location_id"]
        total_tests = request.form["total_tests"]
        new_tests = request.form["new_tests"] 
        total_tests_per_thousand = request.form["total_tests_per_thousand"] if request.form["total_tests_per_thousand"] !="" else None
        new_tests_per_thousand = request.form["new_tests_per_thousand"] if request.form["new_tests_per_thousand"] !="" else None
        new_tests_smoothed = request.form["new_tests_smoothed"] if request.form["new_tests_smoothed"] !="" else None
        positive_rate = request.form["positive_rate"] if request.form["positive_rate"] !="" else None
        date_time = request.form["date_time"] if request.form["date_time"] !="" else None
        result = covid_test.insert_row(location_id, total_tests, new_tests, total_tests_per_thousand, new_tests_per_thousand, new_tests_smoothed, positive_rate, date_time)
        if result:
            message = "success"  
        else:
            message = "failed" 
    return render_template("tests/add-tests.html", message=message) 

def update_tests_page():
    row_id = int(request.args.get('id'))
    covid_test = CovidTests()
    row = np.array(covid_test.read_by_id(row_id))
    message = "empty"
    if request.method == "POST":   
        location_id = request.form["location_id"] if request.form["location_id"] !="" else row[1]
        total_tests = request.form["total_tests"] if request.form["total_tests"] !="" else row[2]
        new_tests = request.form["new_tests"] if request.form["new_tests"] !="" else row[3]
        total_tests_per_thousand = request.form["total_tests_per_thousand"] if request.form["total_tests_per_thousand"] !="" else row[4]
        new_tests_per_thousand = request.form["new_tests_per_thousand"] if request.form["new_tests_per_thousand"] !="" else row[5]
        new_tests_smoothed = request.form["new_tests_smoothed"] if request.form["new_tests_smoothed"] !="" else row[6]
        positive_rate = request.form["positive_rate"] if request.form["positive_rate"] !="" else row[7]
        date_time = request.form["date_time"] if request.form["date_time"] !="" else row[8]
        result = covid_test.update(row_id, location_id, total_tests, new_tests, total_tests_per_thousand, new_tests_per_thousand, new_tests_smoothed, positive_rate, date_time)
        if result:
            message = "success"  
        else:
            message = "failed" 
    
    return render_template("tests/update-tests.html", id = row_id, data=row, message=message)