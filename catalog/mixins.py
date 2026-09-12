from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin
class SellerRequiredMixin(UserPassesTestMixin):
   """Faqat role=SELLER bo‘lgan user kiradi."""
   def test_func(self):
       user = self.request.user
       return user.is_authenticated and getattr(user, "role", None) == "SELLER"

   def handle_no_permission(self):
       messages.error(self.request, "Bu bo‘lim faqat sotuvchilar uchun ❌")
       return redirect("product_list")

class OwnerRequiredMixin(UserPassesTestMixin):
   """
   Faqat obyekt egasi (seller) kiradi.
   """
   def test_func(self):
       obj = self.get_object() 
       return obj.seller == self.request.user

   def handle_no_permission(self):
       messages.error(self.request, "Bu mahsulot sizga tegishli emas ❌")
       return redirect("seller_products")
