import mongoengine as me
import datetime

me.connect('webshop')


class Category(me.Document):
    title = me.StringField(min_length=1, max_length=512)
    subcategories = me.ListField(me.ReferenceField('self'))
    parent = me.ReferenceField('self', default=None)

    def add_subcategory(self, category: 'Category'):
        category.parent = self
        category.save()
        self.subcategories.append(category)
        self.save()

    def get_products(self):
        return Products.objects(category=self)

    @classmethod
    def get_root_categories(cls):
        return cls.objects(parent=None)

    @property
    def is_parent(self) -> bool:
        return bool(self.subcategories)


class Products(me.Document):
    title = me.StringField(min_length=1, max_length=512)
    description = me.StringField(min_length=1, max_length=4096)
    created = me.DateTimeField(default=datetime.datetime.now())
    price = me.DecimalField(required=True)
    discount = me.IntField(min_value=0, max_value=100, default=0)
    in_stock = me.BooleanField(default=True)
    image = me.FileField()
    category = me.ReferenceField(Category)

    @classmethod
    def get_discount_products(cls):
        return cls.objects(discount__ne=0)


class User(me.Document):
    _id = me.IntField()
    f_name = me.StringField()
    surname = me.StringField()
    email = me.StringField()
    add_price = me.ListField()


class MyCart(me.Document):
    user_id = me.IntField()
    product_id = me.ObjectIdField()
    value = me.IntField(default=1)
