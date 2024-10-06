class ProductService:
    def __init__(self, product_list):
        self.product_list = product_list

    def find_product_by_id(self, id):
        for product in self.product_list:
            if product.id == id:
                return product
        return None

    def find_products_by_category(self, categories):
        products = []
        for product in self.product_list:
            if any(category in product.categories for category in categories):
                products.append(product)
        return products