from flask import Flask, render_template, redirect, request, flash, session, abort, url_for
import model
import os
import json
import datetime
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound
import pdb 

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03")
if os.environ.get('DEBUG', False):
    app.config['DEBUG'] = True

#   date function
def format_date():
    # '{dt.year}/{dt.month}/{dt.day}'.format(dt = dt.datetime.now())
    today = datetime.date.today()
    day = datetime.date.today().strftime("%A")
    month = datetime.date.today().strftime("%B")
    date = datetime.date.today().strftime("%d")
    date = str(int(date)) # hack to strip leading zero
    year = datetime.date.today().strftime("%Y")

    return "Daily Route for %s, %s %s, %s" % (day, month, date, year)

#
#   HOME PAGE
#
#   daily route
@app.route('/')
def daily_route():
    page_date = format_date()

    congregate_list = []
    congregate_dict = {}
    
    incline_village_list = []
    incline_village_dict = {}

    kings_beach_list = []
    kings_beach_dict = {}

    tahoe_city_list = []
    tahoe_city_dict = {}

    truckee_list = []
    truckee_dict = {}

    all_routes_list = ["Congregate", "Incline Village", "Kings Beach", "Tahoe City", "Truckee"]

    route_list = model.session.query(model.Route_Details) \
                .join("participant").order_by(model.Route_Details.route).all()
    for delivery in route_list:
        alert_list = []
        no_list = []
        yes_list = []    
        part_pref_list = model.session.query(model.Participant_Preferences) \
        .filter(model.Participant_Preferences.participant_id == delivery.participant.id) \
        .all()
        # pdb.set_trace()
        for pref in part_pref_list:
            if pref.pref_type == "alert":
                alert_list.append(pref.pref_description)
            elif pref.pref_type == "no":
                no_list.append(pref.pref_description)
            elif pref.pref_type == "yes":
                yes_list.append(pref.pref_description)
        part_dict = {
            'id': delivery.participant.id,
            'name': delivery.participant.full_name,
            'addr1': delivery.participant.delivery_addr_line1,
            'addr2': delivery.participant.delivery_addr_line2,
            'city': delivery.participant.delivery_city,
            'notes': delivery.participant.delivery_notes,
            'delivery_id': delivery.id,
            'regular': delivery.regular,
            'frozen': delivery.frozen,
            'breakfast': delivery.breakfast,
            'milk': delivery.milk,
            'salad': delivery.salad,
            'fruit': delivery.fruit,
            'bread': delivery.bread,
            'alerts': sorted(alert_list),
            'noes': sorted(no_list),
            'yeses': sorted(yes_list)
        }
        if delivery.route == "Congregate":
            congregate_list.append(delivery.participant.full_name)
            congregate_dict[delivery.participant.full_name] = part_dict
        elif delivery.route == "Incline Village":
            incline_village_list.append(delivery.participant.full_name)
            incline_village_dict[delivery.participant.full_name] = part_dict
        elif delivery.route == "Kings Beach":
            kings_beach_list.append(delivery.participant.full_name)
            kings_beach_dict[delivery.participant.full_name] = part_dict
        elif delivery.route == "Tahoe City":
            tahoe_city_list.append(delivery.participant.full_name)
            tahoe_city_dict[delivery.participant.full_name] = part_dict
        elif delivery.route == "Truckee":
            truckee_list.append(delivery.participant.full_name)
            truckee_dict[delivery.participant.full_name] = part_dict

    congregate_list.sort()
    incline_village_list.sort()
    kings_beach_list.sort()
    tahoe_city_list.sort()
    truckee_list.sort()

    html = render_template("index.html", page_date = page_date, \
        all_routes_list = all_routes_list, \
        congregate_list = congregate_list, congregate_dict = congregate_dict, \
        incline_village_list = incline_village_list, incline_village_dict = incline_village_dict, \
        kings_beach_list = kings_beach_list, kings_beach_dict = kings_beach_dict,
        tahoe_city_list = tahoe_city_list, tahoe_city_dict = tahoe_city_dict,
        truckee_list = truckee_list, truckee_dict = truckee_dict)
    return html

