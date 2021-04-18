import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Verbose';
  studentID : string = "";

  onSubmit(id : string) {
    this.studentID = id;
  }
}
