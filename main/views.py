from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView, DeleteView, CreateView

# Create your views here.
from .forms import *
from .models import *
from .permissions import UserHasPermissionMixin


class MainPageView(ListView):
    model = Product
    template_name = 'main.html'
    context_object_name = 'products'


class ProductListView(ListView):
    model = Product
    template_name = 'list_product.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category_detail.html'
    context_object_name = 'category'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.slug = kwargs.get('slug', None)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(category_id=self.slug)
        return context


class CompanyDetailView(DetailView):
    model = Company
    template_name = 'company_detail.html'
    context_object_name = 'company'


class TagDetailView(DetailView):
    model = Tag
    template_name = 'update_product.html'
    context_object_name = 'tag'


class AddProduct(CreateView):
    model = Product
    template_name = 'add_product.html'
    form_class = AddProductForm

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs['request'] = self.request
    #     return kwargs

    def get_success_url(self):
        return reverse('add_product_image.html', args=(self.object.id, ))


class AddProductImage(CreateView):
    model = Image
    template_name = 'add_product_image.html'
    form_class = ImageForm

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs['request'] = self.request
    #     return kwargs

    def get_success_url(self):
        return reverse('product-detail', args=(self.object.id, ))

#
# @login_required(login_url='login')
# def add_product(request):
#     ImageFormSet = modelformset_factory(Image, form=ImageForm, max_num=5)
#     if request.method == 'POST':
#         product_form = AddProductForm(request.POST)
#         formset = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())
#         if product_form.is_valid() and formset.is_valid():
#             product = product_form.save(commit=False)
#             product.user = request.user
#             product.save()
#
#             for form in formset.cleaned_data:
#                 image = form['image']
#                 Image.objects.create(image=image, product=product)
#                 image.save()
#             return redirect(product.get_absolute_url())
#     else:
#         product_form = AddProductForm()
#         formset = ImageFormSet(queryset=Image.objects.none())
#     return render(request, 'add_product.html', locals())
#
#
# def update_product(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     if request.user == product.user:
#         ImageFormSet = modelformset_factory(Image, form=ImageForm, max_num=5)
#         product_form = AddProductForm(request.POST or None, instance=product)
#         formset = ImageFormSet(request.POST or None, request.FILES or None, queryset=Image.objects.filter(product=product))
#         if product_form.is_valid() and formset.is_valid():
#             product_form.save()
#
#             for form in formset:
#                 image = form.save(commit=False)
#                 image.product = product
#                 image.save()
#             return redirect(product.get_absolute_url())
#         return render(request, 'update_product.html', locals())
#
#     else:
#         return HttpResponse('<h1> Error:403 Forbidden</h1>')


class DeleteRecipeView(UserHasPermissionMixin, DeleteView):
    model = Product
    template_name = 'delete_product.html'
    success_url = reverse_lazy('home')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.add_message(request, messages.SUCCESS, 'Successfully deleted!')
        return HttpResponse(success_url)