#   edit meal quantity
@app.route('/change_meals/<int:delivery_id>', methods=["POST"])
def change_meals(delivery_id):
    route_detail = model.session.query(model.Route_Details).get(delivery_id)

    route_detail.regular = int(request.form.get('regular'))
    route_detail.frozen = int(request.form.get('frozen'))
    route_detail.breakfast = int(request.form.get('breakfast'))
    route_detail.milk = int(request.form.get('milk'))
    route_detail.salad = int(request.form.get('salad'))
    route_detail.fruit = int(request.form.get('fruit'))
    route_detail.bread = int(request.form.get('bread'))

    model.session.commit()
    return "success"

#
#   LOOKUP TABLE CRUD
#
#   preferences
@app.route('/define_preferences', methods=["GET"])
def show_preferences():
    preference_list = model.session.query(model.Preferences).order_by(model.Preferences.description).all()
    return render_template("define_preferences.html", preference_list=preference_list)

@app.route('/add_preference', methods=["POST"])
def get_preference(): 
    form_preference_description = request.form['preference_description']

    new_preference = model.Preferences(
        description = form_preference_description,
        )

    model.session.add(new_preference)
    model.session.commit()
    
    if new_preference == None:
        #send and error
        return json.JSONEncoder().encode({"error": "Unable to set record"})
    else:
        return json.JSONEncoder().encode({
            "id": str(new_preference.id),
            "desc": new_preference.description
            })

@app.route('/delete_preference', methods=["POST"])
def delete_preference():
    form_preference = request.form["preference_id"]
    model.session.query(model.Preferences).filter_by(id=form_preference).delete()
    model.session.commit()
    return "success"

#
#   PARTICIPANT
#

#   main screen - add or change from here
@app.route('/participant')
def show_participants():
    participant_list = model.session.query(model.Participant).order_by(model.Participant.full_name).all()
    return render_template("participant.html", participant_list=participant_list)    

#   add - basic fields then add to database
@app.route('/participant_add', methods=["GET"])
def empty_participant_status():
    html = render_template("participant_add.html")
    return html

@app.route('/participant_add', methods=["POST"])
def new_participant_status():

    participant = model.Participant(
        full_name = request.form.get('full_name'),
        ptype = request.form.get('participant_type'),
        status = request.form.get('status'),
        route = request.form.get('participant_route'),
        Q_ID = request.form.get('Q_ID'),
        general_notes = request.form.get('general_notes'))

    model.session.add(participant)
    model.session.commit()
    return redirect(url_for('show_participant_status', participant_id=participant.id))


#   status - first screen, data each screen handled as an update    
@app.route('/participant/<int:participant_id>/status', methods=["GET"])
def show_participant_status(participant_id):
    participant = model.session.query(model.Participant).get(participant_id)

    if not participant:
        abort(404)

    html = render_template("participant_status.html", participant=participant)
    return html

@app.route('/participant/<int:participant_id>/status', methods=["POST"])
def update_participant_status(participant_id):

    participant = model.session.query(model.Participant).get(participant_id)

    # example error handling
    # if not participant:
    #     abort(404)
    # if form_Q_ID == "12345":
    #     flash("Successfully updated.")

    participant.full_name = request.form.get('full_name')
    participant.type = request.form.get('participant_type')
    participant.status = request.form.get('participant_status')
    participant.route = request.form.get('participant_route')
    participant.Q_ID = request.form.get('Q_ID') # generated by Area4 database system
    participant.general_notes = request.form.get('general_notes')
    model.session.commit()
    return redirect(url_for('show_participant_status', participant_id=participant_id))

#   delivery - handled as an update
@app.route('/participant/<int:participant_id>/delivery', methods=["GET"])
def show_participant_delivery(participant_id):
    # Load participant
    participant = model.session.query(model.Participant).get(participant_id)

    if not participant:
        abort(404)

    html = render_template("participant_delivery.html", participant=participant)
    return html

