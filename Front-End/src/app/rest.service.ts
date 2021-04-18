import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class RestService {
  url : string = "http://localhost:5000/student/"
  testurl : string = "http://localhost:5000/students"

  constructor(private http : HttpClient) { }

  getStudentRecords(id : string) {
    return this.http.get<any>(this.url + id);
  }

  // getAllRecords() {
  //   return this.http.get<Student[]>(this.testurl);
  // }
}
