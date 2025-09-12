from flask import Flask, request, jsonify
from database import db
from models.user import User, Meal
from flask_login import LoginManager, login_user, current_user, logout_user, login_required


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3307/flask-crud'

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)

login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({"message": "You need to be logged in to perform this action"})


@app.route("/login", methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
         user = User.query.filter_by(username=username).first()

         if user and user.password == password:
             login_user(user)
             print(current_user.is_authenticated)
             return jsonify({"message": "You have successfully logged in"})

    return jsonify({"message": "Invalid credentials"}), 400

@app.route('/logout', methods=["GET"])
@login_required

def logout():
    logout_user()
    return jsonify({"message": "You have successfully logged out"})

@app.route('/createuser', methods=['POST'])
def create_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({"message": f"Username {username} already taken"}), 403

        user = User(username=username, password=password, role='user')
        db.session.add(user)
        db.session.commit()
        return jsonify ({"message": "User successfully registered"})

    return jsonify({"message": "Invalid credentials type"}), 400

@app.route('/user/<int:id_user>', methods=['GET'])
@login_required
def read_user(id_user):
    user = User.query.get(id_user)

    if user:
        for meal in user.meals:
            jsonify({"message": f"{meal}"})

    
    return jsonify({"message": "User not found"}), 404

@app.route('/user/<int:id_user>', methods=['PUT'])
@login_required
def update_user(id_user):
    data = request.json
    user = User.query.get(id_user)

    if id_user != current_user.id and current_user.role == 'user':
        return jsonify({"message": "Operation not allowed"}), 403
    
    if user and data.get("password"):
        user.password = data.get("password")
        db.session.commit()

        return jsonify({"message": f"User {user.username}(id:{id_user}) was successfully updated"})

    return jsonify({"message": "User not found"}), 404

@app.route('/user/<int:id_user>', methods=['DELETE'])
@login_required
def delete_user(id_user):
    user = User.query.get(id_user)

    if id_user == current_user.id or current_user.role != 'admin':
        return jsonify ({"message": "Operation not allowed"})
    
    if user:
        deleted_username = user.username
        db.session.delete(user)
        db.session.commit()
        return jsonify ({"message": f"User {deleted_username} (id:{id_user}) was successfully deleted"})
    
    return jsonify({"message": "User not found"}), 404

@app.route('/createmeal/<int:id_user>', methods=['POST'])
@login_required
def create_meal(id_user):

    user = User.query.get(id_user)

    if not user:
        return jsonify({"message": "User not found"}), 404

    if id_user != current_user.id:
        return jsonify({"message": "You can only create meals for your won user"}) , 403
    
    data = request.json
    name = data.get("name")
    description = data.get("description")
    mealtime = data.get("mealtime")
    indiet = data.get("indiet")

    if name and indiet is not None:
        new_meal = Meal(name=name, description=description, mealtime=mealtime, indiet=indiet, user_id=id_user)
        db.session.add(new_meal)
        db.session.commit()
        return jsonify({"message": "Meal successfully registered"})

    return jsonify({"message": "The meal need at least a name and if it's in the diet"}), 400

@app.route('/readmeals/<int:id_user>', methods=['GET'])
@login_required

def read_meals(id_user):
    user = User.query.get(id_user)
    meal_list = []

    if not user:
        return jsonify({"message": "User not found"}), 404
    
    if id_user != current_user.id:
        return jsonify ({"message": "You may only see your own meals"})

    if not user.meals:
        return jsonify({"message": "User has no meals"}), 404
    
    for meal in user.meals:
            meal_data = {
                "id": meal.id,
                "name": meal.name,
                "description": meal.description,
                "indiet": meal.indiet
            }

            meal_list.append(meal_data)
    
    return jsonify(meal_list)

@app.route('/readmeals/<int:id_user>/<int:id_meal>', methods=['GET'])
@login_required

def read_meal(id_user, id_meal):

    user = User.query.get(id_user)

    if not user:
        return jsonify({"message": "User not found"}), 404
    
    if id_user != current_user.id:
        return jsonify ({"message": "You may only see your own meals"})

    if not user.meals:
        return jsonify({"message": "User has no meals"}), 404
    
    for meal in user.meals:
        if id_meal == meal.id:
            meal_data = { 
                "id": meal.id,
                "name": meal.name,
                "description": meal.description,
                "indiet": meal.indiet
            }
            return jsonify(meal_data)
        
    return jsonify({"message": "Meal not found"}), 404

@app.route('/user/<int:id_user>/<int:id_meal>', methods=['DELETE'])
@login_required

def delete_meal(id_user, id_meal):
    user = User.query.get(id_user)

    if not user:
        return jsonify({"message": "User not found"}), 404

    if id_user != current_user.id:
        return jsonify ({"message": "You may only delete your own meals"})
    
    if not user.meals:
        return jsonify({"message": "User has no meals"}), 404
    
    for meal in user.meals:
        if meal.id == id_meal:
            deleted_meal = meal.name
            deleted_meal_id = meal.id
            db.session.delete(meal)
            db.session.commit()
            return jsonify ({"message": f"Meal {deleted_meal}(id: {deleted_meal_id}) was successfully deleted"})
        
    return jsonify({"message": "Meal not found"}), 404

@app.route('/user/<int:id_user>/<int:id_meal>', methods=['PUT'])
@login_required
def edit_meal(id_user, id_meal):

    user = User.query.get(id_user)
    meal = Meal.query.get(id_meal)

    if not user:
        return jsonify({"message": "User not found"}), 404

    if id_user != current_user.id or current_user.role == 'user':
        return jsonify ({"message": "You don't have permission to do that"}), 403
    
    if not user.meals:
        return jsonify({"message": "User has no meals"}), 404
    
    data = request.json

    if data.get("name") and data.get("indiet") is not None:
        for meals in user.meals:
            if id_meal == meals.id:
                old_name = meals.name
                meal.name = data.get("name")
                meal.description = data.get("description")
                meal.mealtime = data.get("mealtime")
                meal.indiet = data.get("indiet")
                db.session.commit()
                return jsonify ({"message": f"Meal {old_name} was successfully updated to {meal.name}"})

        return jsonify({"message": "Meal not found"}), 404
        
    return jsonify({"message": "Meal needs to have both a name and if it is in the diet"})
    



if __name__ == '__main__':
    app.run(debug=True)


 