from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.
class Product(models.Model):
    CATEGORY = (
        ('electronics', 'Electronics'),
        ('fashion', 'Fashion'),
        ('home_appliances', 'Home Appliances'),
        ('books', 'Books'),
        ('toys', 'Toys'),
        ('sports', 'Sports'),
        ('beauty', 'Beauty'),
    )

    image = models.ImageField()
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.IntegerField()
    category = models.CharField()
    availability = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    num_reviews = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def update_rating(self):
        reviews = self.reviews_set.all()
        if reviews:
            self.rating = sum(review.rating for review in reviews) / len(reviews)
            self.num_reviews = len(reviews)
        else:
            self.rating = 0.00
            self.num_reviews = 0
        self.save()
        
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    data_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} - {self.product.name}'
    
    class Meta: 
        unique_together = ('product', 'user')

