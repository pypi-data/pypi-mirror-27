<h1> Django-AB-project </h1>
<p>Here is my first package for <b>Django</b>. I tried to write it so that it would be easy for you to use this package.</p>

<p>It provide four function in utils.py and some models in models.py.</p>
<p>This would be easy to used this package with Generic views in Django, but this can be work properly in methods, just used another technic.</p>

(You can read about Generic Views in Django here - https://docs.djangoproject.com/en/1.11/topics/class-based-views/)

<h2>How to install?</h2>
  1. Use pip to download this package - <b><i>pip install django-AB-project</i></b>
  <br>
  2. Add <i>'ab',</i> to <b>INSTALLED_APPS</b> in settings.py
  <br>
  3. Configure your sessions - set in settings.py at the end of file (or where you want): 
  <br>
    В В В В <b><i>SESSION_EXPIRE_AT_BROWSER_CLOSE</i> = True</b>
  <br>
    В В В В <b><i>SESSION_COOKIE_AGE</i> = 60 * 60 * 24</b>
  <br>
  In first line, if <b>True</b> sessions will be destroyed after browser close.
  In second case means sessions will be destroyed after 24 hours.
  <br>
  You can edit this lines if you need.
  <br>
  4. Run <b><i>python manage.py makemigrations</i></b>, and <b><i>python manage.py migrate</i></b>
  <br>
  5. Run server (<i>python manage.py runserver</i>) and go to the admin page. If you see new line named <i>"Ab_Split_Testing"</i> and can click on them without error page - Congratulation! You successfully installed this package.

<h2>How to use?</h2>
<i>(Generic views version)</i>
<p></p>

