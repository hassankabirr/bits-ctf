from django.contrib import admin

# Register your models here.
from .models import *
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
# Register your models here.
admin.site.register(Question)
admin.site.register(Team)
admin.site.register(Contest)


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (                      # new fieldset added on to the bottom
            'Custom Field Heading',  # group heading of your choice; set to None for a blank space instead of a header
            {
                'fields': (
                    'team',
                    'user_status',

                ),
            },
        ),
    )
admin.site.register(CustomUser, CustomUserAdmin)