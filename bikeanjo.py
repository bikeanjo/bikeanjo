#!/usr/bin/env python
from importd import d
import time

d(  # configure django
    DEBUG=True,
    SMART_RETURN=True,
    INSTALLED_APPS=['debug_toolbar', 'django_extensions'],
    STATICFILES_DIRS=['static', 'bower_components'],
)


@d('/', name='home')
def home(request):
    import time
    return 'home.html', {'msg': time.time(),
                         'objs': ''}


@d('/view_template/<word:name>', name='view_template')  # named urls
def real_index(request, name):
    return name+'.html', {'msg': time.time()}


if __name__ == '__main__':
    d.main()
