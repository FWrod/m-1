from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from ckeditor.fields import RichTextField

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Add your email adress')
        if not username:
            raise ValueError('Add your username')
        if not password:
            raise ValueError('Add your password')

        user = self.model(
            email = self.normalize_email(email),
            username = username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            email = self.normalize_email(email),
            password = password,
            username = username
        )
        user.staff = True
        user.active = True
        user.admin = True
        user.superuser = True 
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="Email", unique=True)
    username = models.CharField(max_length=18, unique=True)
    staff = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    superuser = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active
    
    @property
    def is_superuser(self):
        return self.superuser

class Card(models.Model):
    title = models.CharField('Card title', max_length=100)
    content = RichTextField('Card content', blank=True, null=True)
    image = models.TextField('Image URL', blank=True)
    favorites = models.ManyToManyField(User, related_name='card_favorited_by', blank=False)
    date = models.CharField('Card date', max_length=80)

    def __str__(self):
        return self.title        

class Deck(models.Model):
    FORMAT_CHOICES = (
        ("STD", "Standard"),
        ("MDN", "Modern"),
        ("PIN", "Pioneer"),
        ("HTC", "Historic"),
        ("PPR", "Pauper"),
        ("LGC", "Legacy"),
        ("VTG", "Vintage"),
        ("CMD", "Commander"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Related user")
    title = models.CharField('Card title', max_length=100)
    deck_format = models.CharField(max_length=3, choices=FORMAT_CHOICES, blank=False, null=False)
    description = models.TextField()
    cards = models.ManyToManyField(Card, related_name='Deck_cards')
    favorites = models.ManyToManyField(User, related_name='deck_favorited_by', blank=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title