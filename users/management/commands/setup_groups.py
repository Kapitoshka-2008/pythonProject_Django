from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from catalog.models import Product
from blogs.models import BlogPost


class Command(BaseCommand):
    help = "Создает группы и назначает права: 'Модератор продуктов' и 'Контент-менеджер'."

    def handle(self, *args, **options):
        # Product Moderator
        product_moderator, _ = Group.objects.get_or_create(name='Модератор продуктов')
        product_ct = ContentType.objects.get_for_model(Product)

        delete_product_perm = Permission.objects.get(codename='delete_product', content_type=product_ct)
        unpublish_perm = Permission.objects.get(codename='can_unpublish_product', content_type=product_ct)

        product_moderator.permissions.set({delete_product_perm, unpublish_perm} | set(product_moderator.permissions.all()))
        self.stdout.write(self.style.SUCCESS("Группа 'Модератор продуктов' настроена."))

        # Content Manager
        content_manager, _ = Group.objects.get_or_create(name='Контент-менеджер')
        blog_ct = ContentType.objects.get_for_model(BlogPost)

        add_blog = Permission.objects.get(codename='add_blogpost', content_type=blog_ct)
        change_blog = Permission.objects.get(codename='change_blogpost', content_type=blog_ct)
        delete_blog = Permission.objects.get(codename='delete_blogpost', content_type=blog_ct)

        content_manager.permissions.set({add_blog, change_blog, delete_blog} | set(content_manager.permissions.all()))
        self.stdout.write(self.style.SUCCESS("Группа 'Контент-менеджер' настроена."))

        self.stdout.write(self.style.SUCCESS("Готово."))

