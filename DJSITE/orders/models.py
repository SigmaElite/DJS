from django.db import models
from main.models import ClothingItem, Size
from django.conf import settings


class Order(models.Model):
    STATUS_CHOICES = [  
        ('pending', 'Pending'), # 1 отобр в бд, 2 в админке
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)#связ с A_U_M
    first_name = models.CharField(max_length=40)# b=T поле может быть пустым(необязат для заполн)
    last_name = models.CharField(max_length=40)
    middle_name = models.CharField(max_length=40)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=40)
    house_number = models.CharField(max_length=10)
    apartment_number = models.CharField(max_length=10)
    postal_code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    tracking_number = models.CharField(max_length=40, blank=True, default='Pending') #d=Pen чтоб в профиле авто вывод трек номер, после заказа чтоб было знач ожид заказа в админке на трекномер

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending') #ch статусы которые пропис выше


    def __str__(self):
        return f'Order {self.id} from {self.first_name} {self.last_name}' #так будет отбр заказ
    
    class Meta:
        verbose_name = 'Order' 
        verbose_name_plural = 'Orders'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    clothing_item = models.ForeignKey(ClothingItem, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return f'{self.quantity} x {self.clothing_item} ({self.size})'
    
    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'