import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
from models import Order

class OrderFunctions:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.orders_file = os.path.join(data_dir, "orders.json")
    
    def _load_orders(self) -> List[Order]:
        """Load orders from JSON file"""
        try:
            with open(self.orders_file, 'r') as f:
                orders_data = json.load(f)
            return [Order.from_dict(order) for order in orders_data]
        except FileNotFoundError:
            return []
    
    def _save_orders(self, orders: List[Order]):
        """Save orders to JSON file"""
        orders_data = [order.to_dict() for order in orders]
        with open(self.orders_file, 'w') as f:
            json.dump(orders_data, f, indent=2)
    
    def get_user_orders(self, user_id: str = "user123") -> List[Dict[str, Any]]:
        """
        Get all orders for a specific user.
        
        Args:
            user_id: User ID to get orders for
        
        Returns:
            List of user's orders
        """
        orders = self._load_orders()
        user_orders = [order.to_dict() for order in orders if order.user_id == user_id]
        return user_orders
    
    def track_order(self, order_id: str) -> Optional[Dict[str, Any]]:
        """
        Track a specific order by its ID.
        
        Args:
            order_id: The order ID to track
        
        Returns:
            Order details with status if found, None otherwise
        """
        orders = self._load_orders()
        for order in orders:
            if order.id == order_id:
                return {
                    "order_id": order.id,
                    "status": order.status,
                    "created_at": order.created_at,
                    "total": order.total,
                    "items": order.items,
                    "estimated_delivery": self._get_estimated_delivery(order.status, order.created_at)
                }
        return None
    
    def _get_estimated_delivery(self, status: str, created_at: str) -> str:
        """Get estimated delivery date based on order status"""
        status_messages = {
            "pending": "Order is being processed. Estimated delivery: 3-5 business days",
            "processing": "Order is being prepared. Estimated delivery: 2-4 business days", 
            "shipped": "Order has been shipped. Estimated delivery: 1-2 business days",
            "delivered": "Order has been delivered",
            "cancelled": "Order has been cancelled"
        }
        return status_messages.get(status, "Status unknown")
    
    def get_order_history(self, user_id: str = "user123", limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get order history for a user.
        
        Args:
            user_id: User ID
            limit: Maximum number of orders to return
        
        Returns:
            Recent orders for the user
        """
        orders = self.get_user_orders(user_id)
        # Sort by created_at descending
        orders.sort(key=lambda x: x['created_at'], reverse=True)
        return orders[:limit]

# Define function schemas for Gemini API
ORDER_FUNCTION_SCHEMAS = [
    {
        "name": "track_order",
        "description": "Track the status of a specific order using order ID",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The unique order ID to track (e.g., ORD001, ORD002)"
                }
            },
            "required": ["order_id"]
        }
    },
    {
        "name": "get_user_orders",
        "description": "Get all orders for a specific user",
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
        "name": "get_order_history",
        "description": "Get recent order history for a user",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "User ID (defaults to current user if not provided)"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of orders to return (default: 10)"
                }
            }
        }
    }
]