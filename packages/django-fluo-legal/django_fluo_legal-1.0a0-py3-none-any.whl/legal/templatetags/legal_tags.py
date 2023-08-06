# Copyright (C) 2007-2017, Raffaele Salmaso <raffaele@salmaso.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from django import template
from django.template.loader import render_to_string

register = template.Library()


class CookieLawTag(template.Node):
    """
    Displays cookie law banner only if user has not dismissed it yet.
    """

    def __init__(self, banner, js, css, id, name):
        self.banner = banner
        self.js = js
        self.css = css
        self.id = id
        self.name = name

    def render(self, context):
        name = self.name.resolve(context)
        if context['request'].COOKIES.get(name, False):
            return ''

        ctx = {
            'legal_cookielaw_banner': self.banner.resolve(context),
            'legal_cookielaw_name': name,
            'legal_cookielaw_banner_id': self.id.resolve(context),
            'legal_cookielaw_js': self.js.resolve(context),
            'legal_cookielaw_css': self.css.resolve(context),
        }
        return render_to_string('legal/cookielaw_tag.html', ctx)


@register.tag
def cookielaw(parser, token):
    """
    {% cookielaw banner='' js='' css='' id='' name='' %}
    where
    - banner: html
    - js: customized js
    - css: customized css
    - id: the banner id to remove
    - name: the cookie name
    """
    bits = token.split_contents()[1:]
    kwargs = {
        'banner': template.Variable("'legal/cookielaw.html'"),
        'name': template.Variable("'legal_cookielaw_accepted'"),
        'id': template.Variable("'CookielawBanner'"),
        'js': template.Variable("'legal/cookielaw.js'"),
        'css': template.Variable("'legal/cookielaw.css'"),
    }
    if len(bits) > 5:
        raise template.TemplateSyntaxError('cookielaw error: must accept max 5 parameters')
    for bit in bits:
        args = bit.split('=')
        kwargs[args[0]] = template.Variable(args[1])
    return CookieLawTag(**kwargs)
