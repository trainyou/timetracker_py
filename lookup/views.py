from django.http import request, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, authenticate
#from .ut import DayIn, Break
from input.models import Daily_Records

def home(request):
    if request.method=='POST':
        usid = request.POST.get('fname')
        passwd = request.POST.get('password')
        user = authenticate(username=usid, password=passwd)
        if user is not None and user.is_active:
            return redirect('lookup')
    else:
        return render(request, 'home.html')

#---------------------------------helper classes
from datetime import datetime, time, date, timedelta

class DayIn:
    obg = {} # This is accessible to all the 'class' objects as it is checked by the 'staticmethod' 'validate'
    def __init__(self, l_date=None, login_time=None,logout_time=None,assignments=None):
        self.iso_d = datetime.today().date().isoformat()
        self.l_date=l_date # date object
        self.init_login_time = None # in isoformat
        self.login_time=login_time # time object
        self.logout_time=logout_time # in isoformat
        self.assignments=assignments # text
        self.login_hours = timedelta(0,0,0) # timedelta object
        self.break_hours=timedelta(0,0,0) # timedelta object

    @staticmethod
    def validate():
        k = datetime.today().date()
        try:
            if DayIn.obg[k.isoformat()]:
                return DayIn.obg[k.isoformat()]
        except KeyError:# if there is no key in the 'obg'
            DayIn.obg[k.isoformat()]=DayIn(l_date=k)
            return DayIn.obg[k.isoformat()]


    @staticmethod
    def calc_time(from_time, to_time): # takes time objects
        today = datetime.today().date()
        from_time = datetime.combine(today, from_time) # needs datetime.date, datetime.time
        to_time = datetime.combine(today, to_time) # needs datetime.date, datetieme.time
        duration = to_time-from_time
        return duration


         

    def calc_loghours(self, br_start_time=None, br_end_time=None): # datetime objects both
        if self.logout_time:
            login_hours = DayIn.calc_time(self.login_time, time.fromisoformat(self.logout_time))
            return login_hours

        elif self.login_time is not None and self.logout_time is None and Break.status == True:
            login_hours = DayIn.calc_time(self.login_time, br_start_time)
            return login_hours
            
        elif self.login_time is None and self.logout_time is None and Break.status == True:
            return self.login_hours
            
        elif self.login_time is not None and self.logout_time is None and Break.status == False:
            #self.login_time = br_end_time
            login_hours = self.login_hours+DayIn.calc_time(self.login_time, datetime.now().time())
            return login_hours
            
        elif self.init_login_time is None:
            return self.login_hours


    if datetime.now().time() == time(10,27):
        self.logout_time = datetime.now().time().isoformat()
        self.auto_logout()


    def auto_logout(self):
        #updating the 'logout_time'
        self.logout_time = datetime.now().time().isoformat()
        # all the values of the 'Day_In' object has to be updated locally and further pushed to database through models.py
        self.login_hours += self.calc_loghours()
        print('Total login hours: ', self.login_hours)

        # Updating the data to the database using models
        h = Daily_Records(l_date=self.l_date, init_login = time.fromisoformat(self.init_login_time), logout_time=time.fromisoformat(self.logout_time), assignments=self.assignments, login_hours=self.login_hours)
        h.save()
        
           
from datetime import datetime, date, time
time_now = datetime.now()
today = datetime.today().date().isoformat()
class Break:
    status = False
#-----------------------------------



def lookup(request):

    #Global availability of 'Day_In.validate' object for all 'lookup' names
    d = DayIn.validate()

    from datetime import datetime, date, time
    if 'loginb' in request.POST:
        d.init_login_time = datetime.now().time().isoformat()
        d.login_time = datetime.now().time() # time object
        d.login_hours = d.calc_loghours()
        print('l_date : ', d.l_date)
        print('login_time: ', d.login_time)
        print('login_hours: ', d.login_hours)
        
        print('Day_In.obg: ',DayIn.obg)
        return redirect('/lookup')

    elif 'savebtn' in request.POST:
        d.assignments = request.POST['text']
        #d.login_hours = d.calc_loghours()
        print('Day_In.obg: ',DayIn.obg)
        print('assignments: ', d.assignments)
        return redirect('/lookup')


    elif 'breaks' in request.POST:
        # break status
        Break.status = True
        # update login_hours
        print('l hours before updating, : ', d.login_hours)
        d.login_hours += d.calc_loghours(br_start_time =datetime.now().time())
        print('l hours after updating, : ', d.login_hours)
        d.login_time = None
        print('Break start time at: ', datetime.now())
        return redirect('/lookup')


    elif 'breake' in request.POST:
        Break.status = False         # set Break status
        d.login_time = br_end_time =datetime.now().time()
        login_hours = d.calc_loghours(br_end_time) # updating the login hours by adding the previous login hours
        print('login hours after updating, : ', login_hours)
       
        return redirect('/lookup')


   
    elif 'logoutb' in request.POST:
        d.auto_logout()

        print('Day_In.obg: ',DayIn.obg)
        print('logout recorded at : ', d.logout_time)
        print('All the records saved')
        return redirect('/lookup')

    elif datetime.now().time()==time(22, 36):
            d.logout_time = datetime.now().time().isoformat()
            d.auto_logout()

            

    else:
        all_recs= Daily_Records.objects.all().values()
        records = []
        for i in all_recs:
            n = {}
            for  g,h in i.items():
                b = ['l_date','init_login', 'login_hours', 'assignments']
                if g in b:
                    n[g] = h
            records.append(n)

        if d.l_date:
            # If logged in and show present values on the page
            valus = {'l_date':d.l_date,'login_time':d.init_login_time, 'login_hours': d.calc_loghours(), 'assignments':d.assignments, 'b':not Break.status} # 'not Break.status' to revert the response because, the 'hidden' attrib of the html label's hidden status(Break:True, hidden:False, viz)
            context2 = {'d':valus, 'r': records}
            
        elif d.login_time:
                valus2 = {}
                valus = {'l_date':d.l_date,'login_time':d.init_login_time, 'login_hours': d.calc_loghours(), 'assignments':d.assignments, 'b':not Break.status}
                context2 = {'d':valus, 'r': records}
        return render(request, 'daylookup.html',  context2)
