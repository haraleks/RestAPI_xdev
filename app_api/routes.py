from flask import jsonify, make_response, request

from app_api import app
from app_api.function import *

if not models.Role.query.all():
    role_list = ['admin', 'guest', 'vip']
    index = 1
    for r in role_list:
        add_role(r)


@app.route('/')
def index():
    return "Hello, this is API!"


@app.route('/api/create_user', methods=['POST'])
def create_user():
    if not request.json:
        abort(400)
    try:
        full_name = request.json['full_name']
        phone = request.json['phone']
        if full_name and phone:
            new_user = add_user(full_name, phone)
            user_dict = dict(id=new_user.id,
                             full_name=new_user.full_name, phone=new_user.phone,
                             created_on=new_user.created_on, updated_on=new_user.updated_on)
            return jsonify({'new_user': user_dict}), 201
        else:
            abort(500)
    except KeyError:
        abort(500)


@app.route('/api/edit_user/<int:id>',  methods=['PUT'])
def edit_user(id):
    user = filter_id(id)
    if not request.json:
        abort(400)
    full_name_replace, phone_replace = check_request_user_change(request.json)
    check_same_user(full_name_replace, phone_replace)
    if full_name_replace or phone_replace:
        user_replace(id, full_name_replace, phone_replace)
        user_dict = dict(id=user.id,full_name=user.full_name, phone=user.phone,
                         created_on=user.created_on, updated_on=user.updated_on, role=user.role)
        return jsonify({'data changed': user_dict}), 201
    else:
        abort(400)


@app.route('/api/give_roles/<int:id>',  methods=['PUT'])
def give_role(id):
    user = filter_id(id)
    if not user or not request.json or not 'id' in request.json:
        abort(500)
    id_role_list = request.json['id']
    if id_role_list:
        role_all = models.Role.query.all()
        roles_list = roles_id_list(role_all)
        if type(id_role_list) == int:
            add_in_table_role(user, id_role_list)
        else:
            for r in id_role_list:
                if not r in roles_list:
                    abort(500)
                else:
                    add_in_table_role(user, id_role_list)
        user_dict = show_user_roles(id)
        return jsonify({'new_role_assigned': user_dict}), 201
    else:
        abort(400)


@app.route('/api/remove_roles/<int:id>',  methods=['PUT'])
def remove_role(id):
    user = filter_id(id)
    if not user or not request.json or not 'id' in request.json:
        abort(500)
    id_role_list = request.json['id']
    if id_role_list:
        role_all = models.Role.query.all()
        if role_all:
            role_list = []
            for role in role_all:
                role_list.append(role.id)
            if type(id_role_list) == int:
                user.roles.remove(role_all[id_role_list - 1])
                db.session.commit()
            else:
                for r in id_role_list:
                    print(r)
                    if not r in role_list:
                        abort(500)
                    else:
                        user.roles.remove(role_all[r-1])
                        db.session.commit()
            user_dict = show_user_roles(id)
            return jsonify({'new_role_assigned': user_dict}), 201
    else:
        abort(400)


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
        u_roles_list = []
        for r in u.roles:
            u_roles_list.append(r.role_name)
        user_dict = dict(id=u.id,
                         full_name=u.full_name, phone=u.phone, created_on=u.created_on,
                         updated_on=u.updated_on, roles=u_roles_list)
        users_list.append(user_dict)
    return jsonify({'users': users_list}), 201


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Data is in the database'}), 404)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 400)

@app.errorhandler(500)
def repeat_inform(error):
    return make_response(jsonify({'error': 'Data is not correct'}), 500)

@app.errorhandler(401)
def not_found(error):
    return make_response(jsonify({'error': 'more two id in database'}), 401)
