from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, Sex, Authority


# Register your models here.
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'nickname', 'school', 'email', 'is_staff', 'is_active', 'is_superuser')

    def nickname(self, obj):
        return obj.profile.nickname

    def school(self, obj):
        return obj.profile.school

    nickname.short_description = '昵称'  # 后台将nickname显示成“昵称”


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'sex')


@admin.register(Authority)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'administrator', 'write', 'read')