@app.route('/participant/<int:participant_id>/delivery', methods=["POST"])
def update_participant_delivery(participant_id):

    participant = model.session.query(model.Participant).get(participant_id)

    participant.delivery_addr_line1 = request.form.get('delivery_addr_line1')
    participant.delivery_addr_line2 = request.form.get('delivery_addr_line2')
    participant.delivery_city = request.form.get('delivery_city')
    if request.form.get('delivery_state') == "State":
        participant.delivery_state = ""
    else:
        participant.delivery_state = request.form.get('delivery_state')
    participant.delivery_zipcode = request.form.get('delivery_zipcode')
    if request.form.get('delivery_county') == "County":
        participant.delivery_county = ""
    else:
        participant.delivery_county = request.form.get('delivery_county')
    participant.tel_3 = request.form.get('tel_3')
    participant.delivery_notes = request.form.get('delivery_notes')
    model.session.commit()
    return redirect(url_for('show_participant_delivery', participant_id=participant_id))

#   contact - handled as an update
@app.route('/participant/<int:participant_id>/contact', methods=["GET"])
def show_participant_contact(participant_id):
    participant = model.session.query(model.Participant).get(participant_id)

    if not participant:
        abort(404)

    html = render_template("participant_contact.html", participant=participant)
    return html

@app.route('/participant/<int:participant_id>/contact', methods=["POST"])
def update_participant_contact(participant_id):

    participant = model.session.query(model.Participant).get(participant_id)

    if request.form.get('lang_english') == 'No':
        participant.lang_english = False
    else:
        participant.lang_english = True
    participant.lang_interpreter = request.form.get('lang_interpreter')
    participant.mail_addr_line1 = request.form.get('mail_addr_line1')
    participant.mail_addr_line2 = request.form.get('mail_addr_line2')
    participant.mail_city = request.form.get('mail_city')
    if request.form.get('mail_state') == "State":
        participant.mail_state = ""
    else:
        participant.mail_state = request.form.get('mail_state')
    participant.mail_zipcode = request.form.get('mail_zipcode')
    participant.email_1 = request.form.get('email_1')
    participant.tel_1 = request.form.get('tel_1')
    participant.tel_2 = request.form.get('tel_2')

    model.session.commit()
    return redirect(url_for('show_participant_contact', participant_id=participant_id))

#   vitals - handled as an update
@app.route('/participant/<int:participant_id>/vitals', methods=["GET"])
def show_participant_vitals(participant_id):
    participant = model.session.query(model.Participant).get(participant_id)

    if not participant:
        abort(404)

    html = render_template("participant_vitals.html", participant=participant)
    return html

@app.route('/participant/<int:participant_id>/vitals', methods=["POST"])
def update_participant_vitals(participant_id):            

    participant = model.session.query(model.Participant).get(participant_id)

    participant.SSN_4 = request.form.get('SSN_4')
    formatted_date = request.form.get('birthdate') # 2000-10-31
    if formatted_date:
        year = int(formatted_date[0:4]) # year
        month = int(formatted_date[5:7]) # month
        day = int(formatted_date[8:10]) # day
        participant.birthdate = datetime.date(year, month, day)
    participant.gender = request.form.get('gender')
    participant.martial_status = request.form.get('martial_status')
    participant.living_status = request.form.get('living_status')   
    participant.household = request.form.get('household')
    if request.form.get('female_head') == 'No':
        participant.female_head = False
    else:
        participant.female_head = True
    participant.rent_own = request.form.get('rent_own')
    participant.rural_status = request.form.get('rural_status')    
    if request.form.get('migrant_farm_worker') == 'No':
        participant.migrant_farm_worker = False
    else:
        participant.migrant_farm_worker = True
    participant.poverty_status = request.form.get('poverty_status')   
    participant.income_level = request.form.get('income_level')
    participant.completed_ed = request.form.get('completed_ed')
    participant.race = request.form.get('race')
    participant.ethnicity = request.form.get('ethnicity')
    if request.form.get('disabled') == 'No':
        participant.disabled = False
    else:
        participant.disabled = True
    participant.healthcare = request.form.get('healthcare')

    model.session.commit()
    return redirect(url_for('show_participant_vitals', participant_id=participant_id))

