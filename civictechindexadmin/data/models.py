from django.conf import settings
from django.db import models


class Organization(models.Model):
    import_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=256)
    parent_organization = models.ForeignKey('self',
                                            null=True,
                                            blank=True,
                                            on_delete=models.SET_NULL)
    # CNK we will probably want to do something more sophisticated for location eventually
    location = models.CharField(max_length=1024, blank=True)
    image_url = models.URLField(max_length=2048, blank=True)

    def __str__(self):
        return f"Org: {self.name}"


class Link(models.Model):
    LINK_TYPE_CHOICES = [
        ('WebSite', 'WebSite'),
        ('MeetUp', 'MeetUp'),
        ('FaceBook', 'FaceBook'),
        ('Twitter', 'Twitter'),
        ('GitHub', 'GitHub'),
    ]

    organization = models.ForeignKey(Organization,
                                     related_name='links',
                                     on_delete=models.CASCADE)
    link_type = models.CharField(max_length=200,
                                 choices=LINK_TYPE_CHOICES)
    url = models.CharField(max_length=1024)

    def __str__(self):
        return f"{self.link_type}: {self.url}"


# ###### FAQS ###########
class FAQ(models.Model):
    question = models.CharField(max_length=512)
    answer = models.TextField(max_length=4096, blank=True)
    live = models.BooleanField(default=False)
    view_count = models.PositiveIntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='faqs_created',
        blank=True,
        on_delete=models.CASCADE
    )
    modified_date = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='faqs_modified',
        blank=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"FAQ {self.id}: {self.question}"


# ######## Notification Signups ##########
class NotificationSubscription(models.Model):
    notification_type = models.CharField(max_length=256)
    email_address = models.EmailField(max_length=256)
    # I am allowing NOT storing ip_address so we don't have to fake it when adding via admin interface
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['notification_type', 'email_address']]
