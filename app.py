from flask import Flask, render_template, redirect, request, flash, session, abort, url_for
import model
import os
import json
import datetime

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03")

@app.route('/')
def daily_route():
    html = render_template("accordian.html")
    return html

#
#   LOOKUP TABLE CRUD
#
#   health alerts
@app.route('/define_health_alerts', methods=["GET"])
def show_health_alerts():
    health_alert_list = model.session.query(model.Health_Alert).order_by(model.Health_Alert.description).all()
    return render_template("define_health_alerts.html", health_alert_list=health_alert_list)

@app.route('/add_health_alert', methods=["POST"])
def get_health_alert(): 
    form_health_alert_description = request.form['health_alert_description']

    new_health_alert = model.Health_Alert(
        description = form_health_alert_description,
        status = "active"
        )

    model.session.add(new_health_alert)
    model.session.commit()
    
    if new_health_alert == None:
        #send and error
        return json.JSONEncoder().encode({"error": "Unable to set record"})
    else:
        return json.JSONEncoder().encode({
            "id": str(new_health_alert.id),
            "desc": new_health_alert.description
            })

@app.route('/delete_health_alert', methods=["POST"])
def delete_health_alert():
    form_health_alert = request.form["health_alert_id"]
    model.session.query(model.Health_Alert).filter_by(id=form_health_alert).delete()
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
    form_gender = request.form['gender']
    form_martial_status = request.form['martial_status']
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

@app.route('/participant_health_alerts')
def health_alerts():
    html = render_template("participant_health_alerts.html")
    return html

if __name__ == "__main__":
    app.run(debug = True)