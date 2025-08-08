from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from booking.models import Performance, Session, Hall, SeatCategory, Booking, Seat

from datetime import datetime

def performance_list(request):
    performances = Performance.objects.all()
    title_query = request.GET.get('title', '')
    date_query = request.GET.get('date', '')
    if title_query:
        performances = performances.filter(title__icontains=title_query)
    if date_query:
        try:
            date = datetime.strptime(date_query, '%Y-%m-%d').date()    
            performances = Performance.objects.filter(session__date=date).distinct()
        except ValueError:
            pass
    paginator = Paginator(performances, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'title_query': title_query,
        'date_query': date_query
    }
    return render(request, 'booking/performance_list.html', context)

def performance_detail(request, performance_id):
    performance = Performance.objects.get(id=performance_id)
    try:
        sessions = Session.objects.filter(performance=performance)
        paginator = Paginator(sessions, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except Session.DoesNotExist:
        page_obj = []
    
    return render(request, 'booking\performance_detail.html', {
        'performance': performance,
        'sessions': page_obj,
    })

def session_detail(request, session_id):
    session = Session.objects.get(id=session_id)
    hall = session.hall
    seats = Seat.objects.filter(hall=hall).select_related('category')
    booked_seats = Booking.objects.filter(session=session).values_list('seat_id', flat=True)

    seats_with_prices = []
    for seat in seats:
        price = session.get_price_for_seat(seat)
        seats_with_prices.append({
            'seat': seat,
            'price': price
        })
    
    seating = []
    row = []
    for i, item in enumerate(seats_with_prices, 1):
        row.append(item)
        if i % 10 == 0:
            seating.append(row)
            row = []
    if row:
        seating.append(row)  


    if request.method == 'POST':
        seat_id = request.POST.get('seat_id')
        seat = Seat.objects.get(id=seat_id)

        # перевірка чи не заброньовано вже
        if Booking.objects.filter(session=session, seat=seat).exists():
            messages.error(request, "Це місце вже зайняте!")
        else:
            price = session.get_price_for_seat(seat)
            Booking.objects.create(
                user=request.user,
                session=session,
                seat=seat,
                price_paid=price
            )
            messages.success(request, "Успішно заброньовано!")
            return redirect('session_detail', session_id=session.pk)

    context = {
        'session': session,
        'hall': hall,
        'seating': seating, 
        'booked_seats': list(booked_seats),
    }
    return render(request, 'booking/session_detail.html', context)
