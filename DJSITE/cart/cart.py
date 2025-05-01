#здесь будет весь функционал корзины
from django.conf import settings
from main.models import ClothingItem

class Cart:
    def __init__(self, request):#метод инициализации, self — это ссылка на текущий экземпляр корзины (например, cart)и будет рабоатть именоо в этой функц для именно этого экземп а не для всех. self.cart — это словарь, который хранит все товары в корзине.
        self.session = request.session  #тут получ сессию юзера у каждого будет своя сессия ниже пропис
        cart = self.session.get(settings.CART_SESSION_ID) #Мы пытаемся получить данные корзины из сессии по ключу settings.CART_SESSION_ID
        if not cart:  #если корзина пуста
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart #self.cart — это словарь, который хранит данные о товарах в корзине. Наконец, мы сохр ссылку на корзину (пустую или существующую) в атрибуте объекта self.cart


    def add(self, clothing_item, size, quantity=1): #этот метод вызов только при добавл в корзину, q=1 Добавляется 1 единица товара
        item_id = str(clothing_item.id)#id товара
        if item_id not in self.cart:
            self.cart[item_id] = {'quantity': 0, 'size': size}  
        self.cart[item_id]['quantity'] = quantity #Устанавл новое знач кол-ва товара в корзине.
        self.save()


    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart 
        self.session.modified = True


    def remove(self, clothing_item):
        item_id = str(clothing_item.id)
        if item_id in self.cart:
            del self.cart[item_id]   
            self.save()

    def get_total_price(self): #общ стоимость корзины
        total = 0 
        for item_id, item_date in self.cart.items():
            try:
                clothing_item = ClothingItem.objects.get(id=item_id)#получ объекты по их айдишнику
                total += clothing_item.get_price_with_discount() * item_date['quantity']#если колво один то ниче а если больше то умнож на колво тех самых товаров, item_data['quantity'] — это значение, которое хранит количество товара в корзине.
            except ClothingItem.DoesNotExist: #если какойто товар не будет найден в корзин то он не будет отправлен в общ стоимость
                continue
        return total
    

    def __iter__(self):
        item_ids = self.cart.keys()#keys возвращ item_id(все айди товаров в корзине)
        items = ClothingItem.objects.filter(id__in=item_ids)#заснули сюда токо те товары которые есть в корзине
        for item in items:
            total_price = item.get_price_with_discount()
            quantity = self.cart[str(item.id)]['quantity']#self.cart[str(item.id)] — это словарь, содержащий информацию о товаре в корзине. 'quantity' — это ключ, который хранит количество товара.
            yield {
                'item': item,
                'quantity': quantity,
                'size' : self.cart[str(item.id)]['size'],
                'total_price': total_price * quantity,
            }


    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())#проход именно по quan чтоб не было ошибки
    

    def clear(self):  #полная очистка корзины
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True # используется для явного указания Django, что данные сессии изменились.