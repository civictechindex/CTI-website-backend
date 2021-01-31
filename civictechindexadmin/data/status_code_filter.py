from django.contrib.admin import SimpleListFilter
from django.db.models import Q


class StatusCodeFilter(SimpleListFilter):
    title = 'Status Code'  # a label for our filter
    parameter_name = 'pages'  # you can put anything here

    def lookups(self, request, model_admin):
        # This is where you create filter options; we have three:
        return [
            ('OK', 'OK'),
            ('NotOK', 'Not OK'),
            ('broken', 'Broken'),
            ('300 - 399', '300 - 399'),
            ('400', '400'),
            ('401 - 499', '401 - 499'),
            ('other', 'Other'),
        ]

    def queryset(self, request, queryset):
        # This is where you process parameters selected by use via filter options:
        if self.value() == 'OK':
            # Get Links that don't have an http status value (or is blank or is < 300)
            return queryset.distinct().filter(http_status__isnull=True)
        elif self.value() == 'broken':
            # Get Links with http status broken.
            return queryset.distinct().filter(http_status='broken')
        elif self.value() == '300 - 399':
            # Get Links with http status in the 300 range.
            return queryset.distinct().filter(Q(http_status__gte='300') & Q(http_status__lte='399'))
        elif self.value() == '400':
            # Get Links with http status = 400.
            return queryset.distinct().filter(http_status='400')
        elif self.value() == '401 - 499':
            # Get Links with http status in the 400 range.
            return queryset.distinct().filter(Q(http_status__gte='401') & Q(http_status__lte='499'))
        elif self.value() == 'other':
            # Get Links with http status is not null or (!= '' and < 300 and >= 500).
            return (queryset.distinct()
                            .exclude(http_status='broken')
                            .filter(Q(http_status__lte='299')  | Q(http_status__gte='500'))
                    )
        elif self.value() == 'NotOK':
            # Get Links with http status is not null or not blank.
            return queryset.distinct().filter(http_status__isnull=False).exclude(http_status__exact='')
