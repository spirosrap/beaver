"""
Customer-Facing Output Generator for Munder Difflin Multi-Agent System

This module generates transparent and explainable outputs for customer interactions
while maintaining privacy and not revealing sensitive internal information.
"""

from typing import Dict, Optional
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine

# Create database connection
db_engine = create_engine("sqlite:///munder_difflin.db")

class CustomerOutputGenerator:
    """
    Generates customer-facing outputs that are:
    1. Transparent and explainable
    2. Include rationale for decisions
    3. Don't reveal sensitive internal information
    """
    
    def __init__(self):
        self.db_engine = db_engine
    
    def generate_customer_quote(self, 
                              item_name: str, 
                              quantity: int, 
                              unit_price: float, 
                              total_price: float,
                              available_stock: int,
                              request_date: str,
                              bulk_discount_applied: bool = False,
                              delivery_date: Optional[str] = None) -> str:
        """
        Generate a customer-facing quote response.
        """
        # Format the date for customer display
        request_date_obj = datetime.strptime(request_date, "%Y-%m-%d")
        formatted_date = request_date_obj.strftime("%B %d, %Y")
        
        # Build the customer response
        response_parts = []
        
        # Quote header
        response_parts.append(f"Thank you for your inquiry on {formatted_date}.")
        response_parts.append(f"\nQUOTE SUMMARY:")
        response_parts.append(f"• Item: {item_name}")
        response_parts.append(f"• Quantity: {quantity:,}")
        response_parts.append(f"• Unit Price: ${unit_price:.2f}")
        
        # Add bulk discount explanation if applicable
        if bulk_discount_applied:
            original_total = unit_price * quantity
            discount_amount = original_total - total_price
            response_parts.append(f"• Bulk Discount: ${discount_amount:.2f} (10% off orders over 500 units)")
            response_parts.append(f"• Total Price: ${total_price:.2f}")
        else:
            response_parts.append(f"• Total Price: ${total_price:.2f}")
        
        # Add stock availability information
        if available_stock >= quantity:
            response_parts.append(f"\nAVAILABILITY: In stock and ready for immediate fulfillment.")
            response_parts.append(f"Your order can be processed immediately.")
        else:
            response_parts.append(f"\nAVAILABILITY: Limited stock available.")
            response_parts.append(f"We currently have {available_stock:,} units in stock.")
            if delivery_date:
                delivery_date_obj = datetime.strptime(delivery_date, "%Y-%m-%d")
                formatted_delivery = delivery_date_obj.strftime("%B %d, %Y")
                response_parts.append(f"We are placing a restock order to fulfill your complete request.")
                response_parts.append(f"Expected delivery date: {formatted_delivery}")
        
        # Add pricing rationale
        response_parts.append(f"\nPRICING INFORMATION:")
        if bulk_discount_applied:
            response_parts.append(f"• Standard pricing applies to all orders")
            response_parts.append(f"• Bulk discount of 10% applied for orders exceeding 500 units")
            response_parts.append(f"• This reflects our commitment to competitive pricing for larger orders")
        else:
            response_parts.append(f"• Standard pricing applies to your order")
            response_parts.append(f"• Bulk discounts available for orders exceeding 500 units")
        
        # Add delivery information
        response_parts.append(f"\nDELIVERY:")
        if available_stock >= quantity:
            response_parts.append(f"• Standard delivery: 3-5 business days")
            response_parts.append(f"• Rush delivery available upon request")
        else:
            response_parts.append(f"• Partial fulfillment available immediately")
            response_parts.append(f"• Complete order delivery upon restock")
        
        response_parts.append(f"\nThank you for choosing Munder Difflin Paper Company!")
        response_parts.append(f"If you have any questions, please don't hesitate to contact us.")
        
        return "\n".join(response_parts)
    
    def generate_customer_decline(self, 
                                 item_name: str, 
                                 quantity: int, 
                                 available_stock: int,
                                 request_date: str,
                                 reason: str = "insufficient_stock") -> str:
        """
        Generate a customer-facing decline response.
        """
        request_date_obj = datetime.strptime(request_date, "%Y-%m-%d")
        formatted_date = request_date_obj.strftime("%B %d, %Y")
        
        response_parts = []
        response_parts.append(f"Thank you for your inquiry on {formatted_date}.")
        response_parts.append(f"\nWe regret to inform you that we are unable to fulfill your request at this time.")
        
        if reason == "insufficient_stock":
            response_parts.append(f"\nREASON: Insufficient inventory")
            response_parts.append(f"• Requested: {quantity:,} units of {item_name}")
            response_parts.append(f"• Currently available: {available_stock:,} units")
            response_parts.append(f"• We apologize for any inconvenience this may cause")
        
        response_parts.append(f"\nALTERNATIVES:")
        response_parts.append(f"• We can fulfill a partial order of {available_stock:,} units")
        response_parts.append(f"• We can place a special order for future delivery")
        response_parts.append(f"• We can suggest alternative products with similar specifications")
        
        response_parts.append(f"\nPlease contact our customer service team to discuss these options.")
        response_parts.append(f"Thank you for your understanding.")
        
        return "\n".join(response_parts)
    
    def generate_customer_confirmation(self, 
                                     item_name: str, 
                                     quantity: int, 
                                     total_price: float,
                                     order_number: str,
                                     request_date: str) -> str:
        """
        Generate a customer-facing order confirmation.
        """
        request_date_obj = datetime.strptime(request_date, "%Y-%m-%d")
        formatted_date = request_date_obj.strftime("%B %d, %Y")
        
        response_parts = []
        response_parts.append(f"ORDER CONFIRMATION")
        response_parts.append(f"Date: {formatted_date}")
        response_parts.append(f"Order Number: {order_number}")
        response_parts.append(f"\nORDER DETAILS:")
        response_parts.append(f"• Item: {item_name}")
        response_parts.append(f"• Quantity: {quantity:,}")
        response_parts.append(f"• Total Amount: ${total_price:.2f}")
        
        response_parts.append(f"\nSTATUS: Order confirmed and being processed")
        response_parts.append(f"• Your order has been successfully placed")
        response_parts.append(f"• You will receive a shipping confirmation within 24 hours")
        response_parts.append(f"• Expected delivery: 3-5 business days")
        
        response_parts.append(f"\nThank you for your business!")
        response_parts.append(f"We appreciate your trust in Munder Difflin Paper Company.")
        
        return "\n".join(response_parts)

