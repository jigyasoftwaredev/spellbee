"""spellbee URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from core.views import save_audio,contests,students,home,junior_spellbee,senior_spellbee,display_all_junior_spellbee
from core.views import phase1_results,check_total_score,select_phase_junior,junior_phase1,update_next_round
from core.views import senior_phase1,senior_phase1_results,check_total_score_senior,show_intro,update_phase_results_phase_questions
from django.conf.urls.static import  static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^words/',save_audio),
    url(r'^contests/',contests),
    url(r'^students/',students),
    url(r'^junior_spellbee/',junior_spellbee),
    url(r'^senior_spellbee/',senior_spellbee),
    url(r'^junior_phase2/',display_all_junior_spellbee),
    url(r'^junior_phase1/',junior_phase1),
    url(r'^senior_phase1/',senior_phase1),
    url(r'^update_phase1_senior_results/',senior_phase1_results),
    url(r'^update_phase1_junior_results/',phase1_results),
    url(r'^check_total_score/',check_total_score),
    url(r'^check_total_score_senior/',check_total_score_senior),
    url(r'^select_phase_junior/',select_phase_junior),
    url(r'^update_next_round/',update_next_round),
    url(r'^intro/',show_intro),
    url(r'^erase_results/',update_phase_results_phase_questions),
    url(r'^$',home),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
