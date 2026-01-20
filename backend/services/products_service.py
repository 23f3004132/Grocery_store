from models import Product
from services.service_errors import ServiceError

class ProductsService():

    @staticmethod
    def get_all():
        return Product.query.all()
    
    @staticmethod
    def get_by_id(id):
        item = Product.query.get(id)
        if not item:
            raise ServiceError(f"Product with id {id} not found")
        return item
