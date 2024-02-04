from tortoise import Model, fields


class User(Model):
    user_id = fields.IntField(unique=True)
    username = fields.CharField(max_length=255, default='')
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "users"


class Asset(Model):
    user = fields.ForeignKeyField('models.User')
    price = fields.FloatField()
    name = fields.CharField(max_length=255)
    number = fields.FloatField()
    currency = fields.CharField(max_length=16)
    transaction_date = fields.DatetimeField(default=None)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "assets"
