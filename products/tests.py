from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Product

User = get_user_model()

class ProductAPITestCase(APITestCase):

    def setUp(self):
        # company user creation
        self.company_user = User.objects.create_user(email="company@gmail.com", password="companypass", username="company", role="company")

        # customer user creation
        self.customer_user = User.objects.create_user(email="customer@gmail.com", password="customerpass", username="customer", role="customer")

        # none owner comapny user creation for testing permission and ownerships 
        self.non_owner_company_user = User.objects.create_user(email="nonownercompany@example.com", password="testpassword", username="nonownercompanyuser", role="company")
        
        self.client = APIClient()

        self.product = Product.objects.create(
            name="sample name",
            description="sample product",
            price=150,
            category="electronics",
            owner=self.company_user
        )

        self.product_url = reverse('product-detail', kwargs={'pk': self.product.pk})


    def test_create_product_as_company(self):
        
        '''Attampt to update send post request (add) to
           the product api with company user - should be allowed'''

        self.client.force_authenticate(user=self.company_user)
        data = {
            "name": "New Product",
            "description": "This is a new product",
            "price": 150,
            "category": "fashion",
            "availability": True
        }
        response = self.client.post(reverse('product-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)
    

    def test_create_product_as_customer(self):

        '''Attampt to update send post request (add) to 
           the product api with customer user - should NOT be allowed'''

        self.client.force_authenticate(user=self.customer_user)
        data = {
            "name": "New Product",
            "description": "This is a new product",
            "price": 150,
            "category": "fashion",
            "availability": True
        }
        response = self.client.post(reverse('product-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Product.objects.count(), 1)


    def test_updating_or_deleting_with_none_owner_user(self):

        '''Attampt to update send put/delete request (update/delete) to 
           the specific product with the none woner user - should NOT be allowed'''

        self.client.force_authenticate(user=self.non_owner_company_user)
        data = {
            "name": "updating",
            "description": "This is a new product",
            "price": 150,
            "category": "fashion",
            "availability": True
        }
        # trying to update the product
        response = self.client.put(reverse('product-detail', kwargs={'pk': self.product.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #trying to delete the product
        response = self.client.delete(reverse('product-detail', kwargs={'pk': self.product.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
