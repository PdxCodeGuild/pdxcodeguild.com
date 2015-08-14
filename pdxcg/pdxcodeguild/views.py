from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, Context
from django.shortcuts import render_to_response, render
from django.core.mail import send_mail, BadHeaderError
from .forms import Comment, Contact, StudentIntakeForm, NewStudentApp, SkillAssessmentForm
import stripe
from django.conf import settings
from django.template.loader import render_to_string
from .models import IntroSurvey
from django.core.mail import EmailMultiAlternatives

NEXT_DAY_CLASS_DATE = 'September 14th'
NEXT_NIGHT_CLASS_DATE = 'October 14th'


def index(request):
    context = RequestContext(request)
    context_dict = {'next_night_class_date': NEXT_NIGHT_CLASS_DATE, 'next_day_class_date': NEXT_DAY_CLASS_DATE}

    return render_to_response('index.html', context_dict, context)


def guarantee(request):
    return render(request, 'guarantee.html')


def piecharttest(request):
    x = IntroSurvey.objects.all().values('mtt_530_to_830', 'ttf_530_to_830', 'mtt_1100_to_0200', 'ss_1100_to_0200',
                                         's_1100_to_0200')
    mtt_530_to_830 = []
    ttf_530_to_830 = []
    mtt_1100_to_0200 = []
    ss_1100_to_0200 = []
    s_1100_to_0200 = []

    for y in x:
        mtt_530_to_830.append(y['mtt_530_to_830'])
        ttf_530_to_830.append(y['ttf_530_to_830'])
        mtt_1100_to_0200.append(y['mtt_1100_to_0200'])
        ss_1100_to_0200.append(y['ss_1100_to_0200'])
        s_1100_to_0200.append(y['s_1100_to_0200'])

    mtt_530_to_830_sum = sum(mtt_530_to_830)
    ttf_530_to_830_sum = sum(ttf_530_to_830)
    mtt_1100_to_0200_sum = sum(mtt_1100_to_0200)
    ss_1100_to_0200_sum = sum(ss_1100_to_0200)
    s_1100_to_0200_sum = sum(s_1100_to_0200)

    xdata = ["Monday, Tuesday and Thursday 5:30-8:30", "Tuesday, Thursday and Friday 5:30-8:30", "Monday, Tuesday and Thursday 11:00-2:00", "Saturday and Sunday 11:00-2:00", "Saturdays 11:00-2:00"]
    ydata = [mtt_530_to_830_sum, ttf_530_to_830_sum, mtt_1100_to_0200_sum, ss_1100_to_0200_sum, s_1100_to_0200_sum]
    chartdata = {'x': xdata, 'y': ydata}
    charttype = "pieChart"
    chartcontainer = 'piechart_container'
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,
        }
    }
    return render(request, 'piecharttest.html', data)


def intro_scholarship(request):
    if request.method == 'POST':
        intsurv = IntroSurvey()
        intsurv.self_study = request.POST['self-study']
        intsurv.city = request.POST['city']
        intsurv.ss_1100_to_0200 = request.POST['ss-1100-200']
        intsurv.last_name = request.POST['last-name']
        intsurv.zip = request.POST['zip']
        intsurv.date_of_birth = request.POST['dob']
        intsurv.ttf_530_to_830 = request.POST['ttf-530-830']
        intsurv.s_1100_to_0200 = request.POST['s-1100-200']
        intsurv.middle_initial = request.POST['mi']
        intsurv.mtt_1100_to_0200 = request.POST['mtt-1100-200']
        intsurv.mtt_530_to_830 = request.POST['mtt-530-830']
        intsurv.phone_number = request.POST['phone']
        intsurv.state = request.POST['state']
        intsurv.programming_knowledge = request.POST['knowledge-level']
        intsurv.street_address = request.POST['address']
        intsurv.first_name = request.POST['first-name']
        intsurv.email = request.POST['email']
        intsurv.save()

        full_name = str(intsurv.first_name) + ' ' + str(intsurv.last_name)
        subject, from_email, to = '%s filled out the Intro Survey form' % full_name, 'forms@pdxcodeguild.com', \
                                  'sheri.dover@gmail.com'
        text_content = '''Name: %s
        Phone number: %s
        Email address: %s
        Go to https://pdxcodeguild.com/admin to view submission.
        ''' % (full_name, intsurv.phone_number, intsurv.email )
        html_content = 'Full name: %s<br>Phone number: %s<br>Email address: %s<br>Go to https://pdxcodeguild.com/admin ' \
                       'to view submission.' % (
                           full_name, intsurv.phone_number, intsurv.email)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return HttpResponseRedirect('/thanks/')
    return render(request, 'intro_survey.html')


def about(request):
    context = RequestContext(request)
    context_dict = {}

    return render_to_response('about.html', context_dict, context)


def advisors(request):
    context = RequestContext(request)
    context_dict = {}

    return render_to_response('advisors.html', context_dict, context)


def apply(request):
    context = RequestContext(request)
    if request.method == 'GET':
        form = Contact()
    else:
        # A POST request: Handle Form Upload
        form = Contact(request.POST)  # Bind data from request.POST into a PostForm

        # If data is valid, proceeds to create a new post and redirect the user
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            phone_number = form.cleaned_data['phone_number']
            email_address = form.cleaned_data['email_address']
            best_contact = form.cleaned_data['best_contact']
            message = form.cleaned_data['message']

            subject, from_email, to = '%s filled out the Interested form' % full_name, 'forms@pdxcodeguild.com', \
                                      'sheri.dover@gmail.com'
            text_content = '''Name: %s
            Phone number: %s
            Email address: %s
            How do you prefer to be contacted? %s
            Message: \n %s''' % (full_name, phone_number, email_address, best_contact, message)
            html_content = 'Full name: %s<br>Phone number: %s<br>Email address: %s<br>How do you prefer to be ' \
                           'contacted? %s<br>Message:<br> %s' % (
                               full_name, phone_number, email_address, best_contact, message)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return HttpResponseRedirect('/thanks/')
    context_dict = {'form': form}

    return render_to_response('apply.html', context_dict, context)


def intro_apply(request):
    context = RequestContext(request)
    if request.method == 'POST':
        stripe.api_key = settings.STRIPE_SECRET
        token = request.POST['stripeToken']
        amount = 45000
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        zip_code = request.POST['zip']
        goals = request.POST['goals']

        try:
            charge = stripe.Charge.create(
                amount=amount,  # amount in cents
                currency="usd",
                card=token,
                description="PDX Code Guild's Intro to Programming"
            )

            name = charge['card']['name']
            payment = charge['amount'] / 100
            context_dict = {'name': name, 'payment': payment}
            from django.core.mail import EmailMultiAlternatives, EmailMessage
            # ################################################
            # Email to Students
            # ################################################
            subject, from_email, to = "Hi %s, thanks for signing up for our Intro to Programming class!" % name, \
                                      "codeguildpayments@pdxcodeguild.com", \
                                      email
            html_content = render_to_string('introclassemail.html', context_dict)
            msg_student = EmailMessage(subject, html_content, from_email, [to])
            msg_student.content_subtype = 'html'
            msg_student.send()

            #################################################
            # Email to Staff
            #################################################
            # TODO make sure this is sending email to admin.
            subject, from_email, to = '%s has signed up for the Intro to Programming class.' % name, 'forms@pdxcodeguild.com', \
                                      'chris@pdxcodeguild.com'
            text_content = '''Name: %s
            Email address: %s
            Phone number: %s
            Address: \n
            %s
            %s, %s %s
            What are your goals for this class?\n
            %s
            ''' % (name, email, phone, address, city, state, zip_code, goals)
            html_content = 'Name: %s <br>' \
                           'Email address: %s<br>' \
                           'Phone number: %s<br>' \
                           'Address: <br>' \
                           '%s<br>' \
                           '%s, %s %s<br>' \
                           'What are your goals for this class?<br>' \
                           '%s' % (name, email, phone, address, city, state, zip_code, goals)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return render(request, 'payment_thanks.html', context_dict)
        except stripe.CardError, e:
            # The card has been declined
            pass

    context_dict = {'stripe_key': settings.STRIPE_PUBLISHABLE}

    return render_to_response('intro_apply.html', context_dict, context)


def intake(request):
    context = RequestContext(request)
    if request.method == 'GET':
        form = StudentIntakeForm()
    else:
        # A POST request: Handle Form Upload
        form = StudentIntakeForm(request.POST)  # Bind data from request.POST into a PostForm

        # If data is valid, proceeds to create a new post and redirect the user
        if form.is_valid():
            name = form.cleaned_data['name']
            email_address = form.cleaned_data['email_address']
            git_hub = form.cleaned_data['git_hub']
            student_bio = form.cleaned_data['student_bio']
            student_goals = form.cleaned_data['student_goals']
            form.save()
            from django.core.mail import EmailMultiAlternatives

            subject, from_email, to = '%s filled out the student intake form' % name, 'forms@pdxcodeguild.com', \
                                      'chris.charles.jones@gmail.com',
            text_content = '''Name: %s
            Email address: %s
            GitHub URL: %s
            Student Bio: \n %s
            Student Goals: \n %s''' % (name, email_address, git_hub, student_bio, student_goals)
            html_content = 'Name: %s<br>Email address: %s<br>GitHub URL: %s<br>Student Bio<br>' \
                           '%s<br>Student Goals:<br>%s' % (
                               name, email_address, git_hub, student_bio, student_goals
                           )
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return HttpResponseRedirect('/thanks/')
    context_dict = {'form': form}

    return render_to_response('intake.html', context_dict, context)


def contact(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = Contact()
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            phone_number = form.cleaned_data['phone_number']
            email_address = form.cleaned_data['email_address']
            best_contact = form.cleaned_data['best_contact']
            message = form.cleaned_data['message']

            from django.core.mail import EmailMultiAlternatives

            subject, from_email, to = '%s filled out the Contact form' % full_name, 'forms@pdxcodeguild.com', \
                                      'sheri.dover@gmail.com'
            text_content = '''Name: %s
            Phone number: %s
            Email address: %s
            How do you prefer to be contacted? %s
            Message: \n %s''' % (full_name, phone_number, email_address, best_contact, message)
            html_content = 'Full name: %s<br>Phone number: %s<br>Email address: %s<br>How do you prefer to be ' \
                           'contacted? %s<br>Message:<br> %s' % (
                               full_name, phone_number, email_address, best_contact, message)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return HttpResponseRedirect('/thanks/')
    else:

        form = Contact()
    context_dict = {'form': form}

    return render_to_response('contact.html', context_dict, context)


def faq(request):
    context = RequestContext(request)
    context_dict = {}

    return render_to_response('faq.html', context_dict, context)


def gettechnical(request):
    context = RequestContext(request)
    context_dict = {}

    return render_to_response('gettechnical.html', context_dict, context)


def individualized(request):
    context = RequestContext(request)
    context_dict = {}

    return render_to_response('individualized.html', context_dict, context)


def jrdevbootcamp(request):
    context = RequestContext(request)
    context_dict = {'next_night_class_date': NEXT_NIGHT_CLASS_DATE, 'next_day_class_date': NEXT_DAY_CLASS_DATE}

    return render_to_response('jrdevbootcamp.html', context_dict, context)


def evening_bootcamp(request):
    context = RequestContext(request)
    context_dict = {'next_night_class_date': NEXT_NIGHT_CLASS_DATE, 'next_day_class_date': NEXT_DAY_CLASS_DATE}

    return render_to_response('evening-bootcamp.html', context_dict, context)


def partner(request):
    context = RequestContext(request)
    context_dict = {}

    return render_to_response('partner.html', context_dict, context)


def program(request):
    context = RequestContext(request)
    context_dict = {}

    return render_to_response('program.html', context_dict, context)


def sponsor(request):
    context = RequestContext(request)
    context_dict = {}

    return render_to_response('sponsor.html', context_dict, context)


def team(request):
    context = RequestContext(request)
    context_dict = {}

    return render_to_response('team.html', context_dict, context)


def thanks(request):
    context = RequestContext(request)
    context_dict = {}

    return render_to_response('thanks.html', context_dict, context)


def payment_thanks(request):
    context = RequestContext(request)
    context_dict = {}

    return render_to_response('payment_thanks.html', context_dict, context)


def value(request):
    context = RequestContext(request)
    context_dict = {}

    return render_to_response('value.html', context_dict, context)


def ppm(request):
    context = RequestContext(request)
    context_dict = {}

    return render_to_response('ppm.html', context_dict, context)


def pythonquiz(request):
    context = RequestContext(request)
    context_dict = {}

    return render_to_response('pythonquiz.html', context_dict, context)


def student_comment(request):
    context = RequestContext(request)
    if request.method == 'GET':
        form = Comment()
    else:
        # A POST request: Handle Form Upload
        form = Comment(request.POST)  # Bind data from request.POST into a PostForm

        # If data is valid, proceeds to create a new post and redirect the user
        if form.is_valid():
            name = form.cleaned_data['name']
            email_address = form.cleaned_data['email_address']
            first = form.cleaned_data['first']
            second = form.cleaned_data['second']
            third = form.cleaned_data['third']
            fourth = form.cleaned_data['fourth']
            fifth = form.cleaned_data['fifth']
            sixth = form.cleaned_data['sixth']
            seventh = form.cleaned_data['seventh']
            eighth = form.cleaned_data['eighth']
            ninth = form.cleaned_data['ninth']
            tenth = form.cleaned_data['tenth']
            message1 = form.cleaned_data['message1']
            message2 = form.cleaned_data['message2']

            from django.core.mail import EmailMultiAlternatives

            subject, from_email, to = 'A new student comment form has been filled out.', 'forms@pdxcodeguild.com', \
                                      'chris.charles.jones@gmail.com'
            text_content = '''Name: %s
            Email address: %s
            Please rate the following on a scale of 1 to 4.
            1 = Poor, 2 = Fair, 3 = Good, 4 = Excellent
            Depth of the Knowledge of the subject: %s
            Presentation Skills: %s
            Sincerity, Commitment, Regularity and Punctuality: %s
            Syllabus Coverage: %s
            Ability to Clarify doubts, teaching with relevant examples: %s
            Ability to relate the course to real life situations: %s
            Ability to generate interest: %s
            Content and length of lectures: %s
            Ability to command and control the class: %s
            Overall teacher rating: %s
            What can we do in the future to improve this class?: \n %s \n
            Is there any other suggestion or issues you would like to bring up?: \n %s
            ''' % (
                name, email_address, first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth,
                message1,
                message2)
            html_content = 'Name: %s<br>Email address: %s<br>Please rate the following on a scale of 1 to 4.<br>1 = Poor, 2 = Fair, 3 = Good, 4 = Excellent<br>Depth of the Knowledge of the subject: %s<br>Presentation Skills: %s<br>Sincerity, Commitment, Regularity and Punctuality: %s<br>Syllabus Coverage: %s<br>Ability to Clarify doubts, teaching with relevant examples: %s<br>Ability to relate the course to real life situations: %s<br>Ability to generate interest: %s<br>Content and length of lectures: %s<br>Ability to command and control the class: %s<br>Overall teacher rating: %s<br>What can we do in the future to improve this class?: <br>%s <br>Is there any other suggestion or issues you would like to bring up?: <br>%s' % (
                name, email_address, first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth,
                message1,
                message2)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return HttpResponseRedirect('/thanks/')
    context_dict = {'form': form}

    return render_to_response('comment.html', context_dict, context)


def student(request):
    context = RequestContext(request)
    context_dict = {}

    return render_to_response('student.html', context_dict, context)


def student_apply(request):
    context = RequestContext(request)
    if request.method == 'GET':
        form = NewStudentApp()
    else:
        # A POST request: Handle Form Upload
        form = NewStudentApp(request.POST)  # Bind data from request.POST into a PostForm

        # If data is valid, proceeds to create a new post and redirect the user
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/thanks/')
    context_dict = {'form': form}

    return render_to_response('student_apply.html', context_dict, context)


def skill_assessment(request):
    context = RequestContext(request)
    if request.method == 'GET':
        form = SkillAssessmentForm()
    else:
        # A POST request: Handle Form Upload
        form = SkillAssessmentForm(request.POST)  # Bind data from request.POST into a PostForm

        # If data is valid, proceeds to create a new post and redirect the user
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/thanks/')
    context_dict = {'form': form}

    return render_to_response('skillassessment.html', context_dict, context)
