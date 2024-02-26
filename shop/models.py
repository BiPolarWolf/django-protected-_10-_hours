import random
import string
from django.db import models
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.text import slugify

def random_slug():
    """
    Generate a random slug consisting of 3 alphanumeric characters.
    """
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(3))

class Category(models.Model):
    name = models.CharField('Категория',max_length=100, db_index=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    slug = models.SlugField('URL',max_length=250, unique=True ,null=True ,editable=True)
    created_at = models.DateTimeField('дата создания',auto_now_add=True)

    class Meta:
        unique_together = (["slug", "parent"])
        verbose_name_plural = "Категории"
        verbose_name = 'Категория'

    def __str__(self):

        """
        Return a string representing the full path by traversing the parent hierarchy.

        """

        full_path = [self.name]
        k = self.parent
        while  k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' > '.join(full_path[::-1])

    

    def save(self,*args, **kwargs):

        """
        Save the category with a generated slug if it doesn't already have one.
        """

        if not self.slug:
            self.slug =slugify(random_slug()+ '-pickBetter' + self.name)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self) :
            return reverse('shop:products_by_category', kwargs={'slug': self.slug}) 

class Product(models.Model):
    """
    Represents a product with a title, brand, description, price, image, availability, and timestamps for creation and update.

    """
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    title = models.CharField('Название',max_length=250)
    brand = models.CharField('Бренд',max_length=250)
    description = models.TextField('Описание',blank=True)
    slug = models.SlugField('URL',max_length=250)
    price = models.DecimalField('Цена',max_digits=10, decimal_places=2 ,default=99.99)
    image = models.ImageField('Изображение',upload_to='products/%Y/%m/%d')
    available = models.BooleanField('Наличие',default=True)
    create_at = models.DateTimeField('дата создания',auto_now_add=True)
    update_at = models.DateTimeField('дата изменения',auto_now=True)

    class Meta:

        """
        Metadata for the Product model, including verbose names for the singular and plural forms.
        """

        verbose_name_plural = "Товары"
        verbose_name = 'Товар'
    
    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.slug]) 


    def __str__(self):
        
        """
        Return a string representation of the object.

        """
        return self.title
    
class ProductManager(models.Manager):

    def get_queryset(self):
        """
        Return a queryset of available products.
        """
        return super(ProductManager, self).get_queryset().filter(available=True)

class ProductProxy(Product):

    objects = ProductManager()

    class Meta:
        proxy = True

