import model
import datetime

def load_participants():
    new_participant = model.Participant(
        full_name = "Sue Ellen Jones",
        ptype = "Senior",
        status = "Active")
    model.session.add(new_participant)

    new_participant1 = model.Participant(
        full_name = "Robert (Bob) Walker",
        ptype = "Senior",
        status = "Active")
    model.session.add(new_participant1)

    new_participant2 = model.Participant(
        full_name = "Lola Rodriquez",
        ptype = "Senior",
        status = "Active")
    model.session.add(new_participant2)
    model.session.commit()

def load_health_alert(): 
    new_health_alert = model.Health_Alert(
        description = "allergy nuts",
        status = "active"
        )
    model.session.add(new_health_alert)

    new_health_alert = model.Health_Alert(
        description = "diabetic",
        status = "active"
        )
    model.session.add(new_health_alert)
        
    new_health_alert = model.Health_Alert(
        description = "extra milk",
        status = "active"
        )
    model.session.add(new_health_alert)   
    model.session.commit()

def load_route_details():
    new_route_detail = model.Route_Details(
        route = "Kings Beach",
        route_date = datetime.date(2014, 8, 6),
        participant_id = 1,
        regular = 1,
        frozen = 1,
        breakfast = 0,
        milk = 1,
        salad = 0,
        fruit = 0,
        bread = 0)
    model.session.add(new_route_detail)

    new_route_detail1 = model.Route_Details(
        route = "Kings Beach",
        route_date = datetime.date(2014, 8, 6),
        participant_id = 2,
        regular = 0,
        frozen = 2,
        breakfast = 0,
        milk = 1,
        salad = 0,
        fruit = 0,
        bread = 0)
    model.session.add(new_route_detail1)

    new_route_detail2 = model.Route_Details(
        route = "Kings Beach",
        route_date = datetime.date(2014, 8, 6),
        participant_id = 3,
        regular = 1,
        frozen = 1,
        breakfast = 0,
        milk = 1,
        salad = 0,
        fruit = 0,
        bread = 0)
    model.session.add(new_route_detail2)
    model.session.commit()

def main():
    load_participants()
    load_health_alert()
    load_route_details()

if __name__ == "__main__":
    main()