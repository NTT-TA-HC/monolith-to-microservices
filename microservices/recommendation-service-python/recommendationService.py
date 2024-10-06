class RecommendationService:
    def __init__(self, product_service):
        self.product_service = product_service

    def get_recommended_products(self, product):
        recommended_products = self.product_service.find_products_by_category(product.categories)
        return [p for p in recommended_products if p.id != product.id]