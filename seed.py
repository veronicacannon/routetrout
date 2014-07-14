import model

def load_participants():
    new_participant = model.Participant(
        full_name = "Babette Greystone",
        status = "active"
        )

    model.session.add(new_participant)
    model.session.commit()

def load_health_alert(): 
    new_health_alert = model.Health_Alert(
        description = "allergy nuts",
        status = "active"
        )

    model.session.add(new_health_alert)
    model.session.commit()

def main():
    load_participants()
    load_health_alert()

if __name__ == "__main__":
    main()