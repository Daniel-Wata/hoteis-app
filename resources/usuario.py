from flask_restful import Resource,reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from hmac import compare_digest
from blacklist import BLACKLIST


class User(Resource):
    #/usuarios/{user_id}
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        else:
            return {'message':'User not found.'},404

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return {"message": "Database error on deleting user."}, 500
            return {"message": "User deleted"},200
        return {"message": "User not Found"},404

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help='the field login is mandatory')
atributos.add_argument('senha', type=str, required=True, help='the field senha is mandatory')

class UserRegister(Resource):
    def post(self):
        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {'message': 'Já existe um usuário com este login.'}
        
        user = UserModel(**dados)
        user.save_user()
        return {'message':'User created successfully'}, 201

class UserLogin(Resource):
    def post(cls):
        dados = atributos.parse_args()

        user = UserModel.find_by_login(dados['login'])

        if user and compare_digest(user.senha, dados['senha']):
            token_de_acesso = create_access_token(identity=user.user_id)
            return {'access_token': token_de_acesso}, 200
        return {'message': 'The username or password is incorrect.'}, 401


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged out successfully.'},200

