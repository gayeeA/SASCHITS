# from django.shortcuts import render
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from .models import Subscriber, ChitGroup, Payment
from django.template.defaultfilters import date
from django.core.exceptions import ValidationError
import datetime 
from datetime import datetime
from datetime import date
from django.db.models import Sum
from . import models
from .forms import DateForm
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from num2words import num2words
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def base(request):
    return render(request, 'base.html')

def home(request):
    return render(request, 'home.html')

# Chit Group Views
def list_chit_groups(request):
    chit_groups = ChitGroup.objects.all()
    return render(request, 'list_chit_groups.html', {'chit_groups': chit_groups})

def add_chit_group(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        total_amount = request.POST.get('total_amount')
        installment_amount = request.POST.get('installment_amount')
        months = request.POST.get('months')
        members_count = request.POST.get('members_count')

        try:
            # Backend processing: Remove commas for storage
            clean_total_amount = Decimal(total_amount.replace(',', ''))
            clean_installment_amount = Decimal(installment_amount.replace(',', ''))

            # Save the chit group
            chit_group = ChitGroup(
                group_name=group_name,
                total_amount=clean_total_amount,
                installment_amount=clean_installment_amount,
                months=int(months),
                members_count=int(members_count)
            )
            chit_group.full_clean()  # Validate model fields
            chit_group.save()

            return redirect('list_chit_groups')  # Replace with your actual URL name
        except ValidationError as e:
            return render(request, 'add_chit_group.html', {'errors': e.messages})
        except Exception as e:
            return render(request, 'add_chit_group.html', {'errors': [str(e)]})

    return render(request, 'add_chit_group.html')

def edit_chit_group(request, id):
    chit_group = ChitGroup.objects.get(id=id)
    if request.method == 'POST':
        chit_group.group_name = request.POST['group_name']
        chit_group.total_amount = request.POST['total_amount']
        chit_group.installment_amount = request.POST['installment_amount']
        chit_group.months = request.POST['months']
        chit_group.members_count = request.POST['members_count']
        chit_group.save()
        return redirect('/chit_groups/')
    return render(request, 'edit_chit_group.html', {'chit_group': chit_group})



def delete_chit_group(request, id):
    chit_group = get_object_or_404(ChitGroup, id=id)
    if request.method == 'POST':
        chit_group.delete()
        return redirect('list_chit_groups')
    # Redirect for non-POST requests (GET)
    return redirect('list_chit_groups')


# Subscriber Views
def list_subscribers(request):
    subscribers = Subscriber.objects.all()
    return render(request, 'list_subscribers.html', {'subscribers': subscribers})

def add_subscriber(request):
    if request.method == 'POST':
        chit_group = ChitGroup.objects.get(id=request.POST['group_name'])
        try:
           chit_group = ChitGroup.objects.get(id=request.POST['group_name'])
        except ChitGroup.DoesNotExist:
           return render(request, 'add_subscriber.html', {'error': 'Chit Group does not exist.'})
        # Subscriber.group_name = chit_group
        Subscriber.objects.create(
            name=request.POST['name'],
            phone=request.POST['phone'],
            address=request.POST['address'],
            email=request.POST['email'],
            group_name=chit_group,   
            ticket_number=request.POST['ticket_number']
        )
        return redirect('/subscribers/')
    chit_groups = ChitGroup.objects.all()
    return render(request, 'add_subscriber.html', {'chit_groups': chit_groups})

def edit_subscriber(request, id):
    subscriber = Subscriber.objects.get(id=id)
    chit_groups = ChitGroup.objects.all()  # Fetch chit groups for the dropdown
    if request.method == 'POST':
        # Retrieve selected group and handle the submission
        chit_group = ChitGroup.objects.get(id=request.POST['group_name'])
        subscriber.name = request.POST['name']
        subscriber.phone = request.POST['phone']
        subscriber.address = request.POST['address']
        subscriber.email = request.POST['email']
        subscriber.group_name = chit_group  # Update the group name
        subscriber.ticket_number = request.POST['ticket_number']
        subscriber.save()  # Save the updated subscriber
        return redirect('/subscribers/')

    return render(request, 'edit_subscriber.html', {'subscriber': subscriber, 'chit_groups': chit_groups})

def delete_subscriber(request, id):
    subscriber = get_object_or_404(Subscriber, id=id)
    if request.method == 'POST':
        subscriber.delete()
        return redirect('list_subscribers')
    # Redirect for non-POST requests (GET)
    return redirect('list_subscribers')


# # Payment Views
def list_payments(request):
    specific_date = date.today()  # Default to today

    # Handle form submission
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            specific_date = form.cleaned_data['specific_date']
    else:
        form = DateForm()

    # Get the payments for the selected date
    payments = models.Payment.objects.filter(payment_date=specific_date)
    
    # Calculate the total payment collected on that specific date
    total_payment = payments.aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    # Manually format the payment date
    for payment in payments:
        payment.payment_date = payment.payment_date.strftime("%d-%m-%Y")

    return render(request, 'list_payments.html', {
        'payments': payments,
        'total_payment': total_payment,
        'specific_date': specific_date,
        'form': form
    })

def add_payment(request):
    if request.method == 'POST':
        # Retrieve form data
        subscriber_id = request.POST.get('subscriber')
        chit_group_id = request.POST.get('chit_group')
        amount = request.POST.get('amount')
        payment_date = request.POST.get('payment_date')
        payment_mode = request.POST.get('payment_mode')  # New field
        installment_number = request.POST.get('installment_number')  # New field
        installment_month = request.POST.get('installment_month')  # New field
        arrears = request.POST.get('arrears') or 0
        future_dues = request.POST.get('future_dues') or 0
        interest_penalty = request.POST.get('interest_penalty') or 0
        other_charges = request.POST.get('other_charges') or 0
        dividend_allowed = request.POST.get('dividend_allowed') or 0
        dividend_forfeited = request.POST.get('dividend_forfeited') or 0
        cheque_details = request.POST.get('cheque_details') or "N/A"
        receiving_clerk_name = request.POST.get('receiving_clerk_name')

        # Convert amount to words
        amount_in_words = num2words(float(amount), to='currency', lang='en_IN')

        # Get Subscriber and Chit Group details
        subscriber = Subscriber.objects.get(id=subscriber_id)
        chit_group = ChitGroup.objects.get(id=chit_group_id)

        # Generate payment receipt as PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="payment_receipt_{subscriber_id}.pdf"'

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)

        styles = getSampleStyleSheet()
        elements = []

        # Header Section
        header_data = [
            ["SRI ANDESIVAIAH CHITS PRIVATE LIMITED"],
            ["Regd. Office: #18-8-22/9E, Madhura Nagar, TIRUPATI-517501"]
        ]
        header_table = Table(header_data, colWidths=[500])
        header_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 14),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 12))

        # Payment Information
        payment_data = [
            ["Sl.No.", "Group Name", "Date", "Payment Mode"],
            ["11272", chit_group.group_name, payment_date, payment_mode]
        ]
        payment_table = Table(payment_data, colWidths=[80, 200, 120, 100])
        payment_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))
        elements.append(payment_table)
        elements.append(Spacer(1, 12))

        # Subscriber Information
        subscriber_data = [
            ["Received with thanks from Sri/Smt.", subscriber.name],
        ]
        subscriber_table = Table(subscriber_data, colWidths=[200, 300])
        subscriber_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ]))
        elements.append(subscriber_table)
        elements.append(Spacer(1, 12))

        # Installment Details
        installment_data = [
            ["Installment No.", "Month", "Current", "Arrears", "Future", "Interest Penalty", "Others", "Total"],
            [installment_number, datetime.strptime(installment_month, "%Y-%m-%d").strftime("%b-%Y"), f"₹{amount}", f"₹{arrears}", f"₹{future_dues}", f"₹{interest_penalty}", f"₹{other_charges}",  f"₹{float(amount) + float(arrears) + float(future_dues) + float(interest_penalty) + float(other_charges)}"]
        ]
        installment_table = Table(installment_data, colWidths=[80, 80, 70, 70, 70, 80, 80, 80])
        installment_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))
        elements.append(installment_table)
        elements.append(Spacer(1, 12))
        # Total Amount in Words (placed above Dividends Allowed section)
        total_amount = (
            float(amount) + float(arrears) + float(future_dues) +
            float(interest_penalty) + float(other_charges)
        )
        total_in_words = num2words(total_amount, to='currency', lang='en_IN', currency='INR')
        # elements.append(Paragraph(f"Total Amount in Words: {total_in_words}", styles['Normal']))
        # elements.append(Spacer(1, 12))
        total_in_words_data = [
             [f"Total Amount in Words: {total_in_words}"]
        ]

        total_in_words_table = Table(total_in_words_data, colWidths=[500])  # Adjust width as needed
        total_in_words_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # Border around the cell
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Align text to the left
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),  # Bold font
            ('FONTSIZE', (0, 0), (-1, -1), 10),  # Font size
            ('BACKGROUND', (0, 0), (-1, -1), colors.whitesmoke),  # Optional background color
            ('PADDING', (0, 0), (-1, -1), 6),  # Padding inside the cell
        ]))
        elements.append(total_in_words_table)
        elements.append(Spacer(1, 12))
        # Additional Information
        additional_data = [
            ["Dividends Allowed", "Forfeited", "UPI RRN", "Cheque Particulars"],
            [f"₹{dividend_allowed}", f"₹{dividend_forfeited}", "N/A", cheque_details],
            ["Receiving Clerk:", receiving_clerk_name, "", "Manager: A. Sivaiah"]
        ]
        additional_table = Table(additional_data, colWidths=[120, 120, 120, 160])
        additional_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))
        elements.append(additional_table)

        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        response.write(buffer.read())
        return response

    # Render form for adding payment
    chit_groups = ChitGroup.objects.all()
    group_subscribers = {group.id: list(Subscriber.objects.filter(group_name=group)) for group in chit_groups}
    payments = Payment.objects.all()

    return render(request, 'add_payment.html', {
        'chit_groups': chit_groups,
        'group_subscribers': group_subscribers,
        'payments': payments,
    })


