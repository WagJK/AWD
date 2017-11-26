# Tutoria Platform
An elegant tutor finding platform designed for tutors and students, which is devoloped with Django and Bootstrap.

### Developers
[Feng Xiyang](https://github.com/andyfengHKU)<br>
[Guo Hongpeng](https://github.com/TTTChairman)<br>
[Wang Jikun](https://github.com/WagJK)<br>
[Zhang Qiping](https://github.com/LostCoding)<br>


### Attentions (Ver 1.00)
1. Avatar is not yet supported in personal profile, default pictures is displayed currently. It will be added in the next iteration.

2. Coupon code distribution and usage is not supported yet. It will be added in the next iteration.

3. Switching between different login types (i.e. Student, tutor, both student and tutor) is not supported yet. We don't plan to support this functionality in the future, but we plan to allow user to delete their account in the next iteration.

4. Switching between different tutor types (i.e. Contract, Private) is allowed only when a tutor has no timeslots activated for students to book. But he/she can have already booked timeslots.

5. Real transactions are simulated in place of payment gateways. Currently the payment system is a system of internal wallets and a simple interface to support demos and testing.

6. When a user is adding courses and tags in edit profile page, courses that are not in the university's course catalogue are not allowed to be added, while there is no restrictions on tags. Tutors are merely responsible for their tags to be accurate, so that only when a student is searching the exact same text, they could be found. Attention: Don't add useless spaces in the input in adding courses and tags.

### Assumptions (Ver 1.00)
1. We assume that tutors always attend their tutorial sessions. In practice, if a tutor is absent and the student informs the company, then all payments are credited back to the student’s wallet manually.



### Disclaimer
This is originally designed for the project of [Software Engineering Course, HKU](http://www.cs.hku.hk/programme/course_info.jsp?infile=2016/comp3297.html "HKU COMP3297 Software Engineering").

We make no representations or warranties of any kind, express or implied, about the completeness, accuracy, reliability, suitability or availability with respect to the courses designed by any third parties using this platfrom. Any reliance you place on such information is therefore strictly at your own risk.<br>

All static css, fonts, images and web templates are correctly referenced either in the header of the file.
