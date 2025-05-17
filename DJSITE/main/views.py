from django.views.generic import ListView, DetailView #убрали рендер т.к пишем классовые представл 
from .models import ClothingItem, Category, Size, ClothingItemSize
from django.db.models import Q #это для выполн поиска и фильтрации

class CatalogView(ListView):
     #предсиавл для каталога
     model = ClothingItem
     template_name = 'main/product/list.html'
     context_object_name = 'clothing_items' #c_o_n указ под каким именем список товаров (ClothingItem) можно обратиться в шаблоне list.html


     def get_queryset(self):
          queryset = super().get_queryset()#здесь просто список товаров из моей бд которым можно манипулировать как угодно, ниже делаем переменные для дальнейшей фильтрации в нашем каталоге по неким параметрам
          category_slugs = self.request.GET.getlist('category') #здесь фильтр по категориям, получаем их в списки через getlist('category')
          size_names = self.request.GET.getlist('size')#получ размеры одежды
          min_price = self.request.GET.get('min_price')
          max_price = self.request.GET.get('max_price')
          search_query = self.request.GET.get('q')
   
          if category_slugs:
               queryset = queryset.filter(category__slug__in=category_slugs)#c__s__in функц которая фильтрует категории котор выбраны в cat_slugs

          if size_names:
               queryset = queryset.filter(
                    Q(sizes__name__in=size_names) & Q(sizes__clothingitemsize__available=True)# & этот знак означ and а q для сложной фильтр и ток с ним можно юзать такие знаки, 1 выбраны ли в фильтрации размеры,  2 проверка доступности товара в этом размере
               ).distinct()  #изза distinct будет вывод ток один товар при выборе нескольки размеров

          if min_price:
               queryset = queryset.filter(price__gte=min_price)# будет показ все что gte больше или равно цене указанной(Greater than or equal), Оставляет товары цена которых ≥ min_price
          
          if max_price:
               queryset = queryset.filter(price__lte=max_price)# будет показ все что меньше или равно цене указанной(Less Than or Equal) 

          if search_query:
               queryset = queryset.filter(
                    Q(name__icontains=search_query) |
                    Q(description__icontains=search_query)
               ).distinct()
         
          return queryset
     
     def get_context_data(self, **kwargs):  #тут функц которая будет отправл контекст в шаблон, kwargs это способ передать в функцию любое количество именованных аргументов (ключ-значение)
          context = super().get_context_data(**kwargs)#context это массив данных из бд(контекста) квагрс чтоб можно было созд скок угодно именнованых аргументов, т.е формирует баз контекст
          context['categories'] = Category.objects.all() #тут созд контекст для всех категорий т.е ключ-знач 
          context['sizes'] = Size.objects.all()  #достаём все доступные размеры из бд
          context['selected_categories'] = self.request.GET.getlist('category')#getlist возвращает список(несколько) значений для параметра из URL в () то что хотим получ из юрла, а не одно значение
          context['selected_sizes'] = self.request.GET.getlist('size')
          context['min_price'] = self.request.GET.get('min_price', '')#метод get это способ получить значение(одно) параметра из URL-адреса, указ '' потому что по дефолту не будет сортировки
          context['max_price'] = self.request.GET.get('max_price', '')

          return context #при обращ к контескту сможем получ данные которые передали выше в гет_кверисет
     

class ClothingItemDetailView(DetailView):
     model = ClothingItem
     template_name = 'main/product/detail.html'
     context_object_name = 'clothing_item'
     slug_field = 'slug'#указ какое поле модели юзать для поиска объекта.
     slug_url_kwarg = 'slug'#указ какое имя параметра в URL содержит slug

     def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          clothing_item = self.object  #получ товар выбранный на стр(которая открыта)
          available_sizes = ClothingItemSize.objects.filter(clothing_item=clothing_item, available=True) #cl_i=cl_i мы в этот(которыйчуть выше) кл айтем заосываем знач из бд
          context['available_sizes'] = available_sizes
          return context