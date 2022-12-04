from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from schedule.models import *

from datetime import datetime, date

import locale
import calendar


def index_page(request):
    return render(request, 'index.html')

def find_date():
    date_now = datetime.now()
    if date_now.month >= 9:
        first_day = datetime(date_now.year, 9, 1)
    else:
        first_day = datetime(date_now.year, 2, 9)

    if datetime.weekday(first_day) == 6:
        first_day = date(date_now.year, 9, 2)
    global_first_week = datetime(first_day.year,1,1)
    number_first_week = ((first_day - global_first_week).days // 7) + 1
    this_week_number = ((date_now - global_first_week).days // 7) + 1 - number_first_week
    type_of_week = this_week_number % 2
    if type_of_week == 0:
        type_of_week = 2

    return type_of_week, datetime.isoweekday(date_now)


def generate_date(id_group, type_of_enter_data):
    type_of_week, this_day = find_date()
    data = [['День недели', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']]


    if type_of_enter_data == "week":
        for day in range(1, 7):
            for num in range(1, 10):
                try:
                    tmp = str(Timetable.objects.get(id_to_group=id_group, subject_to_number=num, day_week=day, type_of_week=type_of_week)).split("_-_")
                    if 'None' in tmp:
                        tmp = ''
                    else:
                        for elem in tmp:
                            elem = ' '.join(elem.split())
                        tmp[1] = str(Lecturer.objects.get(id_lecturer=int(tmp[1])))
                    if len(data) - 1 < num:
                        ind = num
                        if ind > 7:
                            ind + 1
                        time = str(CallSchedule.objects.get(subject_number=ind)).split()
                        time[0] = ':'.join(str(time[0]).split(":")[:-1])
                        time[1] = ':'.join(str(time[1]).split(":")[:-1])
                        data.append([[str(ind), str('-'.join(time))]])
                    data[num].append(tmp)

                except:
                    pass
        
        for index in range(7, 10):
            flag = True
            try:
                for i, elem in enumerate(data[index]):
                    if elem != "" and i > 0:
                        flag = False
                if flag is True:
                    data.pop(index)
            except:
                pass
    
    else:
        if this_day == 7:
            return ["Сегодня выходной, пар нет!"]

        data = [['День недели', data[0][this_day]]]
        for num in range(1, 10):
            try:
                tmp = str(Timetable.objects.get(id_to_group=id_group, subject_to_number=num, day_week=this_day, type_of_week=type_of_week)).split("_-_")
                if 'None' in tmp:
                    tmp = ''
                else:
                    for elem in tmp:
                        elem = ' '.join(elem.split())
                    tmp[1] = str(Lecturer.objects.get(id_lecturer=int(tmp[1])))
                if len(data) - 1 < num:
                    ind = num
                    if ind > 7:
                        ind + 1
                    time = str(CallSchedule.objects.get(subject_number=ind)).split()
                    time[0] = ':'.join(str(time[0]).split(":")[:-1])
                    time[1] = ':'.join(str(time[1]).split(":")[:-1])
                    data.append([[str(ind), str('-'.join(time))]])
                data[num].append(tmp)
            except:
                pass
    return data


@login_required
def timetable_page(request):
    type_of_enter_data = request.session.get('type_of_enter_data', 'week')
    
    group_name, id_group = str(UserProfileInfo.objects.get(author=request.user)).split()
    
    data = generate_date(int(id_group), type_of_enter_data)

    context = {
        'group': group_name,
        'data': data,
        'type': type_of_enter_data,
        'calendar': calendar.LocaleHTMLCalendar(locale='ru_RU.UTF-8').formatmonth(datetime.today().year, datetime.today().month)
    }
    return render(request, "timetable.html", context)

def change_type_info(request):
    if request.POST.get('type_of_info'):
        request.session["type_of_enter_data"] = str(request.POST.get('type_of_info'))
    return redirect('/timetable')