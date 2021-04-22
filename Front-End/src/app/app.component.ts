import { DatePipe } from '@angular/common';
import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  dateVisibility = false;
  student = false;
  teacher = false;

  title = 'Verbose';
  minDate = new Date(2021, 3, 1)
  maxDate = new Date()
  selectedDate: any;

  id : string = "";
  queryDate: any;

  constructor(public datepipe: DatePipe) {}

  dateFilter = (date: Date | null): boolean => {
    const day = ( date|| new Date() ).getDay();
    return day != 0 && day != 6;
  }

  OnDateChange(date: any) {
    this.selectedDate = date;
  }

  onKey(event: any) {
    this.dateVisibility = event.target.value.includes("uow");
  }

  onSubmit(input : string) {
    if( input.toLowerCase().startsWith("w") ) {   
      this.student = true;
      this.teacher = false;
    }
    else if( input.toLowerCase().startsWith("uow") ) {   
      this.student = false;
      this.teacher = true;
    }
    else {
      this.student = false;
      this.teacher = false;
    }

    this.id = input;
    this.queryDate = this.datepipe.transform(this.selectedDate, 'yyyy-MM-dd')
  }
}
