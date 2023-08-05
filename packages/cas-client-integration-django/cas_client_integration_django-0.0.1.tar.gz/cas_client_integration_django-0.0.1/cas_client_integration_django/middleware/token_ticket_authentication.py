# -*- coding: UTF-8 -*-

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.conf import settings

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

import time
from jwcrypto import common, jwk, jwt, jwe


def VerifySSOToken(ssoToken):
    if len(ssoToken.split()) != 2:
        return '', False

    # prefix = ssoToken.split()[0]
    token = ssoToken.split()[1]

    try:
        key = jwk.JWK(**{'k': common.base64url_encode(settings.CENTRAL_AUTHENTICATION_SERVICE['SIGNING_KEY']), 'kty': 'oct'})
        jwtToken = jwt.JWT(jwt=token, key=key)
    except:
        return '', False

    try:
        key = jwk.JWK(**{"k": settings.CENTRAL_AUTHENTICATION_SERVICE['ENCRYPTION_KEY'], "kty": "oct"})
        jweToken = jwe.JWE()
        jweToken.deserialize(common.base64url_decode(jwtToken.claims).decode('utf-8'))
        jweToken.decrypt(key)
    except:
        return '', False
    finally:
        payload = common.json_decode(jweToken.payload)
        username = payload['sub']
        if int(time.time()) > payload['exp']:
            return username, True

    return username, False


class TokenTicketAuthentication(MiddlewareMixin):
    def process_request(self, request):
        pass

    def process_view(self, request, view_func, view_args, view_kwargs):
        cas_address = settings.CENTRAL_AUTHENTICATION_SERVICE['ADDRESS']
        service = request.scheme + '://' + request.get_host() + request.path
        # service = settings.CENTRAL_AUTHENTICATION_SERVICE['CALLBACK']

        if request.method == 'GET' and 'ticket' in request.GET and len(request.GET['ticket'].split('.')) == 3:
            request.session['sso-token'] = 'JWT ' + request.GET['ticket']

        if 'sso-token' in request.session:
            username, expired = VerifySSOToken(request.session['sso-token'])
            if not username or expired:
                del request.session['sso-token']
                # request.session.modified = True
                return HttpResponseRedirect(cas_address + "/login?service=" + service)
            request.session['sso-username'] = username
            return None

        if 'HTTP_AUTHORIZATION' in request.META:
            username, expired = VerifySSOToken(request.META['HTTP_AUTHORIZATION'])
            if not username:
                return HttpResponse("Invalid token", status=401)
            if expired:
                return HttpResponse("Token expired", status=401)
            request.session['sso-username'] = username
            return None

        return HttpResponseRedirect(cas_address + "/login?service=" + service)

    def process_response(self, request, response):
        return response
