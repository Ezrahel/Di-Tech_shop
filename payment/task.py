from io import BytesIO
from celery import shared_task
# from weasyprint import HTML, CSS


from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order
import pdfkit


@shared_task
def payment_completed(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    order = Order.objects.get(id=order_id)
    # create invoice e-mail
    subject = f'My Shop - EE Invoice no. {order.id}'
    message = 'Please, find attached the invoice for your recent purchase.'
    email = EmailMessage(subject,
                         message,
                         'adelakinisrael024@gmail.com',
                         [order.email])
    # generate PDF
    html = render_to_string('orders/order/invoice.html', {'order': order})

    # Generate the PDF file from the HTML content
    config = pdfkit.configuration(wkhtmltopdf='/opt/bin/wkhtmltopdf')
    pdf = pdfkit.from_string(html, False, configuration=config)

    # Attach the PDF file to the email
    email.attach(f'order_{order.id}.pdf', pdf, 'application/pdf')
    # send e-mail
    email.send()
