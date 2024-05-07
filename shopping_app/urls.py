from django.urls import path
from .views import (ProductList, 
                    LoginView,
                    UserRegisterView,
                    LogoutView, 
                    LikeProduct,
                    UserProfileView,
                    ProductUploudView, 
                    SearchView,
                    UserProfilePhotoView,
                    ProductDetailView, 
                    CommentrionView,
                    CartView, 
                    AddToCartView, 
                    CartDeleteView , 
                    UserProfileView,
                    UsernameUpdateView, 
                    PasswordChangeView,
                    UserProductsView,
                    UpdateProdcut,
                    SettingsView,
                    GetTexnikProducts,
                    ProductCategoryView,
                    GetHouseCategoryView,
                    GetCarCategoryView,
                    GetSeleProducts,
                    GetBuisnesProductsView,
                    DeleteProdcutView)


urlpatterns = [
    path('', ProductList.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('sign_up/', UserRegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('like_product<int:pk>/', LikeProduct.as_view(), name='like'),
    path('user_profile/', UserProfileView.as_view(), name='profile'),
    path('uploud_product/', ProductUploudView.as_view(), name='product_uploud'),
    path('search_product/', SearchView.as_view(), name='search'),
    path('photo_uploud/', UserProfilePhotoView.as_view(), name='profile_photo_uploud'),
    path('product_detail<int:pk>/', ProductDetailView.as_view(), name='product_info'),
    path('comment_view<int:pk>/', CommentrionView.as_view(), name='comment'),
    path('add-to-cart/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', CartView.as_view(), name='view_cart'),
    path('delete/<int:pk>/', CartDeleteView.as_view(), name='product_delete'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('change/', UsernameUpdateView.as_view(), name='username_change'),
    path('change_password/', PasswordChangeView.as_view(), name='password_change'),
    path('products/', UserProductsView.as_view(), name='user_products'),
    path('change_product/<int:pk>/', UpdateProdcut.as_view(), name='update_product'),
    path('settings/', SettingsView.as_view(), name='settings'),
    path('texnik/', GetTexnikProducts.as_view(), name='texnik_products'),
    path('product_with_category/', ProductCategoryView.as_view(), name='category_products'),
    path('get_houses_category/', GetHouseCategoryView.as_view(), name='house'),
    path('get_car_category/', GetCarCategoryView.as_view(), name='cars'),
    path('get_sele_products/', GetSeleProducts.as_view(), name='sele_prodcuts'),
    path('get_buisnes_products/', GetBuisnesProductsView.as_view(), name='buisnes_products'),
    path('product_delete/<int:pk>/', DeleteProdcutView.as_view(), name='delete')


















]