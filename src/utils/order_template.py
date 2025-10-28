"""This module contains the function for the order email template."""

from src.utils.constants import OrderStatus, PaymentMethod, PaymentStatus


def order_email_template(order, user, cancelled_due_to_stock=False):
    order_status_enum = OrderStatus(int(order.order_status))
    order_status = order_status_enum.name  # This will give CONFIRMED or CANCELLED value
    is_confirmed = (
        order_status_enum == OrderStatus.CONFIRMED
    )  # This will check if the status is CONFIRMED or not
    payment = order.payments
    payment_method = PaymentMethod(int(payment.payment_method)).name
    total_amount = payment.amount

    product_rows = ""
    for history in order.order_histories:
        name = history.subproducts.products.name
        qty = history.order_quantity
        price = history.subproducts.price
        product_rows += f"""
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #ccc;">{name}</td>
                <td style="padding: 10px; border-bottom: 1px solid #ccc;">{qty}</td>
                <td style="padding: 10px; border-bottom: 1px solid #ccc;">₹{price}</td>
            </tr>
        """

    if is_confirmed:
        message = "<p style='font-size: 10pt;'>We’re pleased to confirm your order. Please find the invoice details below:</p>"
    else:
        if cancelled_due_to_stock:
            message = f"""
            <p style='font-size: 10pt;'>
                We regret to inform you that your order placed on {order.created_at.strftime('%Y-%m-%d')}, has been cancelled due to insufficient stock availability for one or more items in your orderlist.
                <br><br>
                A full refund has been initiated with refund ID <strong >{payment.refund_id}</strong>. It will be processed within <strong>7 business days</strong>.
                <br><br>
                If you need further assistance our support team is here to help.
                <br><br>
            </p>
            """
        else:
            message = f"""
            <p style='font-size: 10pt;'>
                Your order placed on {order.created_at.strftime('%Y-%m-%d')} has been successfully cancelled as per your request.
                <br><br>
                A full refund has been initiated with refund ID <strong>{payment.refund_id}</strong>. It will be processed within <strong>7 business days</strong>.
                <br><br>
                If you need further assistance our support team is here to help.
            </p>
            """

    html = f"""
    <div style="font-family: 'Book Antiqua', Palatino, serif; color: #333; padding: 30px; background-color: #f9f9f9; border: 1px solid #ddd; max-width: 600px; margin: auto;">
        <div style="text-align: center; margin-bottom: 30px;">
            <h2 style="margin: 0; font-size: 24pt; background-color:#748C70; color:white; padding:8px">Urban Stitch</h2>
            <p style="margin: 5px 0; font-size: 10pt; color: #666;">Thank you for shopping with us!</p>
        </div>

        <p style="font-size: 12pt;">Hello <strong>{user.first_name} {user.last_name}</strong>,</p>
        {message}

        <table style="width: 100%; border-collapse: collapse; margin-top: 20px; font-size: 10pt;">
            <tr><td><strong>Order ID:</strong></td><td>{order.id}</td></tr>
            <tr><td><strong>Email:</strong></td><td>{user.email}</td></tr>
            <tr><td><strong>Shipping Address:</strong></td><td>{user.address} {user.landmark} {user.city} {user.state} {user.country} {user.pincode}</td></tr>
            <tr><td><strong>Order status:</strong></td><td>{order_status}</td></tr>
            <tr><td><strong>Payment mode:</strong></td><td>{payment_method}</td></tr>
            <tr><td><strong>Transaction ID:</strong></td><td>{payment.transaction_id}</td></tr>
        </table>

        <h3 style="margin-top: 30px; font-size: 14pt;">Order Summary</h3>
        <table style="width: 100%; border-collapse: collapse; font-size: 10pt; margin-top:10px;">
            <tr>
                <th style="text-align: left; padding: 10px; border-bottom: 2px solid #ccc;">Product Name</th>
                <th style="text-align: left; padding: 10px; border-bottom: 2px solid #ccc;">Quantity</th>
                <th style="text-align: left; padding: 10px; border-bottom: 2px solid #ccc;">Price</th>
            </tr>
            {product_rows}
        </table>

        <p style="text-align: right; font-weight: bold; font-size: 11pt; margin-top: 20px; padding-right:50px">Total: ₹{total_amount}</p>
        <p style="margin-top: 20px;">Best regards,<br><strong>Urban Stitch Team</strong></p>
        <p style="font-size: 10pt; margin-top: 20px;">Thank you for choosing <strong>Urban Stitch</strong>.</p>
    </div>
    """
    return html
