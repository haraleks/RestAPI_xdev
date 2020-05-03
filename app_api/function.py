from flask import abort

from app_api import models, db


def roles_id_list(role_all):
    if role_all:
        role_list = []
        for role in role_all:
            role_list.append(role.id)
    return role_list

def add_in_table_role(user, id_role_list):
    role_all = models.Role.query.all()
    user.roles.append(role_all[id_role_list - 1])
    db.session.add(user)
    db.session.commit()


def add_role(role_name: list):
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


def check_request_user_change(req):
    if 'full_name' in req and 'phone' in req:
        full_name_replace = req['full_name']
        phone_replace = req['phone']
    elif not 'full_name' in req or not 'phone' in req:
        abort(500)
    return full_name_replace, phone_replace


def filter_id(key_id):
    user = db.session.query(models.Users).filter(models.Users.id == key_id).all()
    if not user:
        abort(400)
    if len(user) >= 2:
        abort(401)
    user = user[0]
    return user


def check_same_user(name, phone):
    user_all = models.Users.query.all()
    if user_all:
        for user in user_all:
            if user.full_name == name and user.phone == phone:
                abort(404)


def add_user(f_name, t_phone):
    user_all = models.Users.query.all()
    check_same_user(f_name, t_phone)
    if not user_all:
        id = 0
    else:
        id = user_all[-1].id + 1
    create_user = models.Users(id=id, full_name=f_name, phone=t_phone)
    db.session.add(create_user)
    db.session.commit()
    user_list = filter_id(id)
    return user_list


def user_replace(id, name_replace, phone_replace):
    user = filter_id(id)
    if name_replace:
        user.full_name = name_replace
    if phone_replace:
        user.phone = phone_replace
    db.session.add(user)
    db.session.commit()
