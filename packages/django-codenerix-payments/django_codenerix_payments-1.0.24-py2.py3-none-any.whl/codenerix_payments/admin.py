# -*- coding: utf-8 -*-
#
# django-codenerix-payments
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
from codenerix_payments.models import Currency, PaymentRequest, PaymentConfirmation, PaymentAnswer

admin.site.register(Currency)
admin.site.register(PaymentRequest)
admin.site.register(PaymentConfirmation)
admin.site.register(PaymentAnswer)
