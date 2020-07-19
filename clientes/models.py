from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

class Document(models.Model):
  num_doc = models.CharField(max_length=50)

  def __str__(self):
    return self.num_doc


class Person(models.Model):
  first_name = models.CharField(max_length=30)
  last_name = models.CharField(max_length=30)
  age = models.IntegerField()
  salary = models.DecimalField(max_digits=5, decimal_places=2)
  bio = models.TextField()
  photo = models.ImageField(upload_to='clients_photos', null=True, blank=True)
  doc = models.OneToOneField(Document, null=True, blank=True, on_delete=models.CASCADE)

  def __str__(self):
    return self.first_name + ' ' + self.last_name


class Product(models.Model):
  description = models.CharField(max_length=100)
  price = models.DecimalField(max_digits=5, decimal_places=2)

  def __str__(self):
    return self.description
  
  
class Sales(models.Model):
  number = models.CharField(max_length=30)
  value = models.DecimalField(max_digits=5, decimal_places=2)
  discount = models.DecimalField(max_digits=5, decimal_places=2)
  tax = models.DecimalField(max_digits=5, decimal_places=2)
  person = models.ForeignKey(Person, null=True, blank=True, on_delete=models.PROTECT)
  products = models.ManyToManyField(Product,blank=True)

  def calcular_total(self):
    tot = self.itemrequest_set.all().aggregate(
    tot_ped=Sum((F('quantity') * F('product__price')) - F('descount'), output_field=FloatField()))['tot_ped']

    tot = tot - float(self.tax) - float(self.discount)
    self.value = tot
    self.save()

  def __str__(self):
    return self.number


class ItemDoPedido(models.Model):
  venda = models.ForeignKey(Sales, on_delete=models.CASCADE)
  produto = models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity = models.FloatField()
  discount = models.DecimalField(max_digits=5,decimal_places=2)

  def __str__(self):
    return self.number


@receiver(post_save, sender=ItemDoPedido)
def update_vendas_total(sender, instance, **kwargs):
  instance.venda.calcular_total()



