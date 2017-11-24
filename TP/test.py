from django.db import models
from django.contrib.auth.models import User
from tutoria.models import *

MyTutors.objects.create()

#dummy profile user for university display
TutorProfile.objects.create(university="HKU")
TutorProfile.objects.create(university="PKU")
TutorProfile.objects.create(university="THU")
TutorProfile.objects.create(university="HKUST")
TutorProfile.objects.create(university="HKUCH")

#Course in system
Course.objects.create(university="HKU",code="HKUCOMP1111")
Course.objects.create(university="HKU",code="HKUCOMP1112")
Course.objects.create(university="HKU",code="HKUCOMP1113")
Course.objects.create(university="HKU",code="HKUCOMP1114")
Course.objects.create(university="HKU",code="HKUCOMP1115")
Course.objects.create(university="HKU",code="HKUCOMP1116")

Course.objects.create(university="PKU",code="PKUCOMP1111")
Course.objects.create(university="PKU",code="PKUCOMP1112")
Course.objects.create(university="PKU",code="PKUCOMP1113")
Course.objects.create(university="PKU",code="PKUCOMP1114")
Course.objects.create(university="PKU",code="PKUCOMP1115")
Course.objects.create(university="PKU",code="PKUCOMP1116")

Course.objects.create(university="THU",code="THUCOMP1111")
Course.objects.create(university="THU",code="THUCOMP1112")
Course.objects.create(university="THU",code="THUCOMP1113")
Course.objects.create(university="THU",code="THUCOMP1114")
Course.objects.create(university="THU",code="THUCOMP1115")
Course.objects.create(university="THU",code="THUCOMP1116")

Course.objects.create(university="HKUST",code="HKUSTCOMP1111")
Course.objects.create(university="HKUST",code="HKUSTCOMP1112")
Course.objects.create(university="HKUST",code="HKUSTCOMP1113")
Course.objects.create(university="HKUST",code="HKUSTCOMP1114")
Course.objects.create(university="HKUST",code="HKUSTCOMP1115")
Course.objects.create(university="HKUST",code="HKUSTCOMP1116")

Course.objects.create(university="HKUCH",code="HKUCHCOMP1111")
Course.objects.create(university="HKUCH",code="HKUCHCOMP1112")
Course.objects.create(university="HKUCH",code="HKUCHCOMP1113")
Course.objects.create(university="HKUCH",code="HKUCHCOMP1114")
Course.objects.create(university="HKUCH",code="HKUCHCOMP1115")
Course.objects.create(university="HKUCH",code="HKUCHCOMP1116")


Tag.objects.create(content="C")
Tag.objects.create(content="Computer Science")
Tag.objects.create(content="C++")
Tag.objects.create(content="Java")
Tag.objects.create(content="Python")
Tag.objects.create(content="Web")
Tag.objects.create(content="Django")
Tag.objects.create(content="Software Engineering")
