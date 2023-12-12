from flask import Flask , render_template , redirect, url_for, request, session, flash
from application import app
from application import db

from flask_pymongo import ObjectId

from bson import ObjectId


@app.route("/") 
def home():
    lists = []
    for list_name in db.display_list.find({}):
        lists.append(list_name)
    return render_template("homepage.html", lists=lists)

@app.route("/add_item",methods=["GET", "POST"])
def add_item():
    if request.method == "POST":

        if "lst" in session:
            list_name = session["lst"]
            list_required = db.display_list.find_one({"list_name": list_name})
            list_required_id = ObjectId(str(list_required["_id"]))


            item_name = request.form["in"]
            quantity = request.form["q"]
            kgs = request.form["k"]

            if kgs == "":
                kgs = "-"
        
            list_to_insert = {"item_name": item_name,
                                "quantity": quantity,
                                "kgs": kgs}
        
            
            list_exists = db.display_single_list.find_one({"key" : str(list_required_id)})
            if list_exists:

                db.display_single_list.update_one(
                    {"key": str(list_required_id)},
                    {"$push": {"items": list_to_insert}}
                )
            else: 
                db.display_single_list.insert_one(
                    {"key": str(list_required_id)}
                )
                db.display_single_list.update_one(
                    {"key": str(list_required_id)},
                    {"$push": {"items": list_to_insert}}
                )
            flash("Item has been added to the list","success")
            return render_template("add_item.html")
        
    else:
        return render_template("add_item.html")

@app.route("/add_list",methods=["GET", "POST"])
def add_list(): 
    if request.method == "POST":
        list_name = request.form["ln"]
        list_name_exists = db.display_list.find_one({"list_name": list_name})

        if list_name_exists:
            flash("List name already exists!","error")
            return render_template("add_list.html")
        
        session["lst"] = list_name
        db.display_list.insert_one({"list_name": list_name})

        flash("List has been created","success")
        return redirect(url_for("display_full_list"))

    else:
        return render_template("add_list.html")
    
@app.route("/display_full_list",methods=["GET", "POST"])
def display_full_list(): 
    selected_list = []
    if request.method == "POST":
        list_name = request.form["in"]
        session["lst"] = list_name
    else: 
        list_name = session["lst"]

    list_required = db.display_list.find_one({"list_name": list_name})

    list_required_id = ObjectId(str(list_required["_id"]))
    selected_list = db.display_single_list.find_one({"key": str(list_required_id)})

    if selected_list is None or "items" not in selected_list :
        selected_list= [] 
    else:
        selected_list = selected_list["items"]

    return render_template("display_full_list.html", selected_list= selected_list, list_name = list_name)

   
@app.route("/delete",methods=["GET", "POST"])
def delete_list():
    if request.method == "POST":
        name = request.form["ln"]
        list_to_delete = db.display_list.find_one({"list_name": name})
        
        if list_to_delete:
            db.display_list.delete_one({"_id": list_to_delete["_id"]})

            db.display_single_list.delete_one({"key":str(list_to_delete["_id"])}) # 
            flash(f"{name} has been deleted", "success")

    
    return redirect(url_for("home"))
    
@app.route("/delete_item",methods = ["POST","GET"])
def delete_item():
    if request.method == "POST":
        index_number = int(request.form["li"])
        list_name = session["lst"]
        list_to_delete_from = db.display_list.find_one({"list_name": list_name})
        
        if list_to_delete_from:
            list_required = db.display_single_list.find_one({"key": str(list_to_delete_from["_id"])})
            i = 0
            list_modified = []
            for item in list_required["items"]:
                if i != index_number-1:
                    list_modified.append(item)
                
                i += 1  
   
            db.display_single_list.update_one(
                {"key": str(list_to_delete_from["_id"])},
                {"$set": {"items": list_modified}}
            )


        flash(f"Item - {index_number} has been deleted", "success")
    
    return redirect(url_for("display_full_list"))

@app.route("/update_item/<index_number>", methods = ["POST", "GET"])
def update_item(index_number):
    item_to_edit = []
    list_name = session["lst"]
    list_to_update_from = db.display_list.find_one({"list_name": list_name})
    
    if list_to_update_from:
        list_required = db.display_single_list.find_one({"key": str(list_to_update_from["_id"])})
        print(list_required)

        item_to_edit = list_required["items"][int(index_number)-1]

    if request.method == "GET":
        
        return render_template("update_item.html", item_to_edit = item_to_edit, index_number = index_number)
    else:
        quantity = request.form["q"]
        kgs = request.form["k"]

        if kgs == "":
            kgs = "-"

        item_to_edit["quantity"] = quantity
        item_to_edit["kgs"] = kgs

        

        db.display_single_list.update_one(
                {"key": str(list_to_update_from["_id"])},
                {"$set": {"items": list_required["items"]}}
            )
        flash("item has been updated", "success")

        return redirect(url_for("display_full_list"))