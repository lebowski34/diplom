from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

tasks = []
users = []
products = []


# Главная страница с приветствием пользователя
@app.route('/')
def home():
    current_user = session.get('username')  # Получаем имя текущего пользователя из сессии
    return render_template('home.html', current_user=current_user, users=users)  # Передаем список пользователей


# Задачи
@app.route('/tasks/')
def task_list():
    return render_template('task_list.html', tasks=tasks)


@app.route('/tasks/add/', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        tasks.append({'title': title, 'completed': False})
        return redirect(url_for('task_list'))
    return render_template('add_task.html')


@app.route('/tasks/edit/<int:task_id>/', methods=['GET', 'POST'])
def edit_task(task_id):
    task = tasks[task_id]
    if request.method == 'POST':
        task['title'] = request.form['title']
        return redirect(url_for('task_list'))
    return render_template('edit_task.html', task=task, task_id=task_id)


@app.route('/tasks/delete/<int:task_id>/')
def delete_task(task_id):
    tasks.pop(task_id)
    return redirect(url_for('task_list'))


# Пользователи
@app.route('/users/')
def user_list():
    return render_template('user_list.html', users=users)


@app.route('/users/add/', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        if any(user['username'] == username for user in users):
            return "Пользователь с таким именем уже существует.", 400
        users.append({'username': username})
        return redirect(url_for('user_list'))
    return render_template('add_user.html')


# Регистрация
@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Проверка, что пароль совпадает с подтверждением
        if password != confirm_password:
            flash('Пароли не совпадают', 'error')
            return redirect(url_for('register'))

        # Проверка, что пользователь не существует
        if any(user['username'] == username for user in users):
            flash('Пользователь с таким именем уже существует', 'error')
            return redirect(url_for('register'))

        # Добавляем нового пользователя
        users.append({'username': username, 'password': password})
        session['username'] = username  # Сохраняем пользователя в сессии
        flash('Регистрация прошла успешно!', 'success')
        return redirect(url_for('home'))  # Перенаправляем на главную страницу

    return render_template('register.html')


# Продукты
@app.route('/products/')
def product_list():
    return render_template('register.html', products=products)


@app.route('/products/add/', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        products.append({'title': title, 'price': price})
        return redirect(url_for('product_list'))
    return render_template('add_product.html')


if __name__ == '__main__':
    app.run(debug=True)
