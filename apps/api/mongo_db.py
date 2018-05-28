from mongoengine import Document, connect
from mongoengine.fields import StringField, DateTimeField, IntField


connect('mes', alias='default')


class DeviceInfo(Document):
    meta = {
        'collection': 'devices',
        'ordering': ['-_id']
    }

    batery = IntField()
    signal = IntField()
    device_id = StringField()


class PackageModel(Document):
    meta = {
        'collection': 'packages',
        'ordering': ['time']
    }

    package_type = StringField(db_field='type')
    time = DateTimeField()
    device_id = StringField()
