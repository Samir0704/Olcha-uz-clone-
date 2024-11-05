import os
import json
from django.db.models.signals import post_save,post_delete, pre_save,pre_delete
from olcha.models import Category,Product
from django.dispatch import receiver
from config.settings import BASE_DIR
from django.core.mail import send_mail
from config.settings import DEFAULT_FROM_EMAIL

def post_save_category(sender,created,instance, **kwargs):
    # Do something
    if created:
       print(f'Category {instance.category_name} created')

    else:
        print(f'Category {instance.category_name} updated')  


post_save.connect(post_save_category, sender=Category)

@receiver(pre_delete, sender=Category)
def pre_delete_category(sender, instance, **kwargs):
    file_path = os.path.join(BASE_DIR,'olcha/delete_products',f'category_{instance.id}.json')

    category_data = {
        'id' : instance.id,
        'category_name' : instance.category_name ,
        'slug' : instance.slug
    }


    with open(file_path,'w') as json_file :
        json.dump(category_data,json_file,indent=4)

def post_save_product(sender,created,instance, **kwargs):
    # Do something
    if created:
       print(f'Product {instance.product_name} created')

    else:
        print(f'Product {instance.product_name} updated')  
post_save.connect(post_save_product, sender=Product)

@receiver(pre_delete, sender=Product)
def pre_delete_product(sender, instance, **kwargs):
    file_path = os.path.join(BASE_DIR,'olcha/delete_products',f'product_{instance.id}.json')

    product_data = {
        'id' : instance.id,
        'product_name' : instance.product_name ,
        'description' : instance.description,
        'price' : instance.price,
        'quantity' : instance.quantity,
        'discount' : instance.discount,
        'slug' : instance.slug
    }


    with open(file_path,'w') as json_file :
        json.dump(product_data,json_file,indent=4)

@receiver(post_save, sender=Product)
def post_save_product(sender, instance, created, **kwargs):
    if created:
        print('Product created ')
        subject = 'Product created'
        message = f' Product {instance.product_name } Admin tomonidan yaratildi'
        from_email = DEFAULT_FROM_EMAIL
        to = 'abdurahimovsamir27@gmail.com'
        send_mail(subject,message,from_email,[to,],fail_silently=False)

    else:
        print('product updated')

# @receiver(post_delete, sender=Product)
# def post_delete_product(sender, instance, delete, **kwargs):
#     if delete:
#         print('Product delete ')
#         subject = 'Product delete'
#         message = f' Product {instance.product_name } Admin tomonidan ochirildi'
#         from_email = DEFAULT_FROM_EMAIL
#         to = 'abdurahimovsamir27@gmail.com'
#         send_mail(subject,message,from_email,[to,],fail_silently=False)

#     else:
#         print('product updated')




