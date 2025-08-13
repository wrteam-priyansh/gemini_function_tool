import os
import sys
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich import print as rprint
from utils import GeminiChatbot

class WRTeamCLI:
    def __init__(self):
        self.console = Console()
        self.chatbot = None
        self.chat_history = []
        self.current_user = "user123"  # Single user for demo
        
    def initialize_chatbot(self) -> bool:
        """Initialize the Gemini chatbot with API key check"""
        try:
            self.chatbot = GeminiChatbot()
            return True
        except ValueError as e:
            self.console.print(f"[red]Error: {e}[/red]")
            self.console.print("[yellow]Please set your GEMINI_API_KEY in a .env file[/yellow]")
            return False
        except Exception as e:
            self.console.print(f"[red]Error initializing chatbot: {e}[/red]")
            return False
    
    def show_welcome(self):
        """Display welcome message and store info"""
        welcome_text = Text()
        welcome_text.append("Welcome to ", style="bold blue")
        welcome_text.append("WRTeam Sport Center", style="bold red")
        welcome_text.append(" AI Assistant!", style="bold blue")
        
        panel = Panel(
            welcome_text,
            title="🏆 Sports Equipment Store",
            title_align="center",
            border_style="blue",
            padding=(1, 2)
        )
        
        self.console.print(panel)
        
        # Store info
        store_info = """
🏪 Your one-stop shop for sports equipment and apparel
⚽ Football • ⚾ Baseball • 🎾 Tennis • 👕 Apparel • 👟 Footwear
📞 1-800-WRTEAM | 📧 support@wrteam.com
🚚 Free shipping on orders over $50 | 📅 30-day returns
        """
        self.console.print(Panel(store_info, border_style="green"))
    
    def show_main_interface(self):
        """Display the simple conversational interface"""
        self.console.print("\n[bold cyan]💬 What can I help you with today?[/bold cyan]")
        self.console.print("You can:")
        self.console.print("• 🔍 [bold]Search products[/bold] - 'Find football equipment' or 'Show me running shoes'")
        self.console.print("• 📦 [bold]Track orders[/bold] - 'Track my orders' or 'Where is order ORD001?'")
        self.console.print("• 🛒 [bold]Cart operations[/bold] - 'Show my cart' or 'Add BALL001 to cart'")
        self.console.print("• ❓ [bold]Get help[/bold] - 'What's your return policy?' or 'Store hours?'")
        self.console.print("• Type '[bold red]exit[/bold red]' to quit\n")
    
    
    def display_chat_response(self, response):
        """Display chatbot response in a formatted way"""
        if response.get('text'):
            self.console.print(f"\n[bold blue]🤖 WRTeam Assistant:[/bold blue]")
            self.console.print(Panel(response['text'], border_style="blue", padding=(0, 1)))
        
        # Show function calls if any (for debugging)
        if response.get('function_calls') and os.getenv('DEBUG'):
            self.console.print(f"\n[dim]Function calls: {len(response['function_calls'])}[/dim]")
        
        if response.get('error'):
            self.console.print(f"[red]Error: {response['error']}[/red]")
    
    def run(self):
        """Main CLI loop - Simple conversational interface"""
        # Clear screen and show welcome
        os.system('clear' if os.name == 'posix' else 'cls')
        self.show_welcome()
        
        # Initialize chatbot
        if not self.initialize_chatbot():
            return
        
        self.console.print("[green]✅ AI Assistant ready![/green]")
        
        # Simple conversational loop
        while True:
            try:
                self.show_main_interface()
                
                user_input = Prompt.ask("[bold green]You[/bold green]")
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    self.console.print("\n[bold green]Thanks for shopping with WRTeam Sport Center! 🏆[/bold green]")
                    break
                
                # Process user input through the chatbot
                response = self.chatbot.chat(user_input, self.chat_history)
                self.display_chat_response(response)
                
                # Update chat history
                if response.get('chat_history'):
                    self.chat_history = response['chat_history']
                
                # Only ask about adding to cart if we searched for products and found results
                if self._should_ask_add_to_cart(response):
                    add_to_cart = Confirm.ask("\n💡 Would you like to add any item to your cart?")
                    if add_to_cart:
                        product_id = Prompt.ask("Enter the product ID")
                        quantity = Prompt.ask("Enter quantity", default="1")
                        
                        cart_response = self.chatbot.chat(f"Add product {product_id} to cart, quantity {quantity}")
                        self.display_chat_response(cart_response)
                        
                        # Update chat history after cart operation
                        if cart_response.get('chat_history'):
                            self.chat_history = cart_response['chat_history']
                
                # Add a separator for better readability
                self.console.print("\n" + "─" * 80)
                    
            except KeyboardInterrupt:
                self.console.print("\n\n[yellow]Exiting... Thanks for shopping with WRTeam! 👋[/yellow]")
                break
            except Exception as e:
                self.console.print(f"\n[red]An error occurred: {e}[/red]")
                if not Confirm.ask("Continue?"):
                    break
    
    def _should_ask_add_to_cart(self, response) -> bool:
        """Check if we should ask about adding items to cart"""
        if not response.get('function_calls'):
            return False
        
        # Only ask if we called search_products and found results
        for call in response['function_calls']:
            if (call.get('function') == 'search_products' and 
                call.get('result') and 
                len(call.get('result', [])) > 0):
                return True
        
        return False

def main():
    """Entry point for the CLI application"""
    cli = WRTeamCLI()
    cli.run()

if __name__ == "__main__":
    main()