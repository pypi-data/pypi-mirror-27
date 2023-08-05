=====
mailchimp_sender_package
=====


Quick start
-----------
0. Install package::
	pip install mailchimpworker

1. Add "mailchimp_sender_package" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'mailchimpworker',
        ...
    ]

2. Make migrations::
	python manage.py makemigrations mailchimpworker
	python manage.py migrate

3. Add the MAILCHIMP_API_KEY in settings.py::
	MAILCHIMP_API_KEY = 'YOUR API KEY'

4. Create into folder with settings.py, wsgi.py and etc. file 'celery.py' with this content::

	from __future__ import absolute_import, unicode_literals
	import os
	from celery import Celery
	from celery.schedules import crontab

	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "[proj_name].settings") # insert project name instead of "[proj_name]"

	app = Celery('[proj_name]') # insert project name instead of "[proj_name]"
	app.config_from_object('django.conf:settings', namespace='CELERY')
	app.conf.broker_url = 'redis://localhost:6379/0'
	app.conf.beat_schedule = {
	    'mailchimpworker.tasks.send_new_emails': {
	        'task': 'mailchimpworker.tasks.send_new_emails',
	        'schedule': crontab(minute=0),
	        'args': ([YOUR_LIST_ID], [YOUR_CATEGORY_ID], [YOUR_INTEREST_ID]) # that should be strings, not lists
	    },
	}
	app.autodiscover_tasks()

5. Write view for creating objects of model Subscriber and bind him with forms. Example of view::

	from django.shortcuts import render
	from mailchimpworker.models import Subscriber

	def new_subscriber(request):
	    data_email = request.POST.get('EMAIL')
	    unique_check = Subscriber.objects.filter(email=data_email)
	    if not len(unique_check):
	        Subscriber.objects.create(email=data_email)
	    return render(request, '[path_to_"thanks"_template].html', {})

P.S. To run scripts correctly, you need to run Celery-worker:
celery -A [proj_name] worker -l info -B
