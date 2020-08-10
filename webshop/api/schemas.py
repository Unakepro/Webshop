from marshmallow import Schema, fields, validates, validate, ValidationError
from ..db.models import Category


class ProductSchema(Schema):
    title = fields.String(validate=validate.Length(min=1, max=512), required=True)
    description = fields.String(validate=validate.Length(min=1, max=4096), required=True)
    created = fields.DateTime(dump_only=True)
    price = fields.Float(required=True)
    discount = fields.Integer()
    in_stock = fields.Boolean(default=True)
    category = fields.String(required=True)

    @validates('category')
    def validate_id(self, value):
        try:
            if Category.objects(id=value):
                pass
            else:
                raise ValidationError(message={'Error': 'Not valid id'})
        except:
            raise ValidationError(message={'Error': 'Not valid id'})


class CategorySchema(Schema):
    title = fields.String(validate=validate.Length(min=1, max=512), required=True)
    subcategories = fields.List(fields.String())
    parent = fields.String()

    @validates('parent')
    def validate_parent(self, value):
        try:
            if Category.objects(id=value):
                pass
            else:
                raise ValidationError(message={'Error': 'Not valid id'})
        except:
            raise ValidationError(message={'Error': 'Not valid id'})

    @validates('subcategories')
    def validate_sub(self, value):
        for i in list(value):
            try:
                if Category.objects(id=i):
                    pass
                else:
                    raise ValidationError(message={'Error': 'Not valid id'})
            except:
                raise ValidationError(message={'Error': 'Not valid id'})