import { Component } from '@angular/core';
import { RestService } from './rest.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Verbose';
  studentID:string = "";
  searched = false;

  constructor(private restService : RestService) {}

  onSubmit() {
    console.log(this.studentID);
    this.searched = true;
  }
}
