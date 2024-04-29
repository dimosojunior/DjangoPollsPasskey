from django.contrib import admin
from .models import *
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin



class MyUserAdmin(BaseUserAdmin):
    list_display=('username', 'email','Course','Year', 'date_joined', 'last_login', 'is_admin', 'is_active')
    search_fields=('email','username', 'first_name', 'last_name')
    readonly_fields=('date_joined', 'last_login')
    filter_horizontal=()
    list_filter=('last_login',)
    fieldsets=()

    add_fieldsets=(
        (None,{
            'classes':('wide'),
            'fields':('email', 'username','Course','Year', 'first_name', 'middle_name', 'last_name', 'phone', 'password1', 'password2'),
        }),
    )

    ordering=('email',)

admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Poll)
admin.site.register(Choice)
admin.site.register(Vote)
admin.site.register(ElectionCategories)
admin.site.register(Courses)
admin.site.register(Years)
admin.site.register(Colleges)
admin.site.register(Location)
