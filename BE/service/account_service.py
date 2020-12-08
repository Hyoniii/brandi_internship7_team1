import bcrypt
import jwt
from datetime import (datetime, timedelta)
from model.account_dao import AccountDao
from config import (SECRET_KEY, ALGORITHM)
from flask import jsonify


class AccountService:
    def __init__(self):
        pass

    def signup_account(self, account_info, connection):
        account_dao = AccountDao()

        is_existing_email = account_dao.find_account(account_info, connection)
        if is_existing_email:
            raise Exception('EXISTING_EMAIL')

        bcrypt_password = bcrypt.hashpw(account_info['password'].encode('utf-8'), bcrypt.gensalt())
        account_info['password'] = bcrypt_password

        signed_up_id = account_dao.create_account(account_info, connection)
        account_info['account_id'] = signed_up_id
        account_info['editor_id'] = signed_up_id
        account_info['is_active'] = 1
        account_dao.create_account_log(account_info, connection)
        return signed_up_id

    def signup_seller(self, account_info, connection):
        account_dao = AccountDao()

        is_existing_email = account_dao.find_account(account_info, connection)
        if is_existing_email:
            raise Exception('EXISTING_EMAIL')

        is_kr_name_taken = account_dao.find_seller_name_kr_exist(account_info, connection)
        if is_kr_name_taken:
            raise Exception('EXISTING_KR_NAME')

        is_en_name_taken = account_dao.find_seller_name_en_exist(account_info, connection)
        if is_en_name_taken:
            raise Exception('EXISTING_EN_NAME')

        bcrypt_password = bcrypt.hashpw(account_info['password'].encode('utf-8'), bcrypt.gensalt())
        account_info['password'] = bcrypt_password

        signed_up_account = account_dao.create_account(account_info, connection)
        account_info['account_id'] = signed_up_account
        account_info['editor_id'] = signed_up_account
        account_info['is_active'] = 1
        account_info['profile_pic_url'] = ''
        account_info['short_desc'] = ''
        account_info['long_desc'] = ''
        account_info['close_time'] = ''
        account_info['open_time'] = ''
        account_info['delivery_policy'] = ''
        account_info['return_policy'] = ''
        account_info['zip_code'] = ''
        account_info['address_1'] = ''
        account_info['address_2'] = ''
        account_info['is_open_weekend'] = ''

        account_dao.create_account_log(account_info, connection)

        signed_up_seller = account_dao.create_seller(account_info, connection)
        account_info['seller_id'] = signed_up_seller

        account_dao.create_seller_log(account_info, connection)

        return signed_up_seller

    def signin(self, login_info, connection):
        account_dao = AccountDao()
        account = account_dao.find_account(login_info, connection)

        if account:
            if account['is_active'] == 0:
                raise Exception('ACCOUNT_NOT_ACTIVE')
            if bcrypt.checkpw(login_info['password'].encode('utf-8'), account['password'].encode('utf-8')):
                token = jwt.encode({'account_id': account['id'], 'expiration': str(datetime.utcnow() + timedelta(hours=1))}, SECRET_KEY, algorithm=ALGORITHM)
                return jsonify({'AUTHORIZATION': token}), 200
            else:
                raise Exception('CHECK_LOGIN')
        else:
            raise Exception('ACCOUNT_DOES_NOT_EXIST')

    def filter_seller(self, filter_info, user, connection):
        account_dao = AccountDao()
        account_type_id = user.get('account_type_id')
        filter_info['offset'] = (filter_info['page'] * filter_info['limit']) - filter_info['limit']
        if account_type_id != 1:
            raise Exception('NO_AUTH')
        seller_list = account_dao.list_seller(filter_info, connection)
        for items in seller_list:
            status = {'status_id': items['seller_status_id']}
            actions = account_dao.get_seller_actions(status, connection)
            items['actions'] = actions
        return seller_list

    def change_account_info(self, change_info, user, connection):
        account_dao = AccountDao()
        if change_info['password']:
            bcrypt_password = bcrypt.hashpw(change_info['password'].encode('utf-8'), bcrypt.gensalt())
            change_info['password'] = bcrypt_password
        change = account_dao.update_account_info(change_info, connection)
        if not change:
            raise Exception('NOTHING_CHANGED')
        get_account_info = account_dao.get_account_info(change_info, connection)
        get_account_info['editor_id'] = user['account_id']
        get_account_info["account_id"] = get_account_info.pop("id")
        account_dao.create_account_log(get_account_info, connection)
        if change_info['id'] != user['account_id'] and user['account_type_id'] == 2:
            raise Exception('NO_AUTH')
        return jsonify({'MESSAGE': 'SUCCESS'}), 200

    def change_seller_info(self, change_info, user, connection):
        account_dao = AccountDao()
        if change_info['seller_id'] != user['account_id'] and user['account_type_id'] == 2:
            raise Exception('NO_AUTH')
        change_info['id'] = change_info.pop('seller_id')
        account_dao.update_seller(change_info, connection)
        seller_info = change_info
        account_info = account_dao.get_seller_info(seller_info, connection)
        account_info['seller_id'] = account_info.pop('id')
        account_info['editor_id'] = user['account_id']
        account_dao.create_seller_log(account_info, connection)
        return jsonify({'MESSAGE': 'SUCCESS'}), 200

    def change_status(self, status, user, connection):
        account_dao = AccountDao()
        actions = account_dao.get_seller_actions_two(status, connection)
        if not actions:
            raise Exception('Invalid action for status')
        new_status_id = actions[0]['new_status_id']
        seller_id = status['seller_id']
        change_info = {'id': seller_id, 'seller_status': new_status_id}
        account_dao.update_seller_status(change_info, connection)
        seller_info = {'id': seller_id}
        account_info = account_dao.get_seller_info(seller_info, connection)
        account_info['seller_id'] = account_info.pop('id')
        account_info['editor_id'] = user['account_id']
        account_dao.create_seller_log(account_info, connection)
        return actions
