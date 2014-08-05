#routetrout

Route Trout is a web app designed for Meals on Wheels.  It helps track participant preferences, meal exception and meal reporting requirements for non-profits.  It is optimized for mobile.

This app tracks participant demographics data for grant and government reporting.  Meal requests and delivery locations are required.

Index page of app will build daily route when first viewed each day.  Actual meals delivered should be entered on daily route page.

To install:
1. Download project to virtual environment.
2. Install requisite files using pip install -r requirements.txt
3. Seed the database using seed.py.  This app supports both Postgres and sqlite3. 
4. Add participants, set status and route.  Meals and delivery screens should be completed.


Route Trout is currently under development and being reviewing by [Sierra Senior Services] (http://sierraseniors.org/)  Expected features not present in alpha release:
* database validation
* field validation
* RSS style logging
* comprehensive reporting
* Ability to edit route delivery totals after delivery day.
* User authentication
