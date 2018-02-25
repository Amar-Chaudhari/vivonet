# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from main.models import *

from django.contrib import admin

# Register your models here.
admin.site.register(Customer)
admin.site.register(Intent_Data)
admin.site.register(Intent_Path_Data)