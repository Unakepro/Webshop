from models import Category, Products
from random import choice
import random
import os


dir_path = os.path.dirname(os.path.realpath(__file__))
category_laptops = Category.objects.create(title='Laptops')

def seed_macbook():
    subcategory = Category.objects.create(title='Macbook')
    category_laptops.add_subcategory(subcategory)

    directory = f'{dir_path}/images/macbook'
    files = os.listdir(directory)

    for photo in files:
        with open(f'{dir_path}/images/macbook/{photo}', 'rb') as image:
            with open(f'{dir_path}/description.txt', 'r') as file:
                line = file.readlines()
                Products.objects.create(title=choice(['Macbook Pro', 'Macbook Air', 'Macbook Pro Retina']),
                                        description=line[random.randrange(1, 5)], discount=random.randrange(1, 50),
                                        price=random.randrange(10, 10000),
                                        image=image, category=subcategory)


def seed_hp():
    subcategory = Category.objects.create(title='HP')
    category_laptops.add_subcategory(subcategory)

    directory = f'{dir_path}/images/hp'
    files = os.listdir(directory)

    for photo in files:
        with open(f'{dir_path}/images/hp/{photo}', 'rb') as image:
            with open(f'{dir_path}/description.txt', 'r') as file:
                line = file.readlines()
                Products.objects.create(title=choice(['Hp 250', 'Hp Notebook', 'Hp pavilion']),
                                        description=line[random.randrange(1, 5)], discount=random.randrange(1, 50),
                                        price=random.randrange(10, 10000),
                                        image=image, category=subcategory)


def seed_laptops():
    seed_macbook()
    seed_hp()


category_pc = Category.objects.create(title='PC')


def seed_video_cards():
    subcategory = Category.objects.create(title='Video Cards')
    category_pc.add_subcategory(subcategory)

    directory = f'{dir_path}/images/video_cards'
    files = os.listdir(directory)

    for photo in files:
        with open(f'{dir_path}/images/video_cards/{photo}', 'rb') as image:
            with open(f'{dir_path}/description.txt', 'r') as file:
                line = file.readlines()
                Products.objects.create(title=choice(['RTX 2080TI', 'RTX 2070 SUPER', 'AMD RX 570']),
                                        description=line[random.randrange(1, 5)],
                                        price=random.randrange(10, 10000),
                                        image=image, category=subcategory)


def seed_processors():
    subcategory = Category.objects.create(title='Processors')
    category_pc.add_subcategory(subcategory)

    directory = f'{dir_path}/images/processors'
    files = os.listdir(directory)

    for photo in files:
        with open(f'{dir_path}/images/processors/{photo}', 'rb') as image:
            with open(f'{dir_path}/description.txt', 'r') as file:
                line = file.readlines()
                Products.objects.create(title=choice(['I9900K', 'I5 10600K', 'AMD ryzen 5']),
                                        description=line[random.randrange(1, 5)],
                                        price=random.randrange(10, 10000),
                                        image=image, category=subcategory)


def seed_pc():
    seed_video_cards()
    seed_processors()


def seed_router():
    category = Category.objects.create(title='Routers')

    directory = f'{dir_path}/images/routers'
    files = os.listdir(directory)

    for photo in files:
        with open(f'{dir_path}/images/routers/{photo}', 'rb') as image:
            with open(f'{dir_path}/description.txt', 'r') as file:
                line = file.readlines()
                Products.objects.create(title=choice(['Asus RT', 'TP-LINK', 'Archer A5']),
                                        description=line[random.randrange(1, 5)], price=random.randrange(10, 10000),
                                        image=image, discount=random.randrange(1, 50), category=category)


if __name__ == '__main__':
    seed_router()
    seed_laptops()
    seed_pc()