#   preferences, ajax add and delete
@app.route('/participant/<int:participant_id>/preferences', methods=["GET"])
def show_participant_preferences(participant_id):
    participant = model.session.query(model.Participant).get(participant_id)
    part_pref_list = model.session.query(model.Participant_Preferences).filter(model.Participant_Preferences.participant_id == participant.id).order_by(model.Participant_Preferences.pref_description).all()
    def_pref_list = model.session.query(model.Preferences).order_by(model.Preferences.description).all()
    html = render_template("participant_preferences.html", participant=participant, part_pref_list=part_pref_list, def_pref_list=def_pref_list)
    return html

@app.route('/participant/<int:participant_id>/preferences', methods=["POST"])
def new_part_pref(participant_id):
    form_pref_type = request.form.get('pref_type');
    form_preference_description = request.form.get('part_pref')

    participant_preference = model.Participant_Preferences(
        participant_id = participant_id,
        pref_type= form_pref_type,
        pref_description = form_preference_description)

    model.session.add(participant_preference)
    model.session.commit()

    if participant_preference == None:
        #send and error
        return json.JSONEncoder().encode({"error": "Unable to set record"})
    else:
        return json.JSONEncoder().encode({
            "id": str(participant_preference.id)
            })

@app.route('/delete_participant_preferences', methods=["POST"])
def delete_participant_preferences():
    form_part_pref_id = request.form.get('part_pref_id')
    model.session.query(model.Participant_Preferences).filter_by(id=form_part_pref_id).delete()
    model.session.commit()
    return "success"

#   meals, update
@app.route('/participant/<int:participant_id>/meals', methods=["GET"])
def show_participant_meals(participant_id):
    # Load participant
    participant = model.session.query(model.Participant).get(participant_id)
    part_meals_list = model.session.query(model.Participant_Meals).filter(model.Participant_Meals.participant_id == participant.id)

    part_meals_dict = {
            'regular':   {'Mon':0,'Tue':0,'Wed':0,'Thu':0,'Fri':0},
            'frozen':    {'Mon':0,'Tue':0,'Wed':0,'Thu':0,'Fri':0},
            'breakfast': {'Mon':0,'Tue':0,'Wed':0,'Thu':0,'Fri':0},
            'milk':      {'Mon':0,'Tue':0,'Wed':0,'Thu':0,'Fri':0},
            'salad':     {'Mon':0,'Tue':0,'Wed':0,'Thu':0,'Fri':0},
            'fruit':     {'Mon':0,'Tue':0,'Wed':0,'Thu':0,'Fri':0},
            'bread':     {'Mon':0,'Tue':0,'Wed':0,'Thu':0,'Fri':0},
        }

    if part_meals_list:
        for meal in part_meals_list:
            part_meals_dict[meal.meal_type][meal.delivery_day] = int(meal.qty)

    if not participant:
        abort(404)

    html = render_template("participant_meals.html", participant=participant, part_meals_dict=part_meals_dict)
    return html

@app.route('/participant/<int:participant_id>/meals', methods=["POST"])
def update_participant_meals(participant_id):
    # meal_list = request.json
    meal_list = request.get_json(force=True)
    for meal in meal_list:
        try:
            existing_part_meal = model.session.query(model.Participant_Meals) \
                .filter(model.Participant_Meals.participant_id == participant_id) \
                .filter(model.Participant_Meals.delivery_day == meal['day']) \
                .filter(model.Participant_Meals.meal_type == meal['meal']) \
                .one()
        except MultipleResultsFound, e:
            print e
        # Deal with it
        except NoResultFound, e:
            print e
            part_meal = model.Participant_Meals(
                participant_id = participant_id,
                delivery_day = meal['day'],
                meal_type = meal['meal'],
                qty = meal['qty'])
            model.session.add(part_meal)
        else:
            existing_part_meal.qty = meal['qty']

    model.session.commit()

    # if meal_list == None:
    #     #send and error
    #     return json.JSONEncoder().encode({"error": "Unable to set record"})
    # else:
    #     return json.JSONEncoder().encode({"response": "success"})
    return "success"

if __name__ == "__main__":
    app.run(debug = True)
