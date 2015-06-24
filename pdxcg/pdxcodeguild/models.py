from django.db import models
from django.core.validators import RegexValidator
import datetime

class NewStudentApplication(models.Model):
    # regex for valid international phone number
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits \
                                 allowed.")

    first_name = models.CharField(max_length=255)
    middle_initial = models.CharField(max_length=1)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(auto_now=False)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip = models.IntegerField(max_length=5)
    applied_before = models.CharField(max_length=255)
    if_yes_app = models.DateField(auto_now=False)
    attended_before = models.CharField(max_length=255)
    if_yes_grad = models.CharField(max_length=255)
    if_no_grad = models.TextField(max_length=255)
    phone_number = models.CharField(validators=[phone_regex], blank=True, max_length=15)
    message_number = models.CharField(validators=[phone_regex], blank=True, max_length=15)
    cell_number = models.CharField(validators=[phone_regex], blank=True, max_length=15)
    email = models.EmailField()
    us_citizen = models.CharField(max_length=255)

    # Emergency Contact Information

    contact_name = models.CharField(max_length=255)
    contact_address = models.CharField(max_length=255)
    contact_city = models.CharField(max_length=255)
    contact_state = models.CharField(max_length=255)
    contact_zip = models.CharField(max_length=255)
    contact_number = models.CharField(validators=[phone_regex], blank=True, max_length=15)


class StudentIntake(models.Model):
    name = models.CharField(max_length=255)
    email_address = models.EmailField(max_length=255)
    git_hub = models.URLField(max_length=255)
    instructor_name = models.CharField(max_length=255)
    student_bio = models.TextField(max_length=2000)
    student_goals = models.TextField(max_length=2000)


class SkillAssessment(models.Model):
    name = models.CharField(max_length=255)
    email_address = models.EmailField(max_length=255)
    instructor_name = models.CharField(max_length=255)
    date = models.DateField()
    skill_level = models.CharField(max_length=255)

    # General Skills
    management = models.CharField(max_length=255)
    internals = models.CharField(max_length=255)
    command_line = models.CharField(max_length=255)
    networking = models.CharField(max_length=255)
    written_communication = models.CharField(max_length=255)
    math = models.CharField(max_length=255)
    logic = models.CharField(max_length=255)
    spreadsheets = models.CharField(max_length=255)
    user_databases = models.CharField(max_length=255)
    editors_ide = models.CharField(max_length=255)
    html = models.CharField(max_length=255)
    css = models.CharField(max_length=255)

    # Code Skills
    variables_datatypes = models.CharField(max_length=255)
    flow_control = models.CharField(max_length=255)
    functions = models.CharField(max_length=255)
    classes_objects = models.CharField(max_length=255)
    design_patterns = models.CharField(max_length=255)
    debugging = models.CharField(max_length=255)
    source_control = models.CharField(max_length=255)
    profiling_performance_optimization = models.CharField(max_length=255)
    what_do_you_hope_we_cover = models.TextField(max_length=2000)
    what_skills_do_you_want_to_acquire = models.TextField(max_length=2000)
    projects_applications_in_mind = models.TextField(max_length=2000)


class IntroSurvey(models.Model):
    # regex for valid international phone number
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits \
                                 allowed.")

    first_name = models.CharField(max_length=255)
    middle_initial = models.CharField(max_length=1)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip = models.IntegerField(max_length=20)
    email = models.EmailField()
    phone_number = models.CharField(validators=[phone_regex], blank=True, max_length=15)
    programming_knowledge = models.TextField(max_length=2000)
    self_study = models.TextField(max_length=2000)
    mtt_530_to_830 = models.IntegerField(max_length=1)
    ttf_530_to_830 = models.IntegerField(max_length=1)
    mtt_1100_to_0200 = models.IntegerField(max_length=1)
    ss_1100_to_0200 = models.IntegerField(max_length=1)
    s_1100_to_0200 = models.IntegerField(max_length=1)

    def __unicode__(self):
            return self.first_name
































