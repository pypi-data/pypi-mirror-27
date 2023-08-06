from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render_to_response
import requests
from django.http import HttpResponseRedirect
from SweetPy.func_plus import FuncHelper


from django.contrib.auth import logout
from django.contrib.auth import authenticate, login



class anon_geely_sso(APIView):
    def get(self, request, format=None):
        """
        登陆跳转信息
        """
        if request.GET:
            ticket = request.GET.get('ticket', None)
            redirect_url = request.GET.get('redirectUrl', None)
            if ticket:
                result = requests.get('http://10.86.96.40:14108/sso/token/' + ticket)
                json_data = FuncHelper.json_to_dict(result.text)
                if json_data['data']:
                    _userName = json_data['data']['userName']
                    _mobile = json_data['data']['mobile']
                    _empNo = json_data['data']['empNo']
                    _domainAccount = json_data['data']['domainAccount']
                    _userId = json_data['data']['userId']
                    from django.contrib.auth.models import User
                    # user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
                    try:
                        user = User.objects.get(username=_domainAccount)
                    except Exception as e:
                        user = None
                    authuser = None
                    if user:
                        # user.employee.chinese_name = _userName
                        authuser = authenticate(request,username=_domainAccount,password=_domainAccount)
                    else:
                        user = User.objects.create_user(_domainAccount,_domainAccount, _domainAccount)
                        from .models import Employee
                        employee = Employee()
                        employee.user = user
                        employee.chinese_name = _userName
                        employee.mobile = _mobile
                        employee.domain_account = _domainAccount
                        employee.emp_no = _empNo
                        employee.save()
                        authuser = authenticate(request, username=_domainAccount, password=_domainAccount)

                    if user is not None:
                        login(request, user)
                        request.session.set_expiry(0)
                    # user = authenticate(username='john', password='secret')

                    if redirect_url:
                        return HttpResponseRedirect(redirect_url)
        return HttpResponseRedirect('/')

class anon_geely_sso_login(APIView):
    sso_url = None
    def get(self, request, format=None):
        redirect_url = request.query_params['next']
        _host = request.get_host()
        redirect_url = 'http://' + _host + '/'
        redirect_url_en = FuncHelper.quote(redirect_url)
        result = HttpResponseRedirect(anon_geely_sso_login.sso_url + '?redirectUrl=' + redirect_url_en)
        return result

class anon_geely_sso_logout(APIView):
    sso_url = None
    def get(self, request, format=None):
        logout(request)
        _host = request.get_host()
        redirect_url = 'http://' + _host + '/'
        result = HttpResponseRedirect(redirect_url)
        return result

from django.conf.urls import RegexURLPattern
from django import conf
from django.conf import settings
from django.core.checks.urls import check_resolver
from django.core.checks.registry import register, Tags


anon_geely_sso_regex = RegexURLPattern('^anon/geely-sso/login/success$', anon_geely_sso.as_view())
anon_geely_sso_login_regex = RegexURLPattern('^anon/geely-sso/login$', anon_geely_sso_login.as_view())
anon_geely_sso_logout_regex = RegexURLPattern('^anon/geely-sso/logout$', anon_geely_sso_logout.as_view())

@register(Tags.urls)
def check_url_config(app_configs, **kwargs):
    if getattr(settings, 'ROOT_URLCONF', None):
        from django.urls import get_resolver
        resolver = get_resolver()
        resolver.url_patterns.append(anon_geely_sso_regex)
        resolver.url_patterns.append(anon_geely_sso_login_regex)
        resolver.url_patterns.append(anon_geely_sso_logout_regex)
        return check_resolver(resolver)
    return []
import django
django.core.checks.urls.check_url_config = check_url_config