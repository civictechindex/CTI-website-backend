from django.db import models

class Organization(models.Model):
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
