from django.db import models
from django.utils.text import slugify
from django.conf import settings
import uuid

# Create your models here.
class Category(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    name = models.CharField(max_length=255,unique=True)
    slug = models.SlugField(unique=True,blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    name = models.CharField(max_length=250)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    slug = models.SlugField(unique=True,blank=True)
    description = models.TextField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    is_active = models.BooleanField(default=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name','category']
    
    def __str__(self):
        return self.name
    
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)





class ProductVariant(models.Model):
    MATERIAL_CHOICES = [
        ('WOOD', 'Wood'),
        ('METAL', 'Metal'),
        ('GLASS', 'Glass'),
        ('PLASTIC', 'Plastic'),
        ('FABRIC', 'Fabric'),
        ('LEATHER', 'Leather'),
        ('MARBLE', 'Marble'),
        ('BAMBOO', 'Bamboo'),
        ('PLYWOOD', 'Plywood'),
        ('MDF', 'Medium-Density Fiberboard'),
        ('RATTAN', 'Rattan / Wicker'),
        ('STONE', 'Stone'),
        ('ACRYLIC', 'Acrylic'),
        ('COMPOSITE', 'Composite / Engineered Material'),
    ]
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    material = models.CharField(choices=MATERIAL_CHOICES,max_length=100)
    color = models.CharField(max_length=100)
    slug = models.SlugField(unique=True,blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product} - {self.material}'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.material)
        super().save(*args, **kwargs)


