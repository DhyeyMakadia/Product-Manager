from django.db import models

# Create your models here.
class Company_data(models.Model):
    com_nm = models.CharField("Company Name",default="",blank=True,null=True,max_length=100)
    com_em = models.EmailField("Company Email",default="")
    com_cno = models.PositiveIntegerField("Contact No",default=0)
    com_add = models.TextField("Address",default="",blank=True,null=True)
    join_date = models.DateField(auto_now=True,blank=True,null=True)
    profile = models.ImageField(upload_to="comp_profile",default="",max_length=200,blank=True,null=True)
    com_pass = models.CharField("Password",default="",max_length=200)

    def __str__(self):
        return self.com_nm

class Company_Customer(models.Model):
    comp = models.ForeignKey('Company_data',on_delete=models.CASCADE,blank=True,null=True)
    cust_nm = models.CharField("Customer Name",default="",blank=True,null=True,max_length=100)
    cust_em = models.EmailField("Customer Email",default="")
    cust_cno = models.PositiveIntegerField("Contact No",default=0)
    cust_add = models.TextField("Address",default="",blank=True,null=True)
    cust_join_date = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    cust_profile = models.ImageField(upload_to="Customer_profile",default="",max_length=200,blank=True,null=True)
    cust_pass = models.CharField("Password",default="",max_length=200)

    def __str__(self):
        return self.cust_nm

class Company_Product(models.Model):
    comp = models.ForeignKey('Company_data',on_delete=models.CASCADE,blank=True,null=True)
    pro_nm = models.CharField("Product Name",default="",blank=True,null=True,max_length=100)
    pro_pr = models.PositiveIntegerField("Price",default=0)
    pro_qty = models.PositiveIntegerField("Quantity",default=0)
    pro_img = models.ImageField(upload_to="Products",default="",max_length=200,blank=True,null=True)

    def __str__(self):
        return self.pro_nm

class Customer_Order(models.Model):
    comp = models.ForeignKey('Company_data',on_delete=models.CASCADE,blank=True,null=True)
    cust = models.ForeignKey('Company_Customer',related_name='customer',on_delete=models.CASCADE,blank=True,null=True)
    pro = models.ForeignKey('Company_Product',on_delete=models.CASCADE,blank=True,null=True)
    total_price = models.PositiveIntegerField("Total Price",default=0)
    qty = models.PositiveIntegerField("Quantity",default=0)
    order_date = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    status = models.CharField("Status",default="pending",max_length=20)

    def __str__(self):
        return self.pro.pro_nm