
from django.template import RequestContext
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404, redirect

from super_archives import queries
from super_archives.forms import UserCreationForm, UserUpdateForm
from super_archives.models import Message, Thread, UserProfile, EmailAddress


def home(request):
    """Index page view"""
    
    latest_threads = queries.get_latest_threads()
    hotest_threads = queries.get_voted_threads()
    
    template_data = {
        'hotest_threads': hotest_threads[:6],
        'latest_threads': latest_threads[:6],
    }
    return render_to_response('home.html', template_data, 
                              context_instance=RequestContext(request))
                              

def signup(request):

    # If the request method is GET just return the form
    if request.method == 'GET':
        form = UserCreationForm()
        return render_to_response('signup-form.html', {'form': form}, 
                                  RequestContext(request))

    # If the request method is POST try to store data
    form = UserCreationForm(request.POST)
    
    # If there is validation errors give the form back to the user
    if not form.is_valid():
        return render_to_response('signup-form.html', {'form': form}, 
                                  RequestContext(request))

    user = User(
        username=form.cleaned_data.get('username'),
        email=form.cleaned_data.get('email'),
        first_name=form.cleaned_data.get('first_name'),
        last_name=form.cleaned_data.get('last_name'),
    )
    user.set_password(form.cleaned_data.get('password'))
    user.save()
    
    profile = UserProfile(
        user=user,
        institution=form.cleaned_data.get('institution'),
        role=form.cleaned_data.get('role'),
        twitter=form.cleaned_data.get('twitter'),
        facebook=form.cleaned_data.get('facebook'),
        google_talk=form.cleaned_data.get('google_talk'),
        webpage=form.cleaned_data.get('webpage'),
    )
    profile.save()
    
    # Check if the user's email have been used previously 
    #   in the mainling lists to link the user to old messages  
    email_addr, created = EmailAddress.objects.get_or_create(address=user.email)
    if created:
        email_addr.real_name = user.get_full_name()

    email_addr.user = user
    email_addr.save()

    return redirect('colab.views.user_profile_username', user.username)


def user_profile(request, user, email_address=None, editable=False, form=None):
    
    if form is None:
        form = UserCreationForm()
    
    if user:
        email_addresses = user.emails.all()
    else:
        email_addresses = [email_address]
        
    if not email_address:
        email_address = email_addresses[0]

    email_addresses_ids = tuple([str(addr.id) for addr in email_addresses])

    query = """
        SELECT
            * 
        FROM
            super_archives_message
        WHERE 
            from_address_id IN (%(ids)s)
        GROUP BY
            thread_id
        ORDER BY
            received_time DESC
        LIMIT 10;
    """ % {'ids': ','.join(email_addresses_ids)}

    emails = Message.objects.raw(query)
    n_sent = Message.objects.filter(from_address__in=email_addresses).count()    

    template_data = {
        'user_profile': user.profile or None,
        'email_address': email_address,
        'emails': emails or [],
        'form': form,
        'editable': editable,
    }
    return render_to_response('user-profile.html', template_data, 
                              RequestContext(request))


@login_required
def user_profile_empty(request):
    return user_profile(request, request.user)


def user_profile_username(request, username):
    user = get_object_or_404(User, username=username)
    return user_profile(request, user)


def user_profile_emailhash(request, emailhash):
    email_addr = get_object_or_404(EmailAddress, md5=emailhash)
    return user_profile(request, email_addr.user, email_addr)


@login_required
def user_profile_edit(request, username):
    profile = get_object_or_404(UserProfile, user__username=username)
    form = UserUpdateForm(initial=model_to_dict(profile))
    
    if request.method == "GET":
        return user_profile(request, profile.user, editable=True, form=form)

    form = UserUpdateForm(request.POST)
    if not form.is_valid():
        return user_profile(request, profile.user, editable=True, form=form)

    profile.institution = form.cleaned_data.get('institution')
    profile.role = form.cleaned_data.get('role')
    profile.twitter = form.cleaned_data.get('twitter')
    profile.facebook = form.cleaned_data.get('facebook')
    profile.google_talk = form.cleaned_data.get('google_talk')
    profile.webpage = form.cleaned_data.get('webpage')
    profile.save()
    
    return redirect('colab.views.user_profile_username', profile.user.username)
    