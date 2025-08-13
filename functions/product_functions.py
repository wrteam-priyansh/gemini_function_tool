import json
import os
from typing import List, Dict, Any, Optional
from models import Product

class ProductFunctions:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.products_file = os.path.join(data_dir, "products.json")
    
    def _load_products(self) -> List[Product]:
        """Load products from JSON file"""
        try:
            with open(self.products_file, 'r') as f:
                products_data = json.load(f)
            return [Product.from_dict(product) for product in products_data]
        except FileNotFoundError:
            return []
    
    def search_products(self, query: str = "", category: str = "", max_price: float = None, min_price: float = None) -> List[Dict[str, Any]]:
        """
        Search for products based on name, category, and price range.
        
        Args:
            query: Search term for product name or description
            category: Product category to filter by
            max_price: Maximum price filter
            min_price: Minimum price filter
        
        Returns:
            List of matching products with their details
        """
        products = self._load_products()
        results = []
        
        for product in products:
            # Text search
            if query and query.lower() not in product.name.lower() and query.lower() not in product.description.lower():
                continue
                
            # Category filter
            if category and category.lower() != product.category.lower():
                continue
                
            # Price filters
            if max_price is not None and product.price > max_price:
                continue
            if min_price is not None and product.price < min_price:
                continue
            
            results.append(product.to_dict())
        
        return results
    
    def get_product_by_id(self, product_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific product by its ID.
        
        Args:
            product_id: The product ID to search for
        
        Returns:
            Product details if found, None otherwise
        """
        products = self._load_products()
        for product in products:
            if product.id == product_id:
                return product.to_dict()
        return None
    
    def check_product_availability(self, product_id: str, quantity: int = 1) -> Dict[str, Any]:
        """
        Check if a product is available in the requested quantity.
        
        Args:
            product_id: The product ID to check
            quantity: Required quantity
        
        Returns:
            Availability status and stock information
        """
        product = self.get_product_by_id(product_id)
        if not product:
            return {"available": False, "message": "Product not found", "stock": 0}
        
        available = product["stock"] >= quantity
        return {
            "available": available,
            "message": f"{'Available' if available else 'Not enough stock'}",
            "stock": product["stock"],
            "requested": quantity
        }

# Define function schemas for Gemini API
PRODUCT_FUNCTION_SCHEMAS = [
    {
        "name": "search_products",
        "description": "Search for sports products based on various criteria like name, category, and price range",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search term for product name or description"
                },
                "category": {
                    "type": "string",
                    "description": "Product category (e.g., Football, Baseball, Tennis, Apparel, Safety, Footwear)"
                },
                "max_price": {
                    "type": "number",
                    "description": "Maximum price filter"
                },
                "min_price": {
                    "type": "number", 
                    "description": "Minimum price filter"
                }
            }
        }
    },
    {
        "name": "get_product_by_id",
        "description": "Get detailed information about a specific product using its ID",
        "parameters": {
            "type": "object",
            "properties": {
                "product_id": {
                    "type": "string",
                    "description": "The unique product ID"
                }
            },
            "required": ["product_id"]
        }
    },
    {
        "name": "check_product_availability",
        "description": "Check if a product is available in stock for the requested quantity",
        "parameters": {
            "type": "object",
            "properties": {
                "product_id": {
                    "type": "string",
                    "description": "The unique product ID to check"
                },
                "quantity": {
                    "type": "integer",
                    "description": "Quantity needed (default: 1)"
                }
            },
            "required": ["product_id"]
        }
    }
]