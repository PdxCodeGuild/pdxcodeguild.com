from models import StudentIntake, NewStudentApplication, SkillAssessment, IntroSurvey
from forms import StudentIntakeForm
from django.contrib import admin

from django.forms import ModelForm, Textarea


class StudentIntakeAdmin(admin.ModelAdmin):
    list_display = ['name', 'email_address', 'instructor_name']
    fieldsets = ((None, {
            'fields': ('name', 'email_address', 'instructor_name', 'git_hub')
        }),
        ('Advanced options', {
            'classes': ('wide',),
            'fields': ('student_bio', 'student_goals')
        }),
    )


class SkillAssessmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'instructor_name', 'date']


class IntroSurveyAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name']

admin.site.register(StudentIntake, StudentIntakeAdmin)
admin.site.register(NewStudentApplication)
admin.site.register(SkillAssessment, SkillAssessmentAdmin)
admin.site.register(IntroSurvey, IntroSurveyAdmin)