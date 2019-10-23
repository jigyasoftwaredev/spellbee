# Author: Integra
# Dev: Partha(Ref)

import hashlib, re, sys, inspect
from datetime import datetime 

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout
from django.utils.translation import activate
from django.utils.deprecation import MiddlewareMixin
from django.http import Http404

# class If_Session_Idle_Timeout:
#     '''middleware that checks for session idle timeout'''
#     def process_request(self, request):
#         path = request.get_full_path()
#         temp_path=request.path
#         try:
#             try:
#                  last_activity=request.session['last_touch']
#             except:
#                  request.session['last_touch'] = datetime.now()
#                  last_activity = request.session['last_touch']
#             now=datetime.now()
#             expiry_time=settings.SESSION_TIMEOUT
#             if (now-last_activity).total_seconds() > expiry_time:
#                 logout(request)
#                 return HttpResponseRedirect('/login/')
#             else:
#                 request.session['last_touch']=datetime.now()
#                 return
#         except:
#             return HttpResponseRedirect('/login/')


    

# class LoginRequired(MiddlewareMixin):

#     def process_request(self, request):
#         if request.user.is_authenticated():
#             if request.path == "/login/":
#                 return HttpResponseRedirect("/")

#         else:
#             if request.path == "/login/" or request.path == '/register/':
#                 return
#             return HttpResponseRedirect('/login/')
class LoginRequired(MiddlewareMixin):

    def process_request(self, request):
    	# import pdb;pdb.set_trace()
        if request.user.is_authenticated():
			# import pdb;pdb.set_trace()
			return
			# if request.user.role!='Administrator':
			# 	if accessible_urls(request):
			# 		return
			# 	else:
			# 		raise Http404

					# HttpResponse('NOT ALLOWED IF YOU TRY TO ACCESS IT AGAIN YOU ARE OVER BETTER SING A COVER')
        else:
            if request.path == "/login/":
                return
            return HttpResponseRedirect('/login/')
