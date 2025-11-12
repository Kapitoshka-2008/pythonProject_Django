from django.db import models
from django.conf import settings


class Category(models.Model):
	name = models.CharField(max_length=255, unique=True, verbose_name='Наименование')
	description = models.TextField(blank=True, verbose_name='Описание')
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
	updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

	class Meta:
		verbose_name = 'Категория'
		verbose_name_plural = 'Категории'
		ordering = ['name']

	def __str__(self) -> str:
		return self.name


class Product(models.Model):
	name = models.CharField(max_length=255, verbose_name='Наименование')
	description = models.TextField(blank=True, verbose_name='Описание')
	image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='Изображение')
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория')
	price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за покупку')
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
	updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

	class PublicationStatus(models.TextChoices):
		DRAFT = 'draft', 'Черновик'
		PUBLISHED = 'published', 'Опубликован'

	status = models.CharField(
		max_length=16,
		choices=PublicationStatus.choices,
		default=PublicationStatus.DRAFT,
		verbose_name='Статус публикации',
	)
	owner = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name='products',
		verbose_name='Владелец',
	)

	class Meta:
		verbose_name = 'Продукт'
		verbose_name_plural = 'Продукты'
		ordering = ['name']
		permissions = (
			('can_unpublish_product', 'Может отменять публикацию продукта'),
		)

	def __str__(self) -> str:
		return f'{self.name} ({self.category.name})'
