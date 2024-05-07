from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import  login, logout, authenticate, update_session_auth_hash
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, DetailView, UpdateView
from django.views import View
from .models import (UserProfile,
                      ShopModel,
                        CommentModel,
                          Cart,
                            CartItem)


from .forms import (UserRegisterForm
                    , SerachProductForm
                    , ProfilePhotoUploudForm,
                      ProductUploudForm,
                        CommentForm,
                          ProfileUpdateForm,
                            PasswordChangeForm)

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpRequest
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class GetSeleProducts(TemplateView):
    template_name = 'category_products/sele.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sale'] = ShopModel.objects.filter(sale = 'ДА')
        return context


class GetCarCategoryView(TemplateView):
    template_name = 'category_products/cars.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cars'] = ShopModel.objects.filter(product_category = 'Машина')
        return context
        



class ProductCategoryView(TemplateView):
    template_name = 'category_products/all_category.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        return render(request, self.template_name)



class SettingsView(TemplateView):
    template_name = 'pages/settings.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        return render(request, self.template_name)



class UserProductsView(TemplateView):
    template_name = 'pages/user_products.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwrags):
        context = super().get_context_data(**kwrags)
        user = self.request.user
        context['products'] = ShopModel.objects.filter(user=user)
        return context

class UpdateProdcut(UpdateView):
    model = ShopModel
    form_class = ProductUploudForm
    template_name = 'uplouds/product_change.html'
    success_url = reverse_lazy('user_profile')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        return queryset.filter(user=user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if not user.is_authenticated:
            return redirect('home') 
        context['form'] = ProductUploudForm(user=user, instance=self.object)
        return context  
    

class GetBuisnesProductsView(TemplateView):
    template_name = 'category_products/buisnes.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['buisnes'] = ShopModel.objects.filter(product_category = 'Бизнес')
        return context
    


class GetHouseCategoryView(TemplateView):
    template_name = 'category_products/house.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['houses'] = ShopModel.objects.filter(product_category ='Дом')
        return context


class SettingsView(TemplateView):
    template_name = 'pages/settings.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwrags):
        return render(request, self.template_name)
    


class UsernameUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'changes/profile_update_view.html'
    model = UserProfile
    form_class = ProfileUpdateForm
    success_url = reverse_lazy('user_profile')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        return self.request.user
    


class PasswordChangeView(TemplateView):

    form_class = PasswordChangeForm
    template_name = 'changes/password_change.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, *kwargs)
    
    def get(self, request):
        form = self.form_class(request.user)
        return render(request, self.template_name, {'form':form} )
    
    def post(self, request):
        
        form = self.form_class(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, '')
            return redirect('user_profile')

        return render(request, self.template_name, {'form':form})



class CartDeleteView(View):

    @method_decorator(login_required)
    def dispatch(self, request, *args, pk:int, **kwargs):
        return super().dispatch(request, *args, pk, **kwargs)

    def get(self, request, pk:int):
        cart_item = CartItem.objects.get(id=pk)
        
        if request.user == cart_item.cart.user:
            cart_item.delete()

        return redirect('view_cart')
    
    
        

class AddToCartView(View):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwrags):
        return super().dispatch(request, *args, **kwrags)

    def get(self, request, product_id):
        if request.user.is_authenticated:
            product = ShopModel.objects.get(id=product_id)
            user_cart, created = Cart.objects.get_or_create(user=request.user)

           
            cart_item, created = CartItem.objects.get_or_create(cart=user_cart, product=product)
            cart_item.quantity += 1
            cart_item.save()

            return redirect('view_cart')  
        else:
            return redirect('login')  

class CartView(View):
    template_name = 'pages/cart.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        user_cart, created = Cart.objects.get_or_create(user=request.user)
        context = {'cart': user_cart}
        return render(request, self.template_name, context)




class ProductList(TemplateView):
    template_name = 'pages/product_list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = ShopModel.objects.all()
        return context
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)
    

class LoginView(TemplateView):
    template_name = 'authofication/login.html'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            
        return render(request, self.template_name, )
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class UserRegisterView(TemplateView):
    template_name = 'authofication/register.html'

    def post(self, request, *args, **kwrags):
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('home')

        context = {
            'form':form
            }

        return render(request, self.template_name, context)
    
    def get(self, request, *args, **kwargs):
        form = UserRegisterForm()
        context = {
            'form':form
        }

        return render(request, self.template_name, context)


