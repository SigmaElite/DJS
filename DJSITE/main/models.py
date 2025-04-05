from django.db import models


class Size(models.Model): #созд табл бд(поля бд)
    name = models.CharField(max_length=10, unique=True)#CF текст поле дефолт, unique=True чтоб не было повт размеров что два объекта не могут иметь один name

    def __str__(self):  #тут как оно будет отбр в админке(стр этим занимается) а мета как отобр в бд
        return self.name 


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)#уникальность тру чтоб не было одинаковых товаров
    slug = models.SlugField(unique=True)#slug юзают для созд человекопонятных URL, unique=True чтоб два объекта не могли иметь один slug

    def __str__(self):  #тут как оно будет отбр в админке(стр этим занимается) а мета как отобр в бд
        return self.name
    
    class Meta: #переопред назв и некоторые параметры в бд
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]  #индексы для поиска
        verbose_name = 'category'
        verbose_name_plural = 'categories'

class ClothingItem(models.Model): #модель самого продукта   
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)#будем переходить для подробных характеристик товара
    available = models.BooleanField(default=True)#доступность товара на сайте, есть или нету
    sizes = models.ManyToManyField(Size, through='ClothingItemSize',  #through указ как к нему в будущ можно обращ, rel_name как будет в бд отобр, blank=True говорит что поле можно оставить пустым необязат выбир размер товара
                                   related_name='clothing_item', blank=True)#MTMF означ что у каждлго размера может быть сколько угодно товара и у каждого товара скока угодно размера, наследуем модель сайз т.к у товара будут размеры))  
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='clothing_items')#on_del при удалении категории удалим все товары которые в нее входят
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)#дата созд товара, a_n_a это автодобавл даты после созд товара, n=T что в бд могло быть как на ноль(пустым)
    updated_at = models.DateTimeField(auto_now=True)#дата когда товар был ласт раз изм, a_n=T чтобы авто поменялось
    price = models.DecimalField(max_digits=20, decimal_places=2)#m_d колво цифр до запятой то есть макс целое число, DF позволяет работать с палвающей точкой ис обычными а также для работы со скидками, d_p=2 будет два нолика после всех вычислений
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    

    def __str__(self):
        return self.name
    
    def get_price_with_discount(self):
        if self.discount > 0:
            return self.price * (1 - (self.discount / 100))
        return self.price
    


class ClothingItemSize(models.Model):#здесь делаем связь всего с товаром(сделали соотношение самого товара(одежды) и его размера)
    clothing_item = models.ForeignKey(ClothingItem, on_delete=models.CASCADE)#берём модель товара
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)#это для того чтобы на опред товаре могли делать доступными или не доступными размеры


    class Meta:
        unique_together = ('clothing_item', 'size')#для каждого товара уникальынй размер и наоборот. Например, нельзя дважды добавить размер "XL" для товара "Футболка