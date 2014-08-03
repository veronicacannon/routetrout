import model
import datetime

def load_participants():
    new_participant = model.Participant(
        full_name = "Sue Ellen Jones",
        ptype = "Senior",
        status = "Active",
        route = "Kings Beach",
        Q_ID = "Q1111",
        delivery_addr_line1 = "14043 Lakeshore Blvd.",
        delivery_addr_line2 = "Apt 2A",
        delivery_city = "Kings Beach",
        delivery_state = "CA",
        delivery_zipcode = "96143",
        delivery_county = "Placer",
        delivery_notes = "Watch that the dog doesn't get out.")
    model.session.add(new_participant)

    new_participant1 = model.Participant(
        full_name = "Robert (Bob) Walker",
        ptype = "Senior",
        status = "Active",
        route = "Kings Beach",
        Q_ID = "Q2222",
        delivery_addr_line1 = "653 Pine Cone Lane",
        delivery_addr_line2 = "",
        delivery_city = "Kings Beach",
        delivery_state = "CA",
        delivery_zipcode = "96143",
        delivery_county = "Placer",
        delivery_notes = "Knock loudly.")
    model.session.add(new_participant1)

    new_participant2 = model.Participant(
        full_name = "Lola Rodriquez",
        ptype = "Senior",
        status = "Active",
        route = "Kings Beach",
        Q_ID = "Q3333",
        delivery_addr_line1 = "704 Dolly Varden",
        delivery_addr_line2 = "Second Apartment",
        delivery_city = "Kings Beach",
        delivery_state = "CA",
        delivery_zipcode = "96143",
        delivery_county = "Placer",
        delivery_notes = "Go to screen door.")
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

    new_pref = model.Preferences(
        description = "gluten free",
        )
    model.session.add(new_pref)

    new_pref = model.Preferences(
        description = "fish",
        )
    model.session.add(new_pref)

    new_pref = model.Preferences(
        description = "salmon",
        )
    model.session.add(new_pref) 
    model.session.commit()

def load_part_meals():
    new_part_meals_1Monr = model.Participant_Meals(
        participant_id = 1,
        delivery_day = "Mon",
        meal_type = "regular",
        qty = 1)
    model.session.add(new_part_meals_1Monr)

    new_part_meals1Tuer = model.Participant_Meals(
        participant_id = 1,
        delivery_day = "Tue",
        meal_type = "regular",
        qty = 1)
    model.session.add(new_part_meals1Tuer)

    new_part_meals_1Wedr = model.Participant_Meals(
        participant_id = 1,
        delivery_day = "Wed",
        meal_type = "regular",
        qty = 1)
    model.session.add(new_part_meals_1Wedr)

    new_part_meals_1Thur = model.Participant_Meals(
        participant_id = 1,
        delivery_day = "Thu",
        meal_type = "regular",
        qty = 1)
    model.session.add(new_part_meals_1Thur)

    new_part_meals_1Frir = model.Participant_Meals(
        participant_id = 1,
        delivery_day = "Fri",
        meal_type = "regular",
        qty = 1)
    model.session.add(new_part_meals_1Frir)

    new_part_meals_2Monr = model.Participant_Meals(
        participant_id = 2,
        delivery_day = "Mon",
        meal_type = "regular",
        qty = 1)
    model.session.add(new_part_meals_2Monr)

    new_part_meals_2Tuer = model.Participant_Meals(
        participant_id = 2,
        delivery_day = "Tue",
        meal_type = "regular",
        qty = 1)
    model.session.add(new_part_meals_2Tuer)

    new_part_meals_2Wedr = model.Participant_Meals(
        participant_id = 2,
        delivery_day = "Wed",
        meal_type = "regular",
        qty = 1)
    model.session.add(new_part_meals_2Wedr)

    new_part_meals_2Wedf = model.Participant_Meals(
        participant_id = 2,
        delivery_day = "Wed",
        meal_type = "frozen",
        qty = 1)
    model.session.add(new_part_meals_2Wedf)

    new_part_meals_2Thur = model.Participant_Meals(
        participant_id = 2,
        delivery_day = "Thu",
        meal_type = "regular",
        qty = 0)
    model.session.add(new_part_meals_2Thur)

    new_part_meals_2Frir = model.Participant_Meals(
        participant_id = 2,
        delivery_day = "Fri",
        meal_type = "regular",
        qty = 1)
    model.session.add(new_part_meals_2Frir)

    new_part_meals_3Monr = model.Participant_Meals(
        participant_id = 3,
        delivery_day = "Mon",
        meal_type = "regular",
        qty = 1)
    model.session.add(new_part_meals_3Monr)

    new_part_meals_3Monm = model.Participant_Meals(
        participant_id = 3,
        delivery_day = "Mon",
        meal_type = "milk",
        qty = 1)
    model.session.add(new_part_meals_3Monm)

    new_part_meals_3Tuer = model.Participant_Meals(
        participant_id = 3,
        delivery_day = "Tue",
        meal_type = "regular",
        qty = 1)
    model.session.add(new_part_meals_3Tuer)

    new_part_meals_3Tuem = model.Participant_Meals(
        participant_id = 3,
        delivery_day = "Tue",
        meal_type = "milk",
        qty = 1)
    model.session.add(new_part_meals_3Tuem)

    new_part_meals_3Wedr = model.Participant_Meals(
        participant_id = 3,
        delivery_day = "Wed",
        meal_type = "regular",
        qty = 1)
    model.session.add(new_part_meals_3Wedr)

    new_part_meals_3Wedm = model.Participant_Meals(
        participant_id = 3,
        delivery_day = "Wed",
        meal_type = "milk",
        qty = 1)
    model.session.add(new_part_meals_3Wedm)

    new_part_meals_3Thur = model.Participant_Meals(
        participant_id = 3,
        delivery_day = "Thu",
        meal_type = "regular",
        qty = 1)
    model.session.add(new_part_meals_3Thur)

    new_part_meals_3Thum = model.Participant_Meals(
        participant_id = 3,
        delivery_day = "Thu",
        meal_type = "milk",
        qty = 1)
    model.session.add(new_part_meals_3Thum)

    new_part_meals_3Frir = model.Participant_Meals(
        participant_id = 3,
        delivery_day = "Fri",
        meal_type = "regular",
        qty = 1)
    model.session.add(new_part_meals_3Frir)

    new_part_meals_3Frim = model.Participant_Meals(
        participant_id = 3,
        delivery_day = "Fri",
        meal_type = "milk",
        qty = 1)
    model.session.add(new_part_meals_3Frim)
    model.session.commit()

def load_route_details():
    new_route_detail1 = model.Route_Details(
        route_date = datetime.date(2014, 8, 6),
        route = "Kings Beach",
        participant_id = 1,
        regular = 1,
        frozen = 0,
        breakfast = 0,
        milk = 0,
        salad = 0,
        fruit = 0,
        bread = 0)
    model.session.add(new_route_detail1)

    new_route_detail2 = model.Route_Details(
        route_date = datetime.date(2014, 8, 6),
        route = "Kings Beach",
        participant_id = 2,
        regular = 1,
        frozen = 1,
        breakfast = 0,
        milk = 0,
        salad = 0,
        fruit = 0,
        bread = 0)
    model.session.add(new_route_detail2)

    new_route_detail13 = model.Route_Details(
        route_date = datetime.date(2014, 8, 6),
        route = "Kings Beach",
        participant_id = 3,
        regular = 1,
        frozen = 0,
        breakfast = 0,
        milk = 1,
        salad = 0,
        fruit = 0,
        bread = 0)
    model.session.add(new_route_detail13)
    model.session.commit()

def main():
    model.create_db()
    load_participants()
    load_preferences()
    load_route_details()
    load_part_meals()

if __name__ == "__main__":
    main()