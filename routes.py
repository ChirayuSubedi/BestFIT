from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db, login_manager
from models import User, Workout, MealPlan, FoodSuggestion

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        age = request.form['age']
        height = request.form['height']
        weight = request.form['weight']
        goal = request.form['goal']
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, age=age, height=height, weight=weight, goal=goal)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.username = request.form['username']
        if request.form['password']:
            current_user.password = generate_password_hash(request.form['password'])
        current_user.age = request.form['age']
        current_user.height = request.form['height']
        current_user.weight = request.form['weight']
        current_user.goal = request.form['goal']
        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('profile'))
    return render_template('profile.html')

@app.route('/dashboard')
@login_required
def dashboard():
    workouts = Workout.query.filter_by(user_id=current_user.id).all()
    meal_plans = MealPlan.query.filter_by(user_id=current_user.id).all()

    # Prepare data for charts
    workout_names = [workout.name for workout in workouts]
    workout_durations = [workout.duration for workout in workouts]
    meal_plan_names = [meal_plan.name for meal_plan in meal_plans]
    meal_plan_calories = [meal_plan.calories for meal_plan in meal_plans]

    return render_template('dashboard.html', workouts=workouts, meal_plans=meal_plans,
                           workout_names=workout_names, workout_durations=workout_durations,
                           meal_plan_names=meal_plan_names, meal_plan_calories=meal_plan_calories)

@app.route('/workouts', methods=['GET', 'POST'])
@login_required
def workouts():
    query = Workout.query.filter_by(user_id=current_user.id)
    if request.method == 'POST':
        search_term = request.form['search']
        query = query.filter(Workout.name.contains(search_term))
    all_workouts = query.all()
    return render_template('workouts.html', workouts=all_workouts)

@app.route('/meal_plans', methods=['GET', 'POST'])
@login_required
def meal_plans():
    query = MealPlan.query.filter_by(user_id=current_user.id)
    if request.method == 'POST':
        search_term = request.form['search']
        query = query.filter(MealPlan.name.contains(search_term))
    all_meal_plans = query.all()
    return render_template('meal_plans.html', meal_plans=all_meal_plans)

@app.route('/add_workout', methods=['POST'])
@login_required
def add_workout():
    name = request.form['name']
    description = request.form['description']
    duration = request.form['duration']
    new_workout = Workout(name=name, description=description, duration=duration, user_id=current_user.id)
    db.session.add(new_workout)
    db.session.commit()
    return redirect(url_for('workouts'))

@app.route('/add_meal_plan', methods=['POST'])
@login_required
def add_meal_plan():
    name = request.form['name']
    description = request.form['description']
    calories = request.form['calories']
    new_meal_plan = MealPlan(name=name, description=description, calories=calories, user_id=current_user.id)
    db.session.add(new_meal_plan)
    db.session.commit()
    return redirect(url_for('meal_plans'))

@app.route('/suggestions')
@login_required
def suggestions():
    suggestions = FoodSuggestion.query.filter_by(user_id=current_user.id).all()
    return render_template('suggestions.html', suggestions=suggestions)

@app.route('/add_suggestion', methods=['POST'])
@login_required
def add_suggestion():
    name = request.form['name']
    description = request.form['description']
    calories = request.form['calories']
    new_suggestion = FoodSuggestion(name=name, description=description, calories=calories, user_id=current_user.id)
    db.session.add(new_suggestion)
    db.session.commit()
    return redirect(url_for('suggestions'))
