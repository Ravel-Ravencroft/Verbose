import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class RestService {
  studentURL : string = "http://localhost:5000/student/"
  classURL : string = "http://localhost:5000/class/"

  constructor(private http : HttpClient) { }

  getStudentRecords(id : string) {
    return this.http.get<any>(this.studentURL + id);
  }

  getTodayRecords(id: string, date: string) {
    return this.http.get<any>(this.classURL + id + "/" + date);
  }
}