class LikeProduct(View):

    @method_decorator(login_required)
    def disptch(self, request, pk:int, *args, **kwargs):
        return super().dispatch(request, pk *args, **kwargs)
    
    # def post(self, request, pk:int):
    #     Prodcut = ShopModel.objects.get(pk=pk)
    #     if request.user not in Prodcut.best_product.all():
    #         Prodcut.best_product.add(request.user)
    #     else:
    #         Prodcut.best_product.remove(request.user)

    #     return JsonResponse({'messgae': 'Ваши Действия Были успешо сохранены '})
    
    def get(self, request, *args, pk:int, **kwargs):
        Prodcut = ShopModel.objects.get(pk=pk)
        if request.user not in Prodcut.best_product.all():
            Prodcut.best_product.add(request.user)
        else:
            Prodcut.best_product.remove(request.user)

        return JsonResponse({'messgae': 'Ваши Действия Были успешо сохранены '})
    



class LogoutView(View):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')
    

class UserProfileView(TemplateView):
    template_name = 'pages/user_profile.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['products'] = ShopModel.objects.filter(user=user)
        return context
    

class ProductUploudView(TemplateView):
    template_name = 'uplouds/product_uploud.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request):
        form = ProductUploudForm(request.POST, request.FILES)
        if form.is_valid():
            new_product = form.save(commit=False)
            new_product.user = request.user 
            new_product.save()
            return redirect('home')
        
        context = {'form': form}
        return render(request, self.template_name, context)
        
    def get(self, request, *args, **kwargs):
        form = ProductUploudForm()
        context = {
            'form':form
        }
        return render(request, self.template_name, context)
    

class SearchView(TemplateView):
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):

        form = SerachProductForm(request.GET or None)
        products = None
        if request.method == 'GET':
            if form.is_valid():
                search_product = form.cleaned_data['search']
                products = ShopModel.objects.filter(product_title__icontains = search_product)
        
        context = {
            'form':form,
            'products':products
        }
        
        return render(request, 'pages/search.html', context)
    

class GetTexnikProducts(TemplateView):
    template_name = 'category_products/texnik.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['texnik_products'] = ShopModel.objects.filter(product_category='Техника')
        return context



class UserProfilePhotoView(TemplateView):
    template_name = 'uplouds/photo_uploud.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form = ProfilePhotoUploudForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        user = request.user
        profile_photo, created = UserProfile.objects.get_or_create(username=user)

        if not created and profile_photo.user_profile_photo:
            messages.success(request, '')

        form = ProfilePhotoUploudForm(request.POST, request.FILES, instance=profile_photo)
        if form.is_valid():
            new_ = form.save(commit=False)
            new_.user = request.user
            new_.save()
            return redirect('home')
        
        context = {
            'form': form
        }

        return render(request, self.template_name, context)

class ProductDetailView(DetailView):
    template_name = 'pages/product_detail.html'
    model = ShopModel
    context_object_name = 'products'

    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    


class CommentrionView(DetailView):
    template_name = 'uplouds/commentarion_uploud.html'
    model = ShopModel

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        commentarion_obj = self.get_object()
        comments = CommentModel.objects.filter(product=commentarion_obj)

        form = CommentForm()

        return render(request, 'uplouds/comment_uploud.html', {'form': form, 'comments': comments, 'commentarion_obj': commentarion_obj})

    def post(self, request, *args, **kwargs):
        commentarion_obj = self.get_object()
        comments = CommentModel.objects.filter(product=commentarion_obj)

        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.product = commentarion_obj
            new_comment.save()
            return JsonResponse({'messgae':'Коментарие было успешно добавлено '})

        return render(request, 'uplouds/comment_uploud.html', {'form': form, 'comments': comments, 'commentarion_obj': commentarion_obj})
    


class DeleteProdcutView(View):

    @method_decorator(login_required)
    def dispatch(Self, request, *args, pk:int, **kwargs):
        return super().dispatch(request, *args, pk ,**kwargs)

    def get(self, request, *args, pk:int, **kwargs):
       pass
    
    def post(self, request, pk:int):

        product_item  = ShopModel.objects.get(id=pk)

        if self.request.user == product_item.user:
            product_item.delete()
        return redirect('user_products')
            
