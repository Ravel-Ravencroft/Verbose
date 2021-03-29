import { AfterViewInit, Component, Input } from '@angular/core';
import { MatTableDataSource } from '@angular/material/table';
import { RestService } from '../rest.service';
import { Student } from "../Student";

@Component({
  selector: 'app-student-details',
  templateUrl: './student-details.component.html',
  styleUrls: ['./student-details.component.css']
})

export class StudentDetailsComponent implements AfterViewInit {
  title = 'Verbose';
  @Input() id: any;
  displayedColumns: string[] = ["id", "timestamp"];
  RECORD_DATA: Student[] = [];
  dataSource: any;

  constructor(private service : RestService) { }

  ngAfterViewInit() {
    this.service.getStudentRecords(this.id).subscribe(
      data => {
        console.log(data);
        this.RECORD_DATA = data.data as Student[];
        this.dataSource = new MatTableDataSource(this.RECORD_DATA);
        console.log(this.dataSource);
      }
    );
  }
}
