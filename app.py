from flask import Flask, render_template, redirect, request, flash, session as b_session
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
    
@app.route('/participant_status')
def participant_status():
    html = render_template("participant_status.html")
    return html

@app.route('/participant_contact')
def participant_status():
    html = render_template("participant_contact.html")
    return html

@app.route('/health')
def health_alerts():
    html = render_template("health_alerts.html")
    return html


#
#


if __name__ == "__main__":
    app.run(debug = True)