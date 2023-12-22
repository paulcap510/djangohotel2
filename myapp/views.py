from django.shortcuts import render, redirect
from .models import Room, Reservation, Guest
from datetime import datetime
from django.shortcuts import get_object_or_404

# Create your views here.
def index(request):
    return render(request, 'index.html')

def results(request):
    checkin_date = request.GET.get('checkin_date')
    checkout_date = request.GET.get('checkout_date')
    guests = int(request.GET.get('guests'))  
    checkin_date = datetime.strptime(checkin_date, '%Y-%m-%d').date()
    checkout_date = datetime.strptime(checkout_date, '%Y-%m-%d').date()

    request.session['search_criteria'] = {
        'checkin_date': checkin_date.strftime('%Y-%m-%d'),
        'checkout_date': checkout_date.strftime('%Y-%m-%d'),
        'guests': guests
    }

    booked_rooms = Reservation.objects.filter(
        checkin_date__lt=checkout_date, 
        checkout_date__gt=checkin_date
    ).values_list('room', flat=True)

    all_rooms = Room.objects.filter(max_guests__gte=guests).exclude(id__in=booked_rooms)
    unique_room_types = {}

    for room in all_rooms:
        if room.type not in unique_room_types:
            unique_room_types[room.type] = room

    if request.method == 'POST':
        selected_room_id = request.POST.get('selected_room_id')
        request.session['reservation_details'] = {
            'selected_room_id': selected_room_id,
            'checkin_date': checkin_date.strftime('%Y-%m-%d'),
            'checkout_date': checkout_date.strftime('%Y-%m-%d'),
            'guests': guests
        }
        return redirect('reserve_room', room_id=selected_room_id)

    return render(request, 'results.html', {'rooms': unique_room_types.values()})



def reserve_room(request, room_id):
    # get search criteria from sessions data
    search_criteria = request.session.get('search_criteria', {})
    checkin_date = search_criteria.get('checkin_date')
    checkout_date = search_criteria.get('checkout_date')
    guests = search_criteria.get('guests')

    # get room details
    room = get_object_or_404(Room, pk=room_id)

    context = {
        'room': room,
        'checkin_date': checkin_date,
        'checkout_date': checkout_date,
        'guests': guests
    }
    return render(request, 'reserve_room.html', context)




def confirm_reservation(request):
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        cc_no = request.POST.get('TEST_cc_no')
        cc_exp = request.POST.get('TEST_cc_exp')

        # get reservation from the session
        search_criteria = request.session.get('search_criteria', {})
        checkin_date = search_criteria.get('checkin_date')
        checkout_date = search_criteria.get('checkout_date')

        checkin_date = datetime.strptime(checkin_date, '%Y-%m-%d').date()
        checkout_date = datetime.strptime(checkout_date, '%Y-%m-%d').date()

        guest = Guest(firstname=firstname, lastname=lastname, email=email, phone=phone)
        guest.save()

        room = get_object_or_404(Room, pk=room_id)

        reservation = Reservation(
            room=room,
            customer=guest,
            checkin_date=checkin_date,
            checkout_date=checkout_date,
            TEST_cc_no=cc_no,
            TEST_cc_exp=cc_exp
        )
        reservation.save()

        context = {
            'reservation': reservation
        }
        return render(request, 'confirm_reservation.html', context)
    return redirect('home')
