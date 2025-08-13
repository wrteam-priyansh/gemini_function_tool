import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
from models import Cart, CartItem, Order
from functions.product_functions import ProductFunctions

class CartFunctions:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.cart_file = os.path.join(data_dir, "cart.json")
        self.orders_file = os.path.join(data_dir, "orders.json")
        self.product_functions = ProductFunctions(data_dir)
    
    def _load_cart(self, user_id: str = "user123") -> Cart:
        """Load cart from JSON file"""
        try:
            with open(self.cart_file, 'r') as f:
                cart_data = json.load(f)
            if cart_data.get('user_id') == user_id:
                return Cart.from_dict(cart_data)
            else:
                return Cart(user_id=user_id, items=[])
        except FileNotFoundError:
            return Cart(user_id=user_id, items=[])
    
    def _save_cart(self, cart: Cart):
        """Save cart to JSON file"""
        with open(self.cart_file, 'w') as f:
            json.dump(cart.to_dict(), f, indent=2)
    
    def add_to_cart(self, product_id: str, quantity: int = 1, user_id: str = "user123") -> Dict[str, Any]:
        """
        Add a product to the cart.
        
        Args:
            product_id: Product ID to add
            quantity: Quantity to add
            user_id: User ID
        
        Returns:
            Status of the add operation
        """
        # Check if product exists and is available
        product = self.product_functions.get_product_by_id(product_id)
        if not product:
            return {"success": False, "message": "Product not found"}
        
        availability = self.product_functions.check_product_availability(product_id, quantity)
        if not availability["available"]:
            return {"success": False, "message": availability["message"]}
        
        # Load cart
        cart = self._load_cart(user_id)
        
        # Check if item already in cart
        existing_item = None
        for item in cart.items:
            if item.product_id == product_id:
                existing_item = item
                break
        
        if existing_item:
            # Update quantity
            new_quantity = existing_item.quantity + quantity
            # Check availability for new total quantity
            availability = self.product_functions.check_product_availability(product_id, new_quantity)
            if not availability["available"]:
                return {"success": False, "message": f"Cannot add {quantity} more. {availability['message']}"}
            existing_item.quantity = new_quantity
        else:
            # Add new item
            cart_item = CartItem(product_id=product_id, quantity=quantity, price=product["price"])
            cart.items.append(cart_item)
        
        self._save_cart(cart)
        return {"success": True, "message": f"Added {quantity} x {product['name']} to cart"}
    
    def remove_from_cart(self, product_id: str, user_id: str = "user123") -> Dict[str, Any]:
        """
        Remove a product from the cart.
        
        Args:
            product_id: Product ID to remove
            user_id: User ID
        
        Returns:
            Status of the remove operation
        """
        cart = self._load_cart(user_id)
        
        # Find and remove item
        for i, item in enumerate(cart.items):
            if item.product_id == product_id:
                removed_item = cart.items.pop(i)
                self._save_cart(cart)
                product = self.product_functions.get_product_by_id(product_id)
                product_name = product["name"] if product else product_id
                return {"success": True, "message": f"Removed {product_name} from cart"}
        
        return {"success": False, "message": "Product not found in cart"}
    
    def update_cart_quantity(self, product_id: str, quantity: int, user_id: str = "user123") -> Dict[str, Any]:
        """
        Update quantity of a product in the cart.
        
        Args:
            product_id: Product ID to update
            quantity: New quantity
            user_id: User ID
        
        Returns:
            Status of the update operation
        """
        if quantity <= 0:
            return self.remove_from_cart(product_id, user_id)
        
        # Check availability
        availability = self.product_functions.check_product_availability(product_id, quantity)
        if not availability["available"]:
            return {"success": False, "message": availability["message"]}
        
        cart = self._load_cart(user_id)
        
        # Find and update item
        for item in cart.items:
            if item.product_id == product_id:
                item.quantity = quantity
                self._save_cart(cart)
                product = self.product_functions.get_product_by_id(product_id)
                product_name = product["name"] if product else product_id
                return {"success": True, "message": f"Updated {product_name} quantity to {quantity}"}
        
        return {"success": False, "message": "Product not found in cart"}
    
    def view_cart(self, user_id: str = "user123") -> Dict[str, Any]:
        """
        View current cart contents.
        
        Args:
            user_id: User ID
        
        Returns:
            Cart contents with product details and total
        """
        cart = self._load_cart(user_id)
        
        cart_items = []
        total = 0
        
        for item in cart.items:
            product = self.product_functions.get_product_by_id(item.product_id)
            if product:
                item_total = item.price * item.quantity
                total += item_total
                cart_items.append({
                    "product_id": item.product_id,
                    "name": product["name"],
                    "price": item.price,
                    "quantity": item.quantity,
                    "item_total": item_total
                })
        
        return {
            "items": cart_items,
            "total": total,
            "item_count": len(cart_items)
        }
    
    def clear_cart(self, user_id: str = "user123") -> Dict[str, Any]:
        """
        Clear all items from the cart.
        
        Args:
            user_id: User ID
        
        Returns:
            Status of the clear operation
        """
        cart = Cart(user_id=user_id, items=[])
        self._save_cart(cart)
        return {"success": True, "message": "Cart cleared"}
    
    def checkout(self, user_id: str = "user123") -> Dict[str, Any]:
        """
        Checkout the current cart and create an order.
        
        Args:
            user_id: User ID
        
        Returns:
            Order details if successful
        """
        cart = self._load_cart(user_id)
        
        if not cart.items:
            return {"success": False, "message": "Cart is empty"}
        
        # Create order items
        order_items = []
        total = 0
        
        for item in cart.items:
            # Check availability one more time
            availability = self.product_functions.check_product_availability(item.product_id, item.quantity)
            if not availability["available"]:
                return {"success": False, "message": f"Product {item.product_id} is no longer available in requested quantity"}
            
            order_item = {
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price": item.price
            }
            order_items.append(order_item)
            total += item.price * item.quantity
        
        # Generate order ID
        import uuid
        order_id = f"ORD{str(uuid.uuid4())[:6].upper()}"
        
        # Create order
        order = Order(
            id=order_id,
            user_id=user_id,
            items=order_items,
            total=total,
            status="pending",
            created_at=datetime.now().isoformat()
        )
        
        # Save order
        try:
            with open(self.orders_file, 'r') as f:
                orders_data = json.load(f)
        except FileNotFoundError:
            orders_data = []
        
        orders_data.append(order.to_dict())
        
        with open(self.orders_file, 'w') as f:
            json.dump(orders_data, f, indent=2)
        
        # Clear cart
        self.clear_cart(user_id)
        
        return {
            "success": True,
            "message": "Order placed successfully",
            "order_id": order_id,
            "total": total
        }

