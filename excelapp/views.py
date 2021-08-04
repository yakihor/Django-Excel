from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
import os
from django.shortcuts import redirect
from pathlib import Path
import pandas as pd


# path = os.
BASE_DIR = Path(__file__).resolve().parent.parent
APP_PATH = os.path.join(BASE_DIR, 'excelapp')
JSON_PATH = os.path.join(APP_PATH, 'location.json')
XLS_PATH = os.path.join(APP_PATH, 'output.xls')

def home(request):
  # Opening JSON file
  f = open(JSON_PATH,)
    
  # returns JSON object as 
  # a dictionary
  data = json.load(f)
  # Closing file
  f.close()
  return render(request, "main.html", {"locations": data})

def edit(request):
  # Opening JSON file
  f = open(JSON_PATH,)
    
  # returns JSON object as 
  # a dictionary
  data = json.load(f)
  # Closing file
  f.close()
  return render(request, "edit.html", {"locations": data})

# API to add JSON data
def add(request):
  if request.method == 'POST':
    # Opening JSON file
    location = request.POST.get("location")
    category = request.POST.get("category")
    col = str(location)[-3:-2]
    with open(JSON_PATH) as fin:
      obj = json.load(fin)
    obj[int(col)-1][str(location)] = str(category)
    obj[int(col)-1] = dict(sorted(obj[int(col)-1].items(), key = lambda x:x[0]))
    with open(JSON_PATH, "w") as fout:
      json.dump(obj, fout, indent="  ")
    return redirect("edit", )

# API to remove JSON data
def remove(request):
  if request.method == 'POST':
    # Opening JSON file
    locations = request.POST.getlist("location")
    with open(JSON_PATH) as fin:
      obj = json.load(fin)
      for location in locations:
        col = str(location)[-3:-2]
        del obj[int(col)-1][str(location)]
        obj[int(col)-1] = dict(sorted(obj[int(col)-1].items(), key = lambda x:x[0]))
    with open(JSON_PATH, "w") as fout:
      json.dump(obj, fout, indent="  ")
    return redirect("edit",)

# API to print JSON data to excel sheet
def out_as_xml(request):
  if request.method == 'POST':
    # Opening JSON file
    catx = request.POST.get("chk_x")
    caty = request.POST.get("chk_y")
    catz = request.POST.get("chk_z")
    with open(JSON_PATH) as fin:
      obj = json.load(fin)
    json_text = []
    json_x = []
    json_y = []
    json_z = []
    for locations in obj:
      for item in locations:
        if catx:
          if str(locations[item]) == "X":
            json_x.append({"X": str(item)})
        if caty:
          if str(locations[item]) == "Y":
            json_y.append({"Y": str(item)})
        if catz:
          if str(locations[item]) == "Z":
            json_z.append({"Z": str(item)})
    counts = len(json_x)
    if counts <= len(json_y):
      counts = len(json_y)
    if counts <= len(json_z):
      counts = len(json_z)
    for i in range(counts):
      tmp_json = {}
      if i+1 <= len(json_x):
        tmp_json.update(json_x[i])
      if i+1 <= len(json_y):
        tmp_json.update(json_y[i])
      if i+1 <= len(json_z):
        tmp_json.update(json_z[i])
      json_text.append(tmp_json)
    df = pd.DataFrame(json_text)
    df.to_excel(XLS_PATH, index=False)
    return redirect("home",)