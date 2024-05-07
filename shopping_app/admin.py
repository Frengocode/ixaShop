from django.contrib import admin
from .models import UserProfile, ShopModel, CommentModel, Cart, CartItem

admin.site.register(UserProfile)
admin.site.register(ShopModel)
admin.site.register(CommentModel)
admin.site.register(Cart)
admin.site.register(CartItem)

