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

def load_preferences(): 
    new_pref = model.Preferences(
        description = "allergy nuts",
        )
    model.session.add(new_pref)

    new_pref = model.Preferences(
        description = "diabetic",
        )
    model.session.add(new_pref)
        
    new_pref = model.Preferences(
        description = "milk",
        )
    model.session.add(new_pref)   
    model.session.commit()

def load_part_meals():
    new_part_meals1r = model.Participant_Meals(
        participant_id = 1,
        delivery_day = "Mon",
        meal_type = "regular",
        qty = 1)
    model.session.add(new_part_meals1r)

    new_part_meals1fz = model.Participant_Meals(
        participant_id = 1,
        delivery_day = "Mon",
        meal_type = "frozen",
        qty = 0)
    model.session.add(new_part_meals1fz)

    new_part_meals1bk = model.Participant_Meals(
        participant_id = 1,
        delivery_day = "Mon",
        meal_type = "breakfast",
        qty = 0)
    model.session.add(new_part_meals1bk)

    new_part_meals1m = model.Participant_Meals(
        participant_id = 1,
        delivery_day = "Mon",
        meal_type = "milk",
        qty = 0)
    model.session.add(new_part_meals1m)

    new_part_meals1s = model.Participant_Meals(
        participant_id = 1,
        delivery_day = "Mon",
        meal_type = "salad",
        qty = 0)
    model.session.add(new_part_meals1s)

    new_part_meals1f = model.Participant_Meals(
        participant_id = 1,
        delivery_day = "Mon",
        meal_type = "fruit",
        qty = 0)
    model.session.add(new_part_meals1f)

    new_part_meals1b = model.Participant_Meals(
        participant_id = 1,
        delivery_day = "Mon",
        meal_type = "bread",
        qty = 0)
    model.session.add(new_part_meals1b)
    model.session.commit()

def load_route_details():
    new_route_detail = model.Route_Details(
        route_date = datetime.date(2014, 8, 6),
        route = "Kings Beach",
        participant_id = 1,
        meal_type = "regular",
        qty = 1)
    model.session.add(new_route_detail)

    new_route_detail1 = model.Route_Details(
        route_date = datetime.date(2014, 8, 6),
        route = "Kings Beach",
        participant_id = 1,
        meal_type = "frozen",
        qty = 1)
    model.session.add(new_route_detail1)

    new_route_detail2 = model.Route_Details(
        route_date = datetime.date(2014, 8, 6),
        route = "Kings Beach",
        participant_id = 1,
        meal_type = "breakfast",
        qty = 0)
    model.session.add(new_route_detail2)

    new_route_detail3 = model.Route_Details(
        route_date = datetime.date(2014, 8, 6),
        route = "Kings Beach",
        participant_id = 1,
        meal_type = "milk",
        qty = 1)
    model.session.add(new_route_detail3)

    new_route_detail4 = model.Route_Details(
        route_date = datetime.date(2014, 8, 6),
        route = "Kings Beach",
        participant_id = 1,
        meal_type = "salad",
        qty = 0)
    model.session.add(new_route_detail4)

    new_route_detail5 = model.Route_Details(
        route_date = datetime.date(2014, 8, 6),
        route = "Kings Beach",
        participant_id = 1,
        meal_type = "fruit",
        qty = 1)
    model.session.add(new_route_detail5)

    new_route_detail6 = model.Route_Details(
        route_date = datetime.date(2014, 8, 6),
        route = "Kings Beach",
        participant_id = 1,
        meal_type = "bread",
        qty = 0)
    model.session.add(new_route_detail6)

    model.session.commit()

def main():
    model.create_db()
    load_participants()
    load_preferences()
    load_route_details()
    load_part_meals()

if __name__ == "__main__":
    main()