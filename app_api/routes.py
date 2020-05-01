from flask import jsonify, make_response, request, abort

from app_api import app, models, db


def add_role(role_name):
    role_all = models.Role.query.all()
    for role in role_all:
        if role.role_name == role_name:
            print('Error. The role is in the database')
            return 'Error. The role is in the database'
    id = role_all[-1].id + 1
    create_role = models.Role(id=id, role_name=role_name)
    db.session.add(create_role)
    db.session.commit()
    role_list = db.session.query(models.Role).filter(models.Role.id == id).all()
    print('add new role')
    return role_list


def add_user(f_name, t_phone):
    user_all = models.Users.query.all()
    if user_all:
        for user in user_all:
            if user.full_name == f_name and user.phone == t_phone:
                print('Error. There is the user in the database')
                abort(500)
    if not user_all:
        id = 0
    else:
        id = user_all[-1].id + 1
    create_user = models.Users(id=id, full_name=f_name, phone=t_phone)
    db.session.add(create_user)
    db.session.commit()
    user_list = filter_id(id)
    print('add new user')
    return user_list


def filter_id(key_id):
    user = db.session.query(models.Users).filter(models.Users.id == key_id).all()
    return user


def user_replace(id, name_replace, phone_replace):
    user = filter_id(id)
    if len(user) >=2:
        abort(401)
    else:
        if name_replace:
            user[0].full_name = name_replace
        if phone_replace:
            user[0].phone = phone_replace
        db.session.add(user[0])
        db.session.commit()


if not models.Role.query.all():
    role_list = ['admin', 'guest', 'vip']
    index = 1
    for r in role_list:
        add_role(r)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/api/create_user', methods=['POST'])
def create_user():
    if not request.json:
        abort(400)
    try:
        full_name = request.json['full_name']
        phone = request.json['phone']
        new_user = add_user(full_name, phone)
        user_dict = dict(id=new_user[0].id,
                         full_name=new_user[0].full_name,
                         phone=new_user[0].phone,
                         created_on=new_user[0].created_on,
                         updated_on=new_user[0].updated_on)

        return jsonify({'new_user': user_dict}), 201
    except KeyError:
        abort(500)


@app.route('/api/edit_user/<int:id>',  methods=['PUT'])
def edit_user(id):
    user = filter_id(id)
    if not user:
        abort(400)
    try:
        full_name_replace = request.json['full_name']

    except KeyError:
        full_name_replace = ''
    try:
        phone_replace = request.json['phone']
    except KeyError:
        phone_replace = ''
    if full_name_replace or phone_replace:
        user_replace(id, full_name_replace, phone_replace)
        user = filter_id(id)
        user_dict = dict(id=user[0].id,
                         full_name=user[0].full_name,
                         phone=user[0].phone,
                         created_on=user[0].created_on,
                         updated_on=user[0].updated_on)

        return jsonify({'data changed': user_dict}), 201
    else:
        abort(400)

@app.route('/api/give_role/',  methods=['PUT'])
def give_role():
    pass


@app.route('/api/change_role/',  methods=['PUT'])
def change_role():
    pass

@app.route('/api/get_roles', methods=['GET'])
def get_roles():
    roles = models.Role.query.all()
    roles_list = []
    for r in roles:
        roles_dict = dict(id=r.id,
                         role_name=r.role_name)
        roles_list.append(roles_dict)

    return jsonify({'roles': roles_list})


@app.route('/api/get_users', methods=['GET'])
def get_users():
    users = models.Users.query.all()
    users_list = []
    for u in users:
        user_dict = dict(id=u.id,
                         full_name=u.full_name,
                         phone=u.phone,
                         created_on=u.created_on,
                         updated_on=u.updated_on)
        users_list.append(user_dict)

    return jsonify({'users': users_list})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 400)

@app.errorhandler(500)
def repeat_inform(error):
    return make_response(jsonify({'error': 'Data is not correct'}), 500)

@app.errorhandler(401)
def not_found(error):
    return make_response(jsonify({'error': 'more two id in database'}), 401)
