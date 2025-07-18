from django.shortcuts import render
from django.core.paginator import Paginator
from booking.models import Performance, Session, Hall, SeatCategory

def performance_list(request):
    performances = Performance.objects.all()
    paginator = Paginator(performances, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'booking\performance_list.html', {'page_obj': page_obj})

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

