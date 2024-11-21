from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from ask_a_woman.account.forms import CustomUserChangeForm, CustomUserForm
from ask_a_woman.account.models import Profile


UserModel = get_user_model()

class ProfileInLine(admin.StackedInline):
    model = Profile


@admin.register(UserModel)
class UserAdmin(BaseUserAdmin):
    model = UserModel
    inlines = [ProfileInLine]

    form = CustomUserChangeForm
    add_form = CustomUserForm

    list_display = ('username', 'email')

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )

    fieldsets = (
        ('Credentials', {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login',)})
    )

    filters = ['username']

    ordering = ['username']




