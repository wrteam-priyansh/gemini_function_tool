from typing import Dict, Any, List

class SupportFunctions:
    def __init__(self):
        self.faq = {
            "return_policy": "You can return items within 30 days of purchase with original receipt. Items must be in original condition.",
            "shipping": "We offer free shipping on orders over $50. Standard shipping takes 3-5 business days.",
            "warranty": "All sports equipment comes with a 1-year manufacturer warranty. Apparel has a 90-day warranty.",
            "size_guide": "Please check our size guide on the product page. We offer exchanges for wrong sizes within 14 days.",
            "payment": "We accept major credit cards, PayPal, and store credit. Payment is processed securely.",
            "contact": "You can reach us at support@wrteam.com or call 1-800-WRTEAM during business hours 9AM-6PM EST."
        }
        
        self.store_info = {
            "name": "WRTeam Sport Center",
            "hours": "Monday-Saturday: 9AM-9PM, Sunday: 10AM-6PM",
            "phone": "1-800-WRTEAM",
            "email": "support@wrteam.com",
            "address": "123 Sports Avenue, Athletic City, AC 12345",
            "website": "www.wrteam.com"
        }
    
    def get_help(self, topic: str = "") -> Dict[str, Any]:
        """
        Get help information on various topics.
        
        Args:
            topic: Help topic (return_policy, shipping, warranty, size_guide, payment, contact)
        
        Returns:
            Help information
        """
        if topic.lower() in self.faq:
            return {
                "topic": topic,
                "information": self.faq[topic.lower()],
                "additional_help": "For more specific questions, contact our support team."
            }
        
        # Return all available topics if no specific topic requested
        return {
            "available_topics": list(self.faq.keys()),
            "faq": self.faq,
            "message": "Here are the help topics available. Ask about any specific topic for detailed information."
        }
    
    def get_store_info(self) -> Dict[str, Any]:
        """
        Get store contact information and details.
        
        Returns:
            Store information
        """
        return self.store_info
    
    def report_issue(self, issue_type: str, description: str) -> Dict[str, Any]:
        """
        Report an issue or problem.
        
        Args:
            issue_type: Type of issue (order, product, website, other)
            description: Description of the issue
        
        Returns:
            Issue report confirmation
        """
        import uuid
        ticket_id = f"TICKET{str(uuid.uuid4())[:8].upper()}"
        
        return {
            "success": True,
            "ticket_id": ticket_id,
            "issue_type": issue_type,
            "status": "submitted",
            "message": f"Your issue has been submitted. Ticket ID: {ticket_id}. Our support team will contact you within 24 hours.",
            "next_steps": "Check your email for updates or contact us at support@wrteam.com with your ticket ID."
        }
    
    def get_size_guide(self, category: str = "") -> Dict[str, Any]:
        """
        Get size guide information for different product categories.
        
        Args:
            category: Product category (footwear, apparel, equipment)
        
        Returns:
            Size guide information
        """
        size_guides = {
            "footwear": {
                "sizes": ["6", "7", "8", "9", "10", "11", "12", "13"],
                "guide": "Measure your foot length in inches. Add 0.5 inches for comfort.",
                "tips": "Try shoes in the evening when feet are slightly swollen for best fit."
            },
            "apparel": {
                "sizes": ["XS", "S", "M", "L", "XL", "XXL"],
                "guide": {
                    "XS": "Chest: 32-34 inches",
                    "S": "Chest: 35-37 inches", 
                    "M": "Chest: 38-40 inches",
                    "L": "Chest: 41-43 inches",
                    "XL": "Chest: 44-46 inches",
                    "XXL": "Chest: 47-49 inches"
                },
                "tips": "Measure around the fullest part of your chest for accurate sizing."
            },
            "equipment": {
                "guide": "Equipment sizes vary by sport. Check individual product pages for specific sizing information.",
                "tips": "Consider your skill level and playing style when choosing equipment sizes."
            }
        }
        
        if category.lower() in size_guides:
            return {
                "category": category,
                "size_info": size_guides[category.lower()]
            }
        
        return {
            "available_categories": list(size_guides.keys()),
            "all_guides": size_guides,
            "message": "Size guides available for footwear, apparel, and equipment."
        }

# Define function schemas for Gemini API
SUPPORT_FUNCTION_SCHEMAS = [
    {
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
    },
    {
        "name": "get_store_info",
        "description": "Get store contact information, hours, and location details",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "report_issue",
        "description": "Report an issue or problem to customer support",
        "parameters": {
            "type": "object",
            "properties": {
                "issue_type": {
                    "type": "string",
                    "description": "Type of issue (order, product, website, other)"
                },
                "description": {
                    "type": "string",
                    "description": "Detailed description of the issue"
                }
            },
            "required": ["issue_type", "description"]
        }
    },
    {
        "name": "get_size_guide",
        "description": "Get size guide information for different product categories",
        "parameters": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "Product category (footwear, apparel, equipment)"
                }
            }
        }
    }
]