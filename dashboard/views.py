from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.views.generic import ListView
from .models import Alarm, Comment
from .forms import EmailAlarmForm, CommentForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class AlarmListView(LoginRequiredMixin, ListView):
    """
    Alternative post list view
    """
    queryset = Alarm.not_ack_alarm.all()
    context_object_name = 'alarms'
    template_name = 'dashboard/index.html'

"""def index(request):
    alarms = Alarm.not_ack_alarm.all()
    return render(request, 'dashboard/index.html', {'alarms': alarms})"""


@login_required
def alarm_detail(request, id):
    alarm = get_object_or_404(Alarm, id=id, ack=False)
    # List of active comments for this post
    comments = alarm.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()

    return render(request, 'dashboard/detail.html', {'alarm': alarm, 'comments': comments, 'form': form})

@login_required
def alarm_share(request, id):
    # Retrieve alarm by id
    alarm = get_object_or_404(Alarm, id=id, ack=False)
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailAlarmForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            subject = f"{cd['name']} recommends you read " f"{str(alarm.type.title)}"
            message = f"Alarm: {alarm.type.title}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            # print(subject, message, 'noc@xyz.com', [cd['to']])
            # send_mail(subject, message, 'your_account@gmail.coom', [cd['to']])
            sent = True
    else:
        form = EmailAlarmForm()
    return render(request, 'dashboard/share.html', {'alarm': alarm, 'form': form, 'sent': sent})


@login_required
@require_POST
def alarm_comment(request, alarm_id):
    alarm = get_object_or_404(Alarm, id=alarm_id, ack=False)
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.alarm = alarm
        if request.user.is_authenticated:
                # Assign the user to the comment
                comment.user = request.user
                # Save the comment to the database
                comment.save()
        else:
            # Optionally, handle the case where the user is not logged in
            return redirect('dashboard:index')
        # Save the comment to the database
        comment.save()
    return render(request, 'dashboard/comment.html', {'alarm': alarm, 'form': form, 'comment': comment})
