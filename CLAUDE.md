# CLAUDE.md - Project Context for Claude Code

This file provides context for Claude Code to better understand and work with the WRTeam Sport Center project.

## Project Overview
**WRTeam Sport Center** is a CLI-based AI chatbot that demonstrates Gemini API function calling for conversational order management. It serves as a proof-of-concept for integrating LLM-powered conversations with structured business operations.

## Key Technologies
- **Python 3.8+**
- **Google Gemini API** (gemini-1.5-pro) for function calling
- **Rich** library for CLI interface
- **JSON files** for data persistence (demo purposes)

## Architecture Pattern
The project follows a **function-driven conversational AI** pattern:
1. User provides natural language input
2. Gemini API analyzes intent and extracts parameters
3. Business functions execute operations
4. AI generates natural language responses

## Core Components

### Data Models (`models/`)
- `Product`: Sports equipment and apparel
- `Order`: Customer orders with status tracking
- `Cart`: Shopping cart management
- All models use dataclasses with JSON serialization

### Business Functions (`functions/`)
- `ProductFunctions`: Search, availability checking
- `OrderFunctions`: Tracking, history
- `CartFunctions`: Add/remove items, checkout
- `SupportFunctions`: Help, store info, issue reporting

### API Integration (`utils/`)
- `GeminiChatbot`: Main class handling Gemini API
- Function schema definitions for API
- Chat history management
- Error handling

### CLI Interface (`cli.py`)
- Menu-driven interface with Rich formatting
- Conversation modes
- Error handling and user feedback

## Function Calling Schema
Each business function includes:
- OpenAPI-compatible parameter definitions
- Required/optional parameter specifications
- Type validation
- Description for AI understanding

## Development Patterns

### Adding New Functions
1. Implement function in appropriate `functions/` module
2. Add function schema with parameters
3. Register in `GeminiChatbot.function_map`
4. Update CLI interface if needed

### Data Management
- JSON files in `data/` directory
- Single user system (`user123`) for demo
- Atomic operations for data consistency

### Error Handling
- Graceful API failures
- User-friendly error messages
- Fallback responses for function errors

## Testing Strategy
- Manual testing through CLI interface
- Function-level testing possible
- API key required for full testing

## Common Tasks

### Running the Application
```bash
python main.py
```

### Environment Setup
```bash
pip install -r requirements.txt
cp .env.example .env
# Add GEMINI_API_KEY to .env
```

### Debugging
Set `DEBUG=1` environment variable to see function call details

## File Structure Context

### Critical Files
- `main.py`: Entry point
- `cli.py`: Main CLI interface
- `utils/gemini_client.py`: Core AI integration
- `functions/`: All business logic

### Data Files
- `data/products.json`: 8 sample sports products
- `data/orders.json`: 3 sample orders with different statuses
- `data/cart.json`: Empty cart for testing

### Configuration
- `requirements.txt`: Python dependencies
- `.env.example`: API key template
- `README.md`: User documentation

## Development Notes
- This is a **demo project** showing function calling patterns
- Real-world implementation would replace JSON with databases/APIs
- Single-user system for simplicity
- Focus on conversational AI integration over production features

## Extension Points
- Multi-user authentication
- Real database integration
- Payment processing
- Inventory management
- Web interface
- Voice recognition

## Common Issues
- Missing API key: Check `.env` file
- Import errors: Ensure all dependencies installed
- Function call failures: Check parameter validation
- CLI crashes: Rich library compatibility

This project demonstrates the power of combining conversational AI with structured business operations through function calling.