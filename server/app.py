from flask import jsonify, request
from models import User, Record
from setup import app, db, bcrypt
from datetime import date, datetime, timedelta
from sqlalchemy import extract
import json
from dateutil import parser
from flask_login import login_user, current_user, logout_user, login_required

# Permissions for GET, 3 levels Admin, User and Manager
# User must be able to Add, Edit and Delete MEALS
# Date, Time, Text and Num of Calories
# Filter from dates and time from
# Expected Number of Calories Per day  _> Green or Red status for the day
# REST API

# Table 1: ID, Date, Time, Text and Num of Calories and User ID (fk) (User)
# Table 2: User ID (pk), Name, Email, Password, Role ID (Manager or Admin)

@app.route('/add-user', methods=['PUT'])
def add_user():
    response_object = {'status': 'success'}
    post_data = request.get_json()
    # print("User data", post_data)
    if request.method == 'PUT':
        user = User.query.filter(User.email == post_data['email']).\
            update({'expected_calories': post_data['expected_calories'],
                    'name': post_data["name"],
                    'role_id': post_data["role_id"],
                    'email': post_data["email"]})
        response_object['message'] = 'User edited!'
    db.session.commit()
    return jsonify(response_object)

@app.route('/delete-user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    response_object = {'status': 'success'}
    user = User.query.filter(User.id == int(user_id)).delete()
    response_object['message'] = 'User deleted!'
    db.session.commit()
    return jsonify(response_object)

@app.route('/add-meal', methods=['POST', 'PUT'])
def add_meal():
    response_object = {}
    post_data = request.get_json()
    if request.method == 'POST':
        if len(User.query.filter(User.id == post_data["user_id"]).all())==0:
            response_object['status'] = 'failure'
            return jsonify(response_object)
        record = Record(text=post_data.get('text'),
                    num_calories=post_data.get('num_calories'),
                    user_id=post_data.get('user_id'))
        response_object['status'] = 'success'
        response_object['message'] = 'Meal added!'
        db.session.add(record)
    elif request.method == 'PUT':
        user = Record.query.filter(Record.id == post_data['id']).\
            update({'text': post_data['text'], 'num_calories': post_data['num_calories']})
        response_object['status'] = 'success'
        response_object['message'] = 'Meal edited!'

    db.session.commit()
    return jsonify(response_object)

@app.route('/delete-meal/<meal_id>', methods=['DELETE'])
def delete_meal(meal_id):
    response_object = {'status': 'success'}
    user = Record.query.filter(Record.id == int(meal_id)).delete()
    response_object['message'] = 'Meal deleted!'

    db.session.commit()
    return jsonify(response_object)

@app.route('/get-users/<user_id>', methods=['GET'])
@app.route('/get-users/', methods=['GET'])
def get_users(user_id=""):
    response_object = {"users": []}
    users = User.query.all()
    for user in users:
        # user_id is in string, but user.id is integer in database
        if user_id and str(user.id) != user_id:
            continue
        response_object["users"].append({"id": user.id,
                                         "name": user.name,
                                         "email": user.email,
                                         "expected_calories": user.expected_calories,
                                         "role_id": user.role_id})
    # print("Getting info for this user", response_object)
    return jsonify(response_object)

@app.route('/calculate-status/<user_id>', methods=['GET'])
def calculate_status(user_id):
    response_object = {"status": "", "calories_balance": 0}
    users = User.query.filter(User.id == user_id).all()
    resp = get_today_meals(user_id).get_json()
    today_meals = resp["meals"]
    # print("Today Meals", today_meals, users, type(users))
    sum_calories = 0
    if users:
        for meal in today_meals:
            sum_calories += meal["num_calories"]
        calories_left = users[0].expected_calories - sum_calories
        if calories_left >= 0:
            response_object["status"] = "Green"
            response_object["calories_balance"] = calories_left
        else:
            response_object["status"] = "Red"
            response_object["calories_balance"] = calories_left
    # print("Getting status for this user for today", response_object)
    return jsonify(response_object)

@app.route('/get-meals/<user_id>/<meal_id>', methods=['GET'])
@app.route('/get-meals/<user_id>', methods=['GET'])
def get_meals(user_id, meal_id=""):
    response_object = {"meals": []}
    meals = Record.query.filter(Record.user_id == int(user_id)).order_by(Record.datetime).all()
    for meal in meals:
        # meal_id is in string, but meal.id is integer in database
        if meal_id and str(meal.id) != meal_id:
            continue
        user_calories = User.query.filter(User.id == user_id).all()[0].expected_calories
        total_so_far = 0
        for meal in meals:
            if total_so_far + meal.num_calories <= user_calories:
                response_object["meals"].append({"id": meal.id,
                                             "datetime": meal.datetime,
                                             "text": meal.text,
                                             "num_calories": meal.num_calories,
                                             "user_id": meal.user_id,
                                             "status": "within_limit"})
            else:
                response_object["meals"].append({"id": meal.id,
                                             "datetime": meal.datetime,
                                             "text": meal.text,
                                             "num_calories": meal.num_calories,
                                             "user_id": meal.user_id,
                                             "status": "exceeded_limit"})
            total_so_far += meal.num_calories
        return jsonify(response_object)

    return jsonify(response_object)


@app.route('/get-today-meals/<user_id>', methods=['GET'])
def get_today_meals(user_id):
    response_object = {"meals": []}
    # today = date(2018, 11, 1)
    today = datetime.now().date()
    # print(today, type(today))
    # print(today, extract('day', date(2018, 11, 1)))
    # meals = Record.query.filter(extract('day', Record.datetime) == today).all()
    # todays_datetime = datetime(datetime.today().year, datetime.today().month, datetime.today().day)

    meals = Record.query.filter(Record.user_id == int(user_id),
                                extract('year', Record.datetime) == today.year,
                                extract('month', Record.datetime) == today.month,
                                extract('day', Record.datetime) == today.day).order_by(Record.datetime).all()
    # print("TODAY MEALS", meals)
    user_calories = User.query.filter(User.id == user_id).all()[0].expected_calories
    total_so_far = 0
    for meal in meals:
        if total_so_far + meal.num_calories <= user_calories:
            response_object["meals"].append({"id": meal.id,
                                         "datetime": meal.datetime,
                                         "text": meal.text,
                                         "num_calories": meal.num_calories,
                                         "user_id": meal.user_id,
                                         "status": "within_limit"})
        else:
            response_object["meals"].append({"id": meal.id,
                                         "datetime": meal.datetime,
                                         "text": meal.text,
                                         "num_calories": meal.num_calories,
                                         "user_id": meal.user_id,
                                         "status": "exceeded_limit"})
        total_so_far += meal.num_calories
    return jsonify(response_object)

@app.route('/filter-meals/<user_id>/<date_from>/<date_to>/<time_from>/<time_to>', methods=['GET'])
def filter_meals(user_id, date_from, date_to, time_from, time_to):
    response_object = {"meals": []}
    this_user = User.query.filter(User.id == user_id).all()[0]
    # admin = False
    # if this_user.role_id == 3:
    #     admin = True
    def replace_spaces(val):
        return val.replace("%20", " ")

    date_from = replace_spaces(date_from)
    date_to = replace_spaces(date_to)
    time_from = replace_spaces(time_from)
    time_to = replace_spaces(time_to)

    start_datetime = parser.parse(date_from+" "+time_from)
    end_datetime = parser.parse(date_to+" "+time_to)
    # print(today, extract('day', date(2018, 11, 1)))
    # meals = Record.query.filter(extract('day', Record.datetime) == today).all()
    # todays_datetime = datetime(datetime.today().year, datetime.today().month, datetime.today().day)

    meals = Record.query.filter(Record.user_id == int(user_id),
                                Record.datetime >= start_datetime,
                                Record.datetime <= end_datetime).order_by(Record.datetime).all()
    user_calories = this_user.expected_calories
    total_so_far = 0
    for meal in meals:
        if total_so_far + meal.num_calories <= user_calories:
            response_object["meals"].append({"id": meal.id,
                                         "datetime": meal.datetime,
                                         "text": meal.text,
                                         "num_calories": meal.num_calories,
                                         "user_id": meal.user_id,
                                         "status": "within_limit"})
        else:
            response_object["meals"].append({"id": meal.id,
                                         "datetime": meal.datetime,
                                         "text": meal.text,
                                         "num_calories": meal.num_calories,
                                         "user_id": meal.user_id,
                                         "status": "exceeded_limit"})
        total_so_far += meal.num_calories
    return jsonify(response_object)

@app.route('/signup', methods=['POST'])
def signup():
    response_object = {'status': 'success'}
    post_data = request.get_json()
    password = post_data.get("password")
    role_id = post_data.get("role_id", 1)
    email = post_data.get('email')
    token = post_data.get("token")

    if not password or not email or (role_id == "2" and token != "1fbef"):
        response_object['status'] = 'failure'
        return jsonify(response_object)

    if role_id == "3" and token != "4ktmno":
        response_object['status'] = 'failure'
        return jsonify(response_object)

    # password should be hashed version of text, not the text itself
    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(name=post_data.get('name'),
                email=post_data.get('email'),
                role_id=post_data.get('role_id', 1),
                password=hashed_pw,
                expected_calories=post_data.get('expected_calories', 2000))
    db.session.add(user)
    response_object['message'] = 'User added!'
    db.session.commit()
    response_object['status'] = 'success'
    response_object['user'] =  { "id": user.id,
                                 "name": user.name,
                                 "email": user.email,
                                 "expected_calories": user.expected_calories,
                                 "role_id": user.role_id}
    return jsonify(response_object)


@app.route('/login', methods=['POST'])
def login():
    response_object = {}
    post_data = request.get_json()
    email = post_data["email"]
    password = post_data["password"]
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        response_object['status'] = 'success'
        response_object['user'] =  { "id": user.id,
                                     "name": user.name,
                                     "email": user.email,
                                     "expected_calories": user.expected_calories,
                                     "role_id": user.role_id}
    else:
        response_object['status'] = 'failure'
    return jsonify(response_object)

@app.route('/get-meals-admin/<user_id>', methods=['GET'])
def get_meals_as_admin(user_id):
    response_object = {"meals": []}
    this_user = User.query.filter(User.id == user_id).all()[0]
    admin = False
    if this_user.role_id == 3:
        admin = True
    else:
        return jsonify(response_object)
    meals = Record.query.order_by(Record.datetime).all()

    for meal in meals:
        response_object["meals"].append({"id": meal.id,
                                     "datetime": meal.datetime,
                                     "text": meal.text,
                                     "num_calories": meal.num_calories,
                                     "user_id": meal.user_id})

    return jsonify(response_object)

@app.route('/get-users-manager/<user_id>', methods=['GET'])
def get_users_as_manager(user_id):
    response_object = {"users": []}
    this_user = User.query.filter(User.id == user_id).all()[0]
    manager = False
    if this_user.role_id == 2 or this_user.role_id == 3:
        manager = True
    else:
        return jsonify(response_object)

    users = User.query.all()

    for user in users:
        response_object["users"].append({"id": user.id,
                                         "name": user.name,
                                         "email": user.email,
                                         "expected_calories": user.expected_calories,
                                         "role_id": user.role_id})
    return jsonify(response_object)

#*************************************************#
#********************TEST SUITE*******************#
#*************************************************#

# sanity check route
@app.route('/test', methods=['GET'])
def test():
    return jsonify('hello mr. bond!')


MEALS = [
    {
        'userName': 'John',
        'userId': 123,
        'text': 'ZYX',
        'numCalories': 1234,
        'date': '23-04-2014',
        'time': '1234'
    },
    {
        'userName': 'Jack',
        'userId': 325,
        'text': '51ASF',
        'numCalories': 324,
        'date': '21-04-2015',
        'time': '1212334'
    },
    {
        'userName': 'Jason',
        'userId': 5313,
        'text': '12vnbqw',
        'numCalories': 143,
        'date': '01-07-2015',
        'time': '12341'
    }
]

@app.route('/test-get', methods=['GET'])
def test_get():
    response_object = {}
    response_object['meals'] = MEALS
    return jsonify(response_object)


@app.route('/test-post', methods=['POST'])
def test_post():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        MEALS.append({
            'text': post_data.get('text'),
            'numCalories': post_data.get('numCalories')
        })
        response_object['message'] = 'Meal added!'
        print(MEALS)
    else:
        response_object['meals'] = MEALS
    return jsonify(response_object)

if __name__ == '__main__':
    app.run(debug=True)
