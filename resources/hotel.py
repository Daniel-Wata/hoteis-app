from flask_restful import Resource,reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required


class Hoteis(Resource):
    def get(self):
        return {'dados': [hotel.json() for hotel in HotelModel.query.all()]}


class Hotel(Resource):

    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="Field nome is mandatory.")
    argumentos.add_argument('estrelas', type=float, required=True, help="Field estrelas is mandatory.")
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        else:
            return {'message':'hotel not found'},404
    
    @jwt_required()
    def post(self, hotel_id):
        

        if HotelModel.find_hotel(hotel_id):
            return {'message': 'O hotel "{}" já existe'.format(hotel_id)},400

        dados = Hotel.argumentos.parse_args()
        hotel= HotelModel(hotel_id,**dados)
        try:
            hotel.save_hotel()
        except:
            return {"message": "Database error on saving hotel."}, 500
        return hotel.json()

    @jwt_required()
    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        
        hotel_encontrado = HotelModel.find_hotel(hotel_id)

        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(),200
        else:
            hotel= HotelModel(hotel_id,**dados)
            try:
                hotel.save_hotel()
            except:
                return {"message": "Database error on saving hotel."}, 500
            return hotel.json(),201

    @jwt_required()
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {"message": "Database error on deleting hotel."}, 500
            return {"message": "Hotel deleted"},200
        return {"message": "Hotel not Found"},404

