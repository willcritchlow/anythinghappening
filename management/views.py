from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from news.models import NewsCheck
from datetime import datetime, timedelta

@login_required
def manage(request):
    if request.user.is_staff:
        users = User.objects.filter(is_active=True).exclude(is_staff=True)
        count = len(users)
        today = datetime.now()
        last_week = today + timedelta(-7)
        nc_week = NewsCheck.objects.filter(time__gt= last_week)

        active_users = {}
        active_count = 0
        for check in nc_week:
            if not check.user.is_staff:
                if check.user in active_users:
                    active_users[check.user]['count'] += 1
                else:
                    active_users[check.user] = {}
                    active_users[check.user]['count'] = 1
                    active_count += 1

        return render_to_response('management/index.html', {'user': request.user, 'count': count, 'active_count': active_count, 'active_users': active_users})
    else:
        return redirect('index')