def edit_payment(request, id):
    """Edit an existing payment"""
    payment = get_object_or_404(Payment, id=id)
    if request.method == 'POST':
        # Get and validate the input
        subscriber_id = request.POST['subscriber']
        chit_group_id = request.POST['chit_group']
        amount = request.POST['amount']
        payment_date_str = request.POST['payment_date']

        # Validate the date format
        try:
            payment_date = datetime.datetime.strptime(payment_date_str, '%Y-%m-%d').date()
        except ValueError:
            return render(request, 'edit_payment.html', {'payment': payment, 'subscribers': Subscriber.objects.all(), 'chit_groups': ChitGroup.objects.all(), 'error_message': 'Invalid date format. Please use YYYY-MM-DD.'})

        # Update payment details
        payment.subscriber_id = subscriber_id
        payment.chit_group_id = chit_group_id
        payment.amount = amount
        payment.payment_date = payment_date
        payment.save()

        return redirect('list_payments')  # Redirect to the payment list view
    return render(
        request, 
        'edit_payment.html', 
        {
            'payment': payment, 
            'subscribers': Subscriber.objects.all(), 
            'chit_groups': ChitGroup.objects.all()
        }
    )
def delete_payment(request, id):
    payment = get_object_or_404(Payment, id=id)

    if request.method == 'POST':
        payment.delete()  # Deletes the payment
        return redirect('list_payments')  # Redirect to the list of payments

    return render(
        request,
        'delete_payment.html',
        {'payment': payment}  # Pass payment info to confirmation page
    )