# Define function schemas for Gemini API
CART_FUNCTION_SCHEMAS = [
    {
        "name": "add_to_cart",
        "description": "Add a product to the shopping cart",
        "parameters": {
            "type": "object",
            "properties": {
                "product_id": {
                    "type": "string",
                    "description": "Product ID to add to cart"
                },
                "quantity": {
                    "type": "integer",
                    "description": "Quantity to add (default: 1)"
                },
                "user_id": {
                    "type": "string",
                    "description": "User ID (defaults to current user if not provided)"
                }
            },
            "required": ["product_id"]
        }
    },
    {
        "name": "remove_from_cart",
        "description": "Remove a product from the shopping cart",
        "parameters": {
            "type": "object",
            "properties": {
                "product_id": {
                    "type": "string",
                    "description": "Product ID to remove from cart"
                },
                "user_id": {
                    "type": "string",
                    "description": "User ID (defaults to current user if not provided)"
                }
            },
            "required": ["product_id"]
        }
    },
    {
        "name": "update_cart_quantity",
        "description": "Update the quantity of a product in the cart",
        "parameters": {
            "type": "object",
            "properties": {
                "product_id": {
                    "type": "string",
                    "description": "Product ID to update"
                },
                "quantity": {
                    "type": "integer",
                    "description": "New quantity"
                },
                "user_id": {
                    "type": "string",
                    "description": "User ID (defaults to current user if not provided)"
                }
            },
            "required": ["product_id", "quantity"]
        }
    },
    {
        "name": "view_cart",
        "description": "View current shopping cart contents",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "User ID (defaults to current user if not provided)"
                }
            }
        }
    },
    {
        "name": "clear_cart",
        "description": "Clear all items from the shopping cart",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "User ID (defaults to current user if not provided)"
                }
            }
        }
    },
    {
        "name": "checkout",
        "description": "Checkout the current cart and create an order",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "User ID (defaults to current user if not provided)"
                }
            }
        }
    }
]