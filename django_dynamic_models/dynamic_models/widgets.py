from django.utils.safestring import mark_safe
from django.forms import TextInput


class CalendarWidget(TextInput):
    class Media:
        css = {'all': ('/static/css/datepicker.css',)
               }
        js = ('/static/js/bootstrap-datepicker.js',
              '/static/js/datepicker_activation.js',
              )

    def render(self, name, value, attrs=None):

        id_selector = attrs.get('id')
        #if id_selector:
        #    name = str(id_selector).sp

        return mark_safe(u'<div class=\"input-append date\" '
                         u'id=\"dpYears\" data-date=\"2012-12-02\" '
                         u'data-date-format=\"yyyy-mm-dd\" '
                         u'data-date-viewmode=\"years\">'
                         u'<input class = \"dp\" type=\"text\" '
                         u'id=\"birth\"  name=\"birthday\" value=\"%s\">'
                         u'</div>' %
                         value
                         )