def create_customer_facing_outputs(results_data: list) -> list:
    """
    Convert internal system outputs to customer-facing outputs.
    
    Args:
        results_data: List of dictionaries containing internal system results
        
    Returns:
        List of dictionaries with customer-facing outputs
    """
    generator = CustomerOutputGenerator()
    customer_outputs = []
    
    for result in results_data:
        # Parse the internal response to extract information
        internal_response = result['response']
        
        # Extract basic information
        request_id = result['request_id']
        request_date = result['request_date']
        
        # Parse the internal response to get details
        if "Quote: $" in internal_response:
            # Extract quote information
            quote_start = internal_response.find("Quote: $") + 8
            quote_end = internal_response.find(".", quote_start)
            total_price = float(internal_response[quote_start:quote_end])
            
            # Extract item and quantity information
            if "Quoted" in internal_response:
                quoted_part = internal_response.split("Quoted")[1].split("at")[0].strip()
                quantity = int(quoted_part.split("x")[0].strip())
                item_name = quoted_part.split("x")[1].strip()
                
                # Extract unit price
                unit_price_part = internal_response.split("at $")[1].split(" each")[0]
                unit_price = float(unit_price_part)
                
                # Check if bulk discount was applied
                bulk_discount = "Bulk discount applied" in internal_response
                
                # If bulk discount was applied, recalculate the original price
                if bulk_discount:
                    # The total_price is already discounted, so original would be total_price / 0.9
                    original_total = total_price / 0.9
                    discount_amount = original_total - total_price
                
                # Check if order was fulfilled or declined
                if "Processed sale" in internal_response:
                    # Order was fulfilled
                    customer_response = generator.generate_customer_quote(
                        item_name=item_name,
                        quantity=quantity,
                        unit_price=unit_price,
                        total_price=total_price,
                        available_stock=quantity,  # If processed, we had enough stock
                        request_date=request_date,
                        bulk_discount_applied=bulk_discount
                    )
                elif "Insufficient stock" in internal_response:
                    # Order was declined due to insufficient stock
                    # Extract available stock from response
                    if "Only" in internal_response and "available" in internal_response:
                        stock_part = internal_response.split("Only ")[1].split(" available")[0]
                        available_stock = int(stock_part)
                    else:
                        available_stock = 0
                    
                    # Check if this is a bulk discount case that should still show the quote
                    if bulk_discount:
                        # Even with insufficient stock, show the quote with bulk discount
                        customer_response = generator.generate_customer_quote(
                            item_name=item_name,
                            quantity=quantity,
                            unit_price=unit_price,
                            total_price=total_price,
                            available_stock=available_stock,
                            request_date=request_date,
                            bulk_discount_applied=bulk_discount
                        )
                    else:
                        customer_response = generator.generate_customer_decline(
                            item_name=item_name,
                            quantity=quantity,
                            available_stock=available_stock,
                            request_date=request_date
                        )
                else:
                    # Some other case
                    customer_response = "We apologize, but we encountered an issue processing your request. Please contact our customer service team for assistance."
            else:
                customer_response = "We apologize, but we encountered an issue processing your request. Please contact our customer service team for assistance."
        else:
            customer_response = "We apologize, but we encountered an issue processing your request. Please contact our customer service team for assistance."
        
        customer_outputs.append({
            'request_id': request_id,
            'request_date': request_date,
            'customer_response': customer_response,
            'internal_status': 'processed'
        })
    
    return customer_outputs

def save_customer_outputs(customer_outputs: list, filename: str = "customer_outputs.csv"):
    """
    Save customer-facing outputs to a CSV file.
    """
    df = pd.DataFrame(customer_outputs)
    df.to_csv(filename, index=False)
    print(f"Customer-facing outputs saved to {filename}")
    return filename 