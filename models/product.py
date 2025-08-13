from dataclasses import dataclass
from typing import List, Optional
import json

@dataclass
class Product:
    id: str
    name: str
    category: str
    price: float
    description: str
    stock: int
    brand: str
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'price': self.price,
            'description': self.description,
            'stock': self.stock,
            'brand': self.brand
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

@dataclass
class Order:
    id: str
    user_id: str
    items: List[dict]  # [{"product_id": str, "quantity": int, "price": float}]
    total: float
    status: str  # pending, processing, shipped, delivered, cancelled
    created_at: str
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'items': self.items,
            'total': self.total,
            'status': self.status,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

@dataclass
class CartItem:
    product_id: str
    quantity: int
    price: float
    
    def to_dict(self):
        return {
            'product_id': self.product_id,
            'quantity': self.quantity,
            'price': self.price
        }

@dataclass
class Cart:
    user_id: str
    items: List[CartItem]
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'items': [item.to_dict() for item in self.items]
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        items = [CartItem(**item) for item in data.get('items', [])]
        return cls(user_id=data['user_id'], items=items)
    
    def get_total(self) -> float:
        return sum(item.price * item.quantity for item in self.items)