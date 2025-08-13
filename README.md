# WRTeam Sport Center - AI-Powered CLI Chatbot

A demonstration project showcasing **Gemini API function calling** in a conversational order management system for a sports equipment store. This CLI-based chatbot demonstrates how to integrate LLM-powered conversations with structured function calls for real-world business operations.

## 🎯 Project Goals

- **LLM + Function Tooling**: Demonstrate how Gemini API can intelligently call functions based on user intent
- **Conversational Commerce**: Show how natural language can drive e-commerce operations
- **Modular Architecture**: Create a scalable pattern for integrating AI with business logic
- **Demo Foundation**: Serve as a template for real-world applications (replace JSON files with API calls)

## ✨ Features

### 🔍 **Product Search**
- Natural language product search
- Filter by category, price range, brand
- Product availability checking
- Intelligent recommendations

### 🛒 **Cart Management**
- Add/remove products with conversation
- Update quantities naturally
- View cart with detailed breakdown
- Smart checkout process

### 📦 **Order Tracking**
- Track orders by ID or natural queries
- Order history and status updates
- Delivery estimations
- Order management

### 💬 **AI Assistant**
- Free-form conversation
- Context-aware responses
- Intent recognition
- Function calling based on user needs

### ❓ **Support & Help**
- Store information and policies
- Size guides and recommendations
- Issue reporting
- FAQ assistance

## 🏗️ Architecture

```
function_tooling/
├── models/          # Data models (Product, Order, Cart)
├── data/            # JSON files (products, orders, cart)
├── functions/       # Business logic functions
│   ├── product_functions.py
│   ├── order_functions.py
│   ├── cart_functions.py
│   └── support_functions.py
├── utils/           # Gemini API integration
│   └── gemini_client.py
├── cli.py           # CLI interface
└── main.py          # Entry point
```

### 🧠 **Function Calling Flow**

1. **User Input** → Natural language query
2. **Gemini API** → Analyzes intent and parameters
3. **Function Mapping** → Calls appropriate business function
4. **Data Processing** → Executes operation (search, add to cart, etc.)
5. **Response Generation** → AI formats result naturally
6. **User Output** → Conversational response with results

## 🚀 Setup & Installation

### Prerequisites
- Python 3.8+
- Gemini API Key ([Get one here](https://aistudio.google.com/app/apikey))

### Installation Steps

1. **Clone/Download the project**
   ```bash
   cd function_tooling
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API key**
   ```bash
   # Copy the example env file
   cp .env.example .env
   
   # Edit .env and add your Gemini API key
   GEMINI_API_KEY=your_actual_api_key_here
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

## 🎮 Usage Examples

### Product Search
```
You: "I need football equipment under $100"
AI: Searches products, filters by category and price, shows results
```

### Cart Operations
```
You: "Add 2 running shoes to my cart"
AI: Searches for running shoes, checks availability, adds to cart
```

### Order Tracking
```
You: "Where is my order ORD001?"
AI: Tracks order, shows status, provides delivery estimate
```

### Natural Conversation
```
You: "What's your return policy for cleats?"
AI: Provides return policy information specific to footwear
```

## 🛠️ Function Schemas

The project includes comprehensive function schemas for:

- **Product Functions**: search_products, get_product_by_id, check_product_availability
- **Order Functions**: track_order, get_user_orders, get_order_history  
- **Cart Functions**: add_to_cart, remove_from_cart, update_cart_quantity, view_cart, checkout
- **Support Functions**: get_help, get_store_info, report_issue, get_size_guide

Each function includes detailed parameter definitions and validation.

## 📊 Sample Data

The project includes realistic sample data:
- **8 Sports Products**: Football, baseball, tennis equipment and apparel
- **3 Sample Orders**: Different statuses (shipped, delivered, processing)
- **Empty Cart**: Ready for testing cart operations

## 🔧 Customization

### Adding New Functions
1. Create function in appropriate module (`functions/`)
2. Add function schema for Gemini API
3. Register in `utils/gemini_client.py`
4. Update CLI interface if needed

### Extending Data Models
1. Modify models in `models/product.py`
2. Update JSON data files in `data/`
3. Adjust function implementations

### Real-World Integration
Replace JSON file operations with:
- **Database queries** (PostgreSQL, MongoDB)
- **API calls** (REST, GraphQL)
- **External services** (payment, inventory)

## 🎯 Demo Scenarios

### Scenario 1: Product Discovery
- Search for "tennis equipment"
- Ask about specific product details
- Compare prices and features
- Add items to cart

### Scenario 2: Order Management
- Check order status
- View order history
- Track delivery updates

### Scenario 3: Customer Support
- Ask about return policies
- Get size recommendations
- Report issues
- Store information

## 🌟 Key Learning Points

1. **Intent Recognition**: How Gemini identifies when to call functions
2. **Parameter Extraction**: Automatic parsing of user input for function calls
3. **Context Maintenance**: Keeping conversation context across function calls
4. **Error Handling**: Graceful handling of function failures
5. **Natural Responses**: Converting function results into conversational replies

## 🚀 Future Enhancements

- **Multi-user Support**: User authentication and profiles
- **Real Database**: Replace JSON with PostgreSQL/MongoDB
- **Payment Integration**: Stripe/PayPal checkout
- **Inventory Management**: Real-time stock updates
- **Voice Interface**: Speech-to-text integration
- **Web Interface**: React/Vue.js frontend
- **Analytics**: Usage tracking and insights

## 📝 Technical Notes

- **Function Schemas**: Defined in OpenAPI-compatible format for Gemini
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Data Validation**: Input validation for all function parameters
- **Conversation Flow**: Maintains chat history for context
- **CLI Design**: Rich terminal UI with colors and formatting

## 🤝 Contributing

This is a demo project, but feel free to:
- Add new product categories
- Implement additional functions
- Improve error handling
- Enhance the CLI interface
- Add tests

## 📄 License

This project is for educational and demonstration purposes.

---

**Built with ❤️ to demonstrate the power of AI-driven function calling in conversational interfaces.**