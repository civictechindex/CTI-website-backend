from django.conf import settings
from django.db import models
from django.contrib.sites.models import Site
from django.utils.text import slugify
from github import Github, GithubException
from treebeard.mp_tree import MP_Node


class Organization(MP_Node):
    ORG_STATE_CHOICES = [
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
    ]

    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(max_length=256, blank=True, unique=True)
    city = models.CharField(max_length=256, blank=True)
    state = models.CharField(max_length=256, blank=True)
    country = models.CharField(max_length=256, blank=True)
    image_url = models.URLField(max_length=2048, blank=True)
    github_name = models.CharField(max_length=1024, blank=True)
    github_id = models.IntegerField(blank=True, null=True)
    cti_contributor = models.BooleanField(blank=True, null=True, default=None)
    org_tag = models.CharField(max_length=128, blank=True)
    # Organization email is the email collected when someone submits an org
    # through the tag generator. It is not a general contact email for the org
    organization_email = models.EmailField(max_length=256, blank=True)
    status = models.CharField(max_length=32,
                              choices=ORG_STATE_CHOICES,
                              default='submitted')

    # Treebeard will store nodes in alphabetic order based on name
    node_order_by = ['name']

    def __str__(self):
        return f"Org: {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
            # Sometimes slugify strips out everything, so check before committing
            if not self.slug:
                raise RuntimeError("Django's slugify method was not able to create a slug for this organization.")
        super().save(*args, **kwargs)

    def _create_github_issue(self):
        site = Site.objects.first()
        domain = site.domain if site else 'localhost'
        body = f"""A new organization, {self.name}, has been submitted.
            Please visit https://{domain}/admin/data/organization/{self.id}/change/ to review and approve it.
        """
        gh_api = Github(settings.GH_TOKEN)
        try:
            repo_path = "civictechindex/CTI-website-frontend"
            repo = gh_api.get_repo(repo_path)
        except GithubException as e:
            print(f"Could not retrieve the desired repository {repo_path} ", e)
            return
        try:
            labels = [repo.get_label("New-Organization-Submission")]
            if domain != 'api.civictechindex.org':
                labels.append(repo.get_label("duplicate"))
                labels.append(repo.get_label("p-feature: tag generator"))
                labels.append(repo.get_label("role: product management"))
        except GithubException as e:
            print("Could not retrieve the desired labels: ", e)
            return
        try:
            issue = repo.create_issue(
                title=f"New Organization: {self.name}",
                body=body,
                labels=labels,
            )
        except:  # noqa
            print('Could not create GitHub issue')

        # Issue has been created, now let's try to create a card for it in the Project Management
        # board
        try:
            for project in repo.get_projects(state='open'):
                if project.name == 'Project Management':
                    pm_project = project
            for col in pm_project.get_columns():
                if col.name == 'New Issue Approval':
                    new_issue_column = col
        except GithubException as e:
            print("Could not retrieve the desired Project board information: ", e)
            return
        # Create the card
        try:
            new_issue_column.create_card(content_id=issue.id, content_type='Issue')
        except GithubException as e:
            print("Could not retrieve the desired Project board information: ", e)
            return


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
    http_status = models.CharField(max_length=8, null=True, blank=True)
    http_status_date = models.DateField(null=True, blank=True)
    notes = models.TextField(max_length=4096, null=True, blank=True)

    def __str__(self):
        return f"{self.link_type}: {self.url}"

    class Meta:
        unique_together = [['organization', 'link_type']]


class Alias(models.Model):
    tag = models.CharField(max_length=30)
    alias = models.CharField(max_length=30)

    class Meta:
        verbose_name = "Alias"
        verbose_name_plural = "Aliases"

    def __str__(self):
        return f"Alias {self.id}: {self.tag} {self.alias}"


# ###### FAQS ###########
class FAQ(models.Model):
    FAQ_STATUS_CHOICES = [
        ('New', 'New'),
        ('ToBeAnswered', 'To be answered'),
        ('ToBeDeleted', 'To be deleted'),
        ('Duplicate', 'Duplicate'),
    ]
    question = models.CharField(max_length=512)
    answer = models.TextField(max_length=4096, blank=True)
    live = models.BooleanField(default=False)
    status = models.CharField(max_length=100,
                              choices=FAQ_STATUS_CHOICES,
                              default='New')
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

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

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
