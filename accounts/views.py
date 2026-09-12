from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView,  DetailView, UpdateView
from .forms import SignUpForm, ProfileForm
from .models import User


class SignUpView(CreateView):
   form_class = SignUpForm
   template_name = "accounts/signup.html"
   success_url = reverse_lazy("home")
   def form_valid(self, form):
       response = super().form_valid(form)   # user bazaga saqlanadi
       login(self.request, self.object)      #tizimga avtomatik kirib qo’yadi
       messages.success(self.request, "Ro‘yxatdan o‘tish muvaffaqiyatli ✅")
       return response
   def form_invalid(self, form):
       messages.error(self.request, "Formada xatolik bor ❌")
       return super().form_invalid(form)
    
class CustomLoginView(LoginView):
   template_name = "accounts/login.html"

   def form_valid(self, form):
       messages.success(self.request, "Tizimga kirdingiz ✅")
       return super().form_valid(form)

   def form_invalid(self, form):
       messages.error(self.request, "Login yoki parol xato ❌")
       return super().form_invalid(form)


class CustomLogoutView(LogoutView):
   next_page = "product_list"
   def dispatch(self, request):
       messages.info(request, "Tizimdan chiqdingiz 👋")
       return super().dispatch(request)
   
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView,  DetailView, UpdateView
from .forms import SignUpForm, ProfileForm
from .models import User
class ProfileDetailView(LoginRequiredMixin, DetailView):
   model = User
   template_name = "accounts/profile_detail.html"
   context_object_name = "profile_user"

   def get_object(self):
       return self.request.user

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
   model = User
   form_class = ProfileForm
   template_name = "accounts/profile_edit.html"
   success_url = reverse_lazy("profile")
   def get_object(self):
       return self.request.user
   def form_valid(self, form):
       messages.success(self.request, "Profil yangilandi ✅")
       return super().form_valid(form)
   def form_invalid(self, form):
       messages.error(self.request, "Profilni saqlashda xatolik bor ❌")
       return super().form_invalid(form)

