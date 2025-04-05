from django.contrib import admin
from .models import Size, Category, ClothingItem, ClothingItemSize 


class ClothingItemSizeInline(admin.TabularInline):  #это нужно для того чтобы на стр самого товара можно было дабвл неогрнич колво размеров по желанию(скок размеров будет сток и добавл можно)
    model = ClothingItemSize
    extra = 4 # ← появиться 4 строки для выбора для новых размеров(например при редактировании какогото товара)


@admin.register(Size)#декоратор регистр добавл модель в админку
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)#l_d позвол указ поля которые заданы в модели для отобр их в админке
    search_fields = ('name',) #это параметр по которому будет осуществл поиск в самой админке поиск именно по этим моделям

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}#pr_f это означ автозаполн параметра slug юзаем для генерации юрла и будем его ген из назв самого товара( {'slug': ('name')} )
    search_fields = ('name',)

@admin.register(ClothingItem)    
class ClothingItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category', 
                    'available', 'price', 'discount',
                    'created_at', 'updated_at',)#в каком порядке впис поля так они и будут располог в админке
    list_filter = ('available', 'category')#параметр для фильтрации
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('-created_at',)#ord это метод фильтрации когда в админке зайдём в список товаров будет идти от самым новых к самым старым поэтому поставили -
    inlines = [ClothingItemSizeInline]#для того чтоб в адимнке могли добавл наши размеры товара
