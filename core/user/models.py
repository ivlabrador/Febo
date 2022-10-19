from crum import get_current_request
from django.db import models
from config import settings
from django.contrib.auth.models import AbstractUser
from django.forms import model_to_dict
# Create your models here.

class User(AbstractUser):
    image = models.ImageField(upload_to='users/%Y/%m/%d', null=True, blank=True)
    token = models.UUIDField(primary_key=False, editable=False, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/no-img-prof.jpg'

    def get_username(self):
        if self.username:
            return self.username

    def toJSON(self):
        item = model_to_dict(self, exclude=['password', 'user_permissions', 'last_login'])
        item['last_login'] = '' if self.last_login is None else self.last_login.strftime('%d-%m-%Y')
        item['date_joined'] = self.date_joined.strftime('%d-%m-%Y')
        item['image'] = self.get_image()
        item['full_name'] = self.get_full_name()
        item['groups'] = [{'id': g.id, 'name': g.name} for g in self.groups.all()]
        return item

    def get_group_session(self):
        try:
            request = get_current_request()
            groups = self.groups.all()
            if groups.exists():
                if 'group' not in request.session:
                    request.session['group'] = groups[0]
        except:
            pass