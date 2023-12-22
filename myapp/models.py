from django.db import models
import uuid

class Room(models.Model):

    TYPES = [
        ('Twin', 'Twin'),
        ('King', 'King'),
        ('Suite', 'Suite')
    ]
    room_no = models.IntegerField(unique=True)
    type = models.CharField(max_length=20, choices=TYPES)
    price = models.IntegerField()
    max_guests = models.IntegerField()
    image = models.ImageField(upload_to='room_images/', blank=True, null=True)

    def __str__(self):
        return f"Room: {self.room_no}, {self.type}"
    
class Guest(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)

class Reservation(models.Model):
    ## uuid field can be used as an alternative, but using the method below allows for incremental counting 
    # reservation_no = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)    
    reservation_no = models.IntegerField(unique=True, editable=False)    

    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    customer = models.ForeignKey(Guest, on_delete=models.CASCADE)
    checkin_date = models.DateField()
    checkout_date = models.DateField()

    TEST_cc_no = models.CharField(max_length=20)
    TEST_cc_exp = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        if not self.id:  
            last_reservation = Reservation.objects.all().order_by('reservation_no').last()
            if last_reservation:
                self.reservation_no = last_reservation.reservation_no + 1
            else:
                self.reservation_no = 100001  
        super(Reservation, self).save(*args, **kwargs)

    def __str__(self):
        return f"Reservation {self.reservation_no} - {self.room.type} for {self.customer.firstname} {self.customer.lastname}"

 