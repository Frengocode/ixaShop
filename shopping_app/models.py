from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
from django_countries.fields import CountryField


class UserProfile(AbstractUser):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'ShopModel_USERProfile', null=True)
    user_profile_photo = models.ImageField(upload_to='profile_image/')
    groups = models.ManyToManyField('auth.Group', related_name='user_profiles')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='user_profiles_permissions')
    country = CountryField()
    

class ShopModel(models.Model):

    PRDOCUT_CATEGORY_CHOICES = [
        ('Техника', 'Техника'),
        ('Одежда', 'Одежда'),
        ('Бизнес', 'Бизнес'),
        ('Дом', 'Дом'),
        ('Машина', 'Машина')    
    ]

    SELE_PRODACTION = [

        ('ДА', 'ДА'),
        ('Нет', 'Нет')

    ]


    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'UploudProduct_UserProfile', null=True)
    
    product_title = models.CharField(verbose_name = 'Название Продукта  ', max_length=100)
    product_price = models.IntegerField(verbose_name = 'Цена Продукта ')
    litle = models.CharField(verbose_name = 'Описание Товара ',max_length=100)

    street_title = models.CharField(verbose_name = 'Насвание улицы ' ,max_length=100)
    product_category = models.CharField(max_length=100, verbose_name = 'Категория товара ', choices = PRDOCUT_CATEGORY_CHOICES)
    best_product = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_product', null=True)
    quantity = models.IntegerField(verbose_name='Количество Продукта ')
    sale = models.CharField(max_length=100,verbose_name='Отобразить ли товар в список скидочных товаров  ' , choices = SELE_PRODACTION)


    created_at = models.DateTimeField(auto_now_add = True)
    first_product_photo = models.ImageField(upload_to='first_product_image/', verbose_name='Первое фото обезательно ', blank=True)
    telephone_number = models.CharField(max_length=100)


    class Meta:
        ordering = ['-created_at']
    
class CommentModel(models.Model):

    REVIEW_COHICES = [
        ('⭐', '⭐'),
        ('⭐⭐', '⭐⭐'),
        ('⭐⭐⭐', '⭐⭐⭐' ),
        ('⭐⭐⭐⭐', '⭐⭐⭐⭐')

    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    product = models.ForeignKey(ShopModel, on_delete = models.CASCADE)
    text = models.CharField(max_length=100)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'users_can_paste_like_for_this_commnet')
    craeted_at = models.DateTimeField(auto_now_add = True)
    review = models.CharField(max_length=100, choices = REVIEW_COHICES ,verbose_name = 'Оцените товар ')


    class Meta:
        ordering = ['-craeted_at']


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(ShopModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} of {self.product}'
    
    class Meta:
        ordering = ['-created_at']
    
    
    