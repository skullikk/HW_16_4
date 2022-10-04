import json

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False

db = SQLAlchemy(app)


def get_data_from_json(path):
    """
    Функция получения данных из json файла
    :param path: str
    :return: list[dict]
    """
    with open(path, encoding='utf-8') as file:
        return json.load(file)


# Объявляем модели User, Order, Offer
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text(50))
    last_name = db.Column(db.Text(50))
    age = db.Column(db.Integer)
    email = db.Column(db.Text(50))
    role = db.Column(db.Text(50))
    phone = db.Column(db.Text(50))

    def return_data(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone
        }


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(50))
    description = db.Column(db.Text(100))
    start_date = db.Column(db.Text(25))
    end_date = db.Column(db.Text(25))
    address = db.Column(db.Text(100))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    customer = db.relationship("User", foreign_keys="Order.customer_id")
    executor = db.relationship("User", foreign_keys="Order.executor_id")

    def return_data(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id
        }


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    order = db.relationship("Order", foreign_keys="Offer.order_id")
    executor = db.relationship("User", foreign_keys="Offer.executor_id")

    def return_data(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id
        }


# Очищаем и создаем таблицы
db.drop_all()
db.create_all()

# Заполняем таблицы данными из json файлов
for add_user in get_data_from_json('data/users.json'):
    db.session.add(User(**add_user))

for add_order in get_data_from_json('data/orders.json'):
    db.session.add(Order(**add_order))

for add_offer in get_data_from_json('data/offers.json'):
    db.session.add(Offer(**add_offer))

db.session.commit()
db.session.close()


@app.route('/')
def hello_my_home_work():  # put application's code here
    return 'Hello My Home Work №16!'


# Создаем представления и методы для модели User
@app.route('/users/', methods=['GET', 'POST'])
def work_users():
    if request.method == 'GET':
        result = []
        users = db.session.query(User).all()
        for user in users:
            result.append(user.return_data())
        return jsonify(result)
    if request.method == 'POST':
        data = request.json
        db.session.add(User(**data))
        db.session.commit()
        db.session.close()
        return app.response_class(json.dumps('OK'), status=200, mimetype='application/json')


@app.route('/users/<int:gid>', methods=['GET', 'PUT', 'DELETE'])
def work_user(gid):
    if request.method == 'GET':
        user = db.session.query(User).get(gid)
        return jsonify(user.return_data())
    if request.method == 'DELETE':
        db.session.query(User).filter(User.id == gid).delete()
        db.session.commit()
        db.session.close()
        return app.response_class(json.dumps('OK'), status=200, mimetype='application/json')
    if request.method == 'PUT':
        user = db.session.query(User).get(gid)
        data = request.json
        user.id = data.get("id")
        user.first_name = data.get("first_name")
        user.last_name = data.get("last_name")
        user.age = data.get("age")
        user.email = data.get("email")
        user.role = data.get("role")
        user.phone = data.get("phone")
        db.session.add(user)
        db.session.commit()
        db.session.close()
        return app.response_class(json.dumps('OK'), status=200, mimetype='application/json')


# Создаем представления и методы для модели Order
@app.route('/orders/', methods=['GET', 'POST'])
def work_orders():
    if request.method == 'GET':
        result = []
        orders = db.session.query(Order).all()
        for order in orders:
            result.append(order.return_data())
        return jsonify(result)
    if request.method == 'POST':
        data = request.json
        db.session.add(Order(**data))
        db.session.commit()
        db.session.close()
        return app.response_class(json.dumps('OK'), status=200, mimetype='application/json')


@app.route('/orders/<int:gid>', methods=['GET', 'PUT', 'DELETE'])
def work_order(gid):
    if request.method == 'GET':
        order = db.session.query(Order).get(gid)
        return jsonify(order.return_data())
    if request.method == 'DELETE':
        db.session.query(Order).filter(Order.id == gid).delete()
        db.session.commit()
        db.session.close()
        return app.response_class(json.dumps('OK'), status=200, mimetype='application/json')
    if request.method == 'PUT':
        order = db.session.query(Order).get(gid)
        data = request.json
        order.id = data.get("id")
        order.name = data.get("name")
        order.description = data.get("description")
        order.start_date = data.get("start_date")
        order.end_date = data.get("end_date")
        order.address = data.get("address")
        order.price = data.get("price")
        order.customer_id = data.get("customer_id")
        order.executor_id = data.get("executor_id")
        db.session.add(order)
        db.session.commit()
        db.session.close()
        return app.response_class(json.dumps('OK'), status=200, mimetype='application/json')


# Создаем представления и методы для модели Offer
@app.route('/offers/', methods=['GET', 'POST'])
def work_offers():
    if request.method == 'GET':
        result = []
        offers = db.session.query(Offer).all()
        for offer in offers:
            result.append(offer.return_data())
        return jsonify(result)
    if request.method == 'POST':
        data = request.json
        db.session.add(Offer(**data))
        db.session.commit()
        db.session.close()
        return app.response_class(json.dumps('OK'), status=200, mimetype='application/json')


@app.route('/offers/<int:gid>', methods=['GET', 'PUT', 'DELETE'])
def work_offer(gid):
    if request.method == 'GET':
        offer = db.session.query(Offer).get(gid)
        return jsonify(offer.return_data())
    if request.method == 'DELETE':
        db.session.query(Offer).filter(Offer.id == gid).delete()
        db.session.commit()
        db.session.close()
        return app.response_class(json.dumps('OK'), status=200, mimetype='application/json')
    if request.method == 'PUT':
        offer = db.session.query(Offer).get(gid)
        data = request.json
        offer.id = data.get("id")
        offer.order_id = data.get("order_id")
        offer.executor_id = data.get("executor_id")
        db.session.add(offer)
        db.session.commit()
        db.session.close()
        return app.response_class(json.dumps('OK'), status=200, mimetype='application/json')


if __name__ == '__main__':
    app.run()
