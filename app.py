from flask import Flask, render_template, redirect, request, flash, session, abort, url_for
import model
import os
import json

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
@app.route('/define_health_alert', methods=["GET"])
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
@app.route('/participant')
def show_participants():
    participant_list = model.session.query(model.Participant).order_by(model.Participant.full_name).all()
    return render_template("participant.html", participant_list=participant_list)
    
@app.route('/participant/<int:participant_id>/status', methods=["GET"])
def show_participant_status(participant_id):
    # Load participant
    participant = model.session.query(model.Participant).get(participant_id)

    if not participant:
        abort(404)

    html = render_template("participant_status.html", participant=participant)
    return html

@app.route('/participant/<int:participant_id>/status', methods=["POST"])
def update_participant_status(participant_id):
    form_full_name = request.form['full_name']
    form_status = request.form['status']
    form_route = request.form['participant_route']
    form_Q_ID = request.form['Q_ID']
    form_general_notes = request.form['general_notes']

    participant = model.session.query(model.Participant).get(participant_id)

    if not participant:
        abort(404)
    if form_Q_ID == "12345":
        flash("Successfully updated.")

    participant.full_name = form_full_name
    participant.status = form_status
    participant.route = form_route
    participant.Q_ID = form_Q_ID
    participant.general_notes = form_general_notes
    model.session.commit()

    return redirect(url_for('show_participant_status', participant_id=participant.id))

@app.route('/participant_delivery')
def participant_delivery():
    html = render_template("participant_delivery.html")
    return html

@app.route('/participant_contact')
def participant_contact():
    # form_lang_english = "Yes" then participant.lang_english = True
    html = render_template("participant_contact.html")
    return html

@app.route('/participant_health_alerts')
def health_alerts():
    html = render_template("participant_health_alerts.html")
    return html

if __name__ == "__main__":
    app.run(debug = True)