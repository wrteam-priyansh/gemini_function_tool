import os
import json
from typing import Dict, Any, List, Optional, Callable
from dotenv import load_dotenv
import google.generativeai as genai
from functions import (
    ProductFunctions, PRODUCT_FUNCTION_SCHEMAS,
    OrderFunctions, ORDER_FUNCTION_SCHEMAS,
    CartFunctions, CART_FUNCTION_SCHEMAS,
    SupportFunctions, SUPPORT_FUNCTION_SCHEMAS
)

load_dotenv()

class GeminiChatbot:
    def __init__(self, data_dir: str = "data"):
        # Initialize API
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=self.api_key)
        
        # Initialize function handlers
        self.product_functions = ProductFunctions(data_dir)
        self.order_functions = OrderFunctions(data_dir)
        self.cart_functions = CartFunctions(data_dir)
        self.support_functions = SupportFunctions()
        
        # Function mapping
        self.function_map = {
            # Product functions
            'search_products': self.product_functions.search_products,
            'get_product_by_id': self.product_functions.get_product_by_id,
            'check_product_availability': self.product_functions.check_product_availability,
            
            # Order functions
            'track_order': self.order_functions.track_order,
            'get_user_orders': self.order_functions.get_user_orders,
            'get_order_history': self.order_functions.get_order_history,
            
            # Cart functions
            'add_to_cart': self.cart_functions.add_to_cart,
            'remove_from_cart': self.cart_functions.remove_from_cart,
            'update_cart_quantity': self.cart_functions.update_cart_quantity,
            'view_cart': self.cart_functions.view_cart,
            'clear_cart': self.cart_functions.clear_cart,
            'checkout': self.cart_functions.checkout,
            
            # Support functions
            'get_help': self.support_functions.get_help,
            'get_store_info': self.support_functions.get_store_info,
            'report_issue': self.support_functions.report_issue,
            'get_size_guide': self.support_functions.get_size_guide,
        }
        
        # Create function declarations for Gemini (following official format)
        self.function_declarations = self._create_function_declarations()
        
        # Create model with tools (following official documentation)
        self.model = genai.GenerativeModel(
            model_name='gemini-1.5-pro',
            tools=[{'function_declarations': self.function_declarations}]
        )
        
        # System prompt
        self.system_prompt = """You are a helpful customer service assistant for WRTeam Sport Center, a sports equipment and apparel store.

Your capabilities include:
- Searching for products by name, category, or price range
- Adding products to cart and managing cart contents  
- Tracking orders and providing order history
- Providing customer support and help information
- Answering questions about store policies, shipping, returns, etc.

Key guidelines:
- Always be helpful, friendly, and professional
- Use the available functions to provide accurate, real-time information
- When customers ask about products, search the inventory using the search function
- For order inquiries, use the order tracking functions
- For cart operations, use the cart management functions
- Provide helpful suggestions and recommendations
- If you can't find what a customer is looking for, suggest alternatives or direct them to customer support

Store Information:
- Name: WRTeam Sport Center
- Specializes in sports equipment, apparel, and accessories
- Offers football, baseball, tennis, safety equipment, footwear, and athletic wear
- Free shipping on orders over $50
- 30-day return policy
- Customer service: support@wrteam.com, 1-800-WRTEAM"""
    
    def _create_function_declarations(self) -> List[Dict[str, Any]]:
        """Create function declaration dictionaries following official Gemini API format"""
        declarations = []
        
        # Product functions
        declarations.append({
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
        })
        
        declarations.append({
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
        })
        
        declarations.append({
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
        })
        
        declarations.append({
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
        })
        
        declarations.append({
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
        })
        
        declarations.append({
            "name": "get_help",
            "description": "Get help information on various topics like return policy, shipping, warranty, etc.",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string", 
                        "description": "Help topic (return_policy, shipping, warranty, size_guide, payment, contact)"
                    }
                }
            }
        })
        
        return declarations
    
    def chat(self, message: str, chat_history: Optional[List] = None) -> Dict[str, Any]:
        """
        Process a chat message and return response with function calls if needed.
        Following official Gemini API documentation pattern.
        
        Args:
            message: User message
            chat_history: Optional chat history for context
        
        Returns:
            Response with text and any function call results
        """
        try:
            # Start a chat session
            chat = self.model.start_chat(history=chat_history or [])
            
            # Add system prompt if this is a new conversation
            if not chat_history:
                system_response = chat.send_message(self.system_prompt)
            
            # Send the user message
            response = chat.send_message(message)
            
            function_results = []
            final_text = ""
            
            # Process the response
            if response.candidates and response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    # Check if this part contains a function call
                    if hasattr(part, 'function_call') and part.function_call:
                        func_call = part.function_call
                        func_name = func_call.name
                        
                        # Extract function arguments
                        func_args = {}
                        if func_call.args:
                            for key, value in func_call.args.items():
                                func_args[key] = value
                        
                        # Execute the function if it exists in our mapping
                        if func_name in self.function_map:
                            try:
                                result = self.function_map[func_name](**func_args)
                                function_results.append({
                                    'function': func_name,
                                    'args': func_args,
                                    'result': result
                                })
                                
                                # For now, let's format the result directly in text
                                # This approach works while we figure out the function response format
                                final_text = self._format_function_result(func_name, result)
                                
                            except Exception as e:
                                function_results.append({
                                    'function': func_name,
                                    'args': func_args,
                                    'error': str(e)
                                })
                                final_text = f"I encountered an error executing {func_name}: {str(e)}"
                        else:
                            final_text = f"Unknown function: {func_name}"
                    
                    elif hasattr(part, 'text') and part.text:
                        # Regular text response
                        final_text = part.text
            
            # If no text was set, use the response text directly
            if not final_text and hasattr(response, 'text'):
                final_text = response.text
            
            return {
                'text': final_text,
                'function_calls': function_results,
                'chat_history': chat.history
            }
            
        except Exception as e:
            return {
                'text': f"I apologize, but I encountered an error: {str(e)}. Please try again or contact our support team at support@wrteam.com.",
                'function_calls': [],
                'error': str(e)
            }
    
    def _format_function_result(self, func_name: str, result: Any) -> str:
        """Format function results into natural language responses"""
        if func_name == "search_products":
            if result:
                text = f"I found {len(result)} products matching your search:\n\n"
                for product in result[:3]:  # Show top 3 results
                    text += f"🏷️ **{product['name']}** (ID: {product['id']})\n"
                    text += f"   💰 ${product['price']} | 📦 {product['stock']} in stock\n"
                    text += f"   📝 {product['description']}\n\n"
                
                if len(result) > 3:
                    text += f"... and {len(result) - 3} more products.\n\n"
                
                text += "To add any item to your cart, just tell me:\n• 'Add [PRODUCT_ID] to cart' (e.g., 'Add BALL001 to cart')\n• Or I'll ask you after showing the results!"
                return text
            else:
                return "I couldn't find any products matching your search. Please try different search terms or browse our categories: Football, Baseball, Tennis, Apparel, Footwear, Safety equipment."
        
        elif func_name == "add_to_cart":
            if result.get('success'):
                return f"✅ {result['message']}\n\nWould you like to view your cart or continue shopping?"
            else:
                return f"❌ {result['message']}\n\nPlease check the product ID and try again."
        
        elif func_name == "view_cart":
            if result['items']:
                text = f"🛒 **Your Cart** ({result['item_count']} items):\n\n"
                for item in result['items']:
                    text += f"• {item['name']} (ID: {item['product_id']})\n"
                    text += f"  Quantity: {item['quantity']} × ${item['price']} = ${item['item_total']:.2f}\n\n"
                text += f"**Total: ${result['total']:.2f}**\n\n"
                text += "💡 **Next steps:**\n• Tell me 'Checkout my cart' when ready\n• Continue shopping to add more items\n• Ask me to 'Remove [PRODUCT_ID] from cart' to remove items"
                return text
            else:
                return "🛒 Your cart is empty. Browse our products and add some items!"
        
        elif func_name == "track_order":
            if result:
                text = f"📦 **Order {result['order_id']}**\n"
                text += f"Status: {result['status'].upper()}\n"
                text += f"Total: ${result['total']:.2f}\n"
                text += f"Created: {result['created_at']}\n"
                text += f"{result['estimated_delivery']}\n\n"
                text += "**Items:**\n"
                for item in result['items']:
                    text += f"• Product {item['product_id']}: {item['quantity']} × ${item['price']}\n"
                return text
            else:
                return "❌ Order not found. Please check the order ID and try again."
        
        elif func_name == "get_user_orders":
            if result:
                text = f"📋 **Your Orders** ({len(result)} orders):\n\n"
                for order in result:
                    text += f"• **{order['id']}** - ${order['total']:.2f} - {order['status'].upper()}\n"
                text += "\nTo track a specific order, just tell me the order ID (like ORD001)."
                return text
            else:
                return "You don't have any orders yet. Start shopping to place your first order!"
        
        elif func_name == "get_help":
            if result.get('topic'):
                return f"**{result['topic'].replace('_', ' ').title()} Information:**\n{result['information']}\n\n{result.get('additional_help', '')}"
            else:
                text = "🏪 **WRTeam Sport Center Help**\n\nAvailable topics:\n"
                for topic in result.get('available_topics', []):
                    text += f"• {topic.replace('_', ' ').title()}\n"
                return text
        
        # Default formatting
        return str(result)
    
    def get_available_functions(self) -> List[str]:
        """Get list of available function names"""
        return list(self.function_map.keys())