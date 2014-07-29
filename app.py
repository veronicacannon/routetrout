from flask import Flask, render_template, redirect, request, flash, session, abort, url_for
import model
import os
import json
import datetime

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03")
if os.environ.get('DEBUG', False):
    app.config['DEBUG'] = True

#
#   HOME PAGE
#
#   daily route
@app.route('/')
def daily_route():
    route_list = model.session.query(model.Route_Details).order_by(model.Route_Details.route).all()
    html = render_template("index.html", route_list = route_list)
    return html

#   edit meal quantity
@app.route('/edit_qty', methods=["POST"])
def edit_qty():
    field = request.form["field"]
    field_list = field.split()
    
    participant_id = int(field_list[0])
    participant = model.session.query(model.Participant).get(participant_id)

    meal = field_list[1]
    qty = request.form["qty"]
    participant.regular = qty
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
    form_full_name = request.form['full_name']
    form_participant_type = request.form['participant_type']
    form_status = request.form['status']
    form_participant_route = request.form['participant_route']
    form_Q_ID = request.form['Q_ID']
    form_general_notes = request.form['general_notes']

    participant = model.Participant(
        full_name = form_full_name,
        ptype = form_participant_type,
        status = form_status,
        route = form_participant_route,
        Q_ID = form_Q_ID,
        general_notes = form_general_notes)

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
    form_full_name = request.form['full_name']
    form_participant_type = request.form['participant_type']
    form_participant_status = request.form['participant_status']
    form_participant_route = request.form['participant_route']
    form_Q_ID = request.form['Q_ID']
    form_general_notes = request.form['general_notes']

    participant = model.session.query(model.Participant).get(participant_id)

    if not participant:
        abort(404)
    if form_Q_ID == "12345":
        flash("Successfully updated.")

    participant.full_name = form_full_name
    participant.type = form_participant_type
    participant.status = form_participant_status
    participant.route = form_participant_route
    participant.Q_ID = form_Q_ID
    participant.general_notes = form_general_notes
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
    # form_delivery_addr_line1 = request.form.get('delivery_addr_line1')  # better if form changed
    # per nicka, no need to repeat 
    form_delivery_addr_line1 = request.form['delivery_addr_line1']
    form_delivery_addr_line2 = request.form['delivery_addr_line2']
    form_delivery_city = request.form['delivery_city']
    form_delivery_state = request.form['delivery_state']
    form_delivery_zipcode = request.form['delivery_zipcode']
    form_delivery_county = request.form['delivery_county']
    form_tel_3 = request.form['tel_3']
    form_delivery_notes = request.form['delivery_notes']

    participant = model.session.query(model.Participant).get(participant_id)

    participant.delivery_addr_line1 = form_delivery_addr_line1
    participant.delivery_addr_line2 = form_delivery_addr_line2
    participant.delivery_city = form_delivery_city
    participant.delivery_state = form_delivery_state
    participant.delivery_zipcode = form_delivery_zipcode
    participant.delivery_county = form_delivery_county
    participant.tel_3 = form_tel_3
    participant.delivery_notes = form_delivery_notes
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
    form_lang_english = request.form['lang_english']
    form_lang_interpreter = request.form['lang_interpreter']    
    form_mail_addr_line1 = request.form['mail_addr_line1']
    form_mail_addr_line2 = request.form['mail_addr_line2']
    form_mail_city = request.form['mail_city']
    form_mail_state = request.form['mail_state']
    form_mail_zipcode = request.form['mail_zipcode']
    form_email_1 = request.form['email_1']
    form_tel_1 = request.form['tel_1']
    form_tel_2 = request.form['tel_2']

    participant = model.session.query(model.Participant).get(participant_id)

    if form_lang_english == 'No':
        participant.lang_english = False
    else:
        participant.lang_english = True
    participant.lang_interpreter = form_lang_interpreter
    participant.mail_addr_line1 = form_mail_addr_line1
    participant.mail_addr_line2 = form_mail_addr_line2
    participant.mail_city = form_mail_city
    participant.mail_state = form_mail_state
    participant.mail_zipcode = form_mail_zipcode
    participant.email_1 = form_email_1
    participant.tel_1 = form_tel_1
    participant.tel_2 = form_tel_2

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
    form_SSN_4 = request.form['SSN_4']
    formatted_date = request.form['birthdate'] # 2000-10-31
    form_gender = request.form.get('gender')
    form_martial_status = request.form.get('martial_status')
    form_living_status = request.form['living_status']        
    form_household = request.form['household']
    form_female_head = request.form['female_head']
    form_rent_own = request.form['rent_own']
    form_rural_status = request.form['rural_status'] 
    form_migrant_farm_worker = request.form['migrant_farm_worker']
    form_income_level = request.form['income_level']
    form_poverty_status = request.form['poverty_status']     
    form_completed_ed = request.form['completed_ed']
    form_race = request.form['race']
    form_ethnicity = request.form['ethnicity']
    form_disabled = request.form['disabled']
    form_healthcare = request.form['healthcare']                

    participant = model.session.query(model.Participant).get(participant_id)

    participant.SSN_4 = form_SSN_4
    year = int(formatted_date[0:4]) # year
    month = int(formatted_date[5:7]) # month
    day = int(formatted_date[8:10]) # day
    participant.birthdate = datetime.date(year, month, day)
    participant.gender = form_gender
    participant.martial_status = form_martial_status
    participant.living_status = form_living_status    
    participant.household = form_household
    if form_female_head == 'No':
        participant.female_head = False
    else:
        participant.female_head = True
    participant.rent_own = form_rent_own
    participant.rural_status = form_rural_status    
    if form_migrant_farm_worker == 'No':
        participant.migrant_farm_worker = False
    else:
        participant.migrant_farm_worker = True
    participant.poverty_status = form_poverty_status    
    participant.income_level = form_income_level
    participant.completed_ed = form_completed_ed
    participant.race = form_race
    participant.ethnicity = form_ethnicity
    if form_disabled == 'No':
        participant.disabled = False
    else:
        participant.disabled = True
    participant.healthcare = form_healthcare

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
    # part_meals_list = model.session.query(model.Participant_Meals).filter(model.Participant_Meals.participant_id == participant.id).order_by(model.sqlalchemy.sql.expression.case(((model.Participant_Meals.delivery_day == "Mon", 1),
    #     (model.Participant_Meals.delivery_day == "Tue", 2),
    #     (model.Participant_Meals.delivery_day == "Wed", 3),
    #     (model.Participant_Meals.delivery_day == "Thu", 4),
    #     (model.Participant_Meals.delivery_day == "Fri", 5))))
    part_meals_dict = {
        'regular': [1,1,1,1,1],
        'frozen': [0,0,0,0,0],
        'breakfast': [0,0,0,0,0],
        'milk': [1,1,1,1,3],
        'salad': [0,0,0,0,0],
        'fruit': [0,0,0,0,0],
        'bread': [0,0,0,0,0]
    }

    if not participant:
        abort(404)

    html = render_template("participant_meals.html", participant=participant, part_meals_dict=part_meals_dict)
    return html

@app.route('/participant/<int:participant_id>/meals', methods=["POST"])
def update_participant_meals(participant_id):
    # form_delivery_addr_line1 = request.form.get('delivery_addr_line1')  # better if form changed

    # ***** consider having form send back a list, dict? and loop through that to write records


    # participant = model.session.query(model.Participant).get(participant_id)

    # participant.delivery_addr_line1 = form_delivery_addr_line1

    # model.session.commit()
    return redirect(url_for('show_participant_meals', participant_id=participant_id))

if __name__ == "__main__":
    app.run(debug = True)
