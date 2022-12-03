from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import WorkoutDate, WorkoutName
from django.middleware.csrf import get_token


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None, request=None):
        self.year = year
        self.month = month
        self.request= request
        super(Calendar, self).__init__()
	# formats a day as a td
	# filter events by day
    def formatday(self,day):
        d=''
        workoutId = WorkoutDate.objects.filter(user = self.request.user,
                                                 date__year=self.year,
                                                 date__month= self.month,
                                                 date__day = day).values('workoutname')


        mydiv="<div class='day col-sm p-2 border border-left-0 border-top-0 text-truncate'>"
        if day !=0:
            if workoutId:
                workoutId = workoutId[0]['workoutname']
                workout = WorkoutName.objects.get(id=workoutId)
                wid = int (workout.id)
                return f"""<td><div class="day col-sm p-2 border border-left-0 border-top-0 text-truncate ">
                           <h5 class="row align-items-center">
                           <span class="date col-1">{day}</span>
                           <small class="col d-sm-none text-center text-muted">Wednesday</small>
                           <span class="col-1"></span>
                           </h5>
                           <div class="dropdown dropleft">
                           <a style="float:right;" type="button" id="dropdownMenu1" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">
                           <span <i class="dots"></i></span>
                           </a>
                           <ul class=" dd dropdown-menu bg-light" aria-labelledby="dropdownMenu1">
                           <li><a data-toggle="modal" data-target="#d{workout.date}ModalCenter" href='' style= "font-size:11px;">Remove Workout</a></li>
                           </ul>
                           </div>
                           <a href="/{workout.id}" class="event d-block p-1 pl-2 pr-2 mb-1 rounded text-truncate small bg-primary text-white text-center" >{workout}</a>
                            <div class="modal fade" id='d{workout.date}ModalCenter' tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">

                                  <div class="modal-dialog modal-dialog-centered" role="document">
                                    <div class="modal-content">
                                      <div class="modal-header">
                                        <h5 class="modal-title" id="ModalLTitle">Delete Workout</h5>
                                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                          <span aria-hidden="true">&times;</span>
                                        </button>
                                      </div>
                                      <div class="modal-body text-wrap">
                                      Are you sure you want to delete {workout.date} {workout.name}?
                                      </div>
                                      <div class="modal-footer">
                                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                                        <a href='/{wid}/delete_workout/' name="calDelete" type="button" class="btn btn-danger">Delete</a>
                                      </div>
                                    </div>
                                  </div>
                                </div>

                           </div></td>"""
            else:
                csrf_token = get_token(self.request)
                csrf_token_html = '<input type="hidden" name="csrfmiddlewaretoken" value="{}" />'.format(csrf_token)
                if day%2==0:
                    placeholder= 'e.g. Leg Day'
                elif day%3==0:
                    placeholder= 'e.g. Cardio'
                else:
                    placeholder = 'e.g. Upper Body'

                dateId= datetime(self.year,self.month,day).date()
                theDate = dateId.strftime("%A, %B %d, %Y")
                return f"""<td><div class="day col-sm p-2 border border-left-0 border-top-0 text-truncate ">
                           <h5 class="row align-items-center">
                           <span class="date col-1">{day}</span>
                           <small class="col d-sm-none text-center text-muted"></small>
                           <span class="col-1"></span>
                           </h5>
                           <div class="dropdown dropleft">
                           <a style="float:right;" type="button" id="dropdownMenu1" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">
                           <span <i class="dots"></i></span>
                           </a>
                           <ul class="dd dropdown-menu bg-light" aria-labelledby="dropdownMenu1">
                           <li><a href="#" data-toggle="modal" data-target="#d{dateId}ModalCenter" style= "font-size:11px;">Add Workout</a></li>
                           </ul>
                           </div>
                           <form class="form-group" method="POST" action="/calendar/">
                           { csrf_token_html }
                           <div class="modal fade" id="d{dateId}ModalCenter" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
                              <div class="modal-dialog modal-dialog-centered" role="document">
                                <div class="modal-content">
                                  <div class="modal-header">
                                    <h5 class="modal-title" id="exampleModalLongTitle">{theDate}</h5>
                                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                      <span aria-hidden="true">&times;</span>
                                    </button>
                                  </div>
                                  <div class="modal-body">
                                  <div class="form-group form-inline">
                                    <label for="wkoutTitle" >Workout Title:   </label>
                                     <input type="hidden" name = "date" value='{ dateId}'>
                                    <input name="workout_title" style="width:70%;" type="text" class="form-control" id="wkoutTitle" placeholder=" {placeholder}" required>
                                  </div>
                                  </div>
                                  <div class="modal-footer">
                                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                                    <button type="submit" class="btn btn-success">Add</button>
                                  </div>
                                </div>
                              </div>
                            </div>
                            </form>
                           </div></td>"""
        else:
            return f"<td class = 'noday border border-right-0 border-bottom-0 '></td>"
	# formats a week as a tr
    def formatweek(self,theweek):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d)
        return f'<tr> {week} </tr>'


	# formats a month as a table
	# filter events by year and month
    def formatmonth(self, withyear=True):
        cal = f'<table style="table-layout:fixed;" border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        #cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        #cal += f'{weekheader}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week)}\n'

        return cal
