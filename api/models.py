import uuid

from django.core.validators import MinValueValidator
from django.db import models

from users.models import CustomUser


class Color(models.Model):
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name


class Discount(models.Model):
    name = models.PositiveIntegerField(validators=[MinValueValidator(0)])

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return str(self.name)


class Brand(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=200, unique=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='section'
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='product_category'
    )
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='product_section'
    )
    description = models.CharField(max_length=2000)
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='product_brand'
    )
    item_number = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    price = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    rating = models.FloatField(null=True, blank=True)
    size = models.FloatField(null=False, blank=False)
    color = models.ManyToManyField(
        Color,
        blank=False,
    )
    age = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        validators=[MinValueValidator(0)]
    )
    male = models.BooleanField(default=True)
    is_sale = models.BooleanField(default=False)
    discount = models.ForeignKey(
        Discount,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return f'{self.name}'


class Picture(models.Model):
    product = models.ForeignKey(
        Product,
        related_name='product_images',
        on_delete=models.CASCADE,
    )
    product_image = models.ImageField()

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return f'{self.product}: {self.product_image}'


class Favorite(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='favorite'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='favorite'
    )

    class Meta:
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'product'), name='unique_favorite_product'
            )
        ]

    def __str__(self):
        return f'{self.product}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='shoppingcart'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='shoppingcart'
    )

    class Meta:
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'product'), name='unique_shopping_cart'
            )
        ]

    def __str__(self):
        return f'{self.user}: {self.product}'
