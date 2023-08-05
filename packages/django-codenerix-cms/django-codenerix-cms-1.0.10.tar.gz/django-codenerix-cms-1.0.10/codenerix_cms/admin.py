# -*- coding: utf-8 -*-
#
# django-codenerix-cms
#
# Copyright 2017 Centrologic Computational Logistic Center S.L.
#
# Project URL : http://www.codenerix.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.contrib import admin
from django.conf import settings

from codenerix_cms.models import Slider, SliderElement, StaticheaderElement, Staticheader, MODELS, StaticPage, TemplateStaticPage


admin.site.register(Slider)
admin.site.register(SliderElement)
admin.site.register(Staticheader)
admin.site.register(StaticheaderElement)
admin.site.register(StaticPage)
admin.site.register(TemplateStaticPage)


for info in MODELS:
    model = info[1]
    for lang_code in settings.LANGUAGES_DATABASES:
        query = "from codenerix_cms.models import {}Text{}\n".format(model, lang_code)
        query += "admin.site.register({}Text{})\n".format(model, lang_code)
        exec(query)
