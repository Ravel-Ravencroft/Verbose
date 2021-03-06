import { Component, Input, OnChanges, ViewChild } from '@angular/core';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { RestService } from '../rest.service';
import { Student } from "../Student";

@Component({
	selector: 'app-student-details',
	templateUrl: './student-details.component.html',
	styleUrls: ['./student-details.component.css']
})

export class StudentDetailsComponent implements OnChanges {
	title = 'Verbose';
	@Input() ID : string = "";
	punctuality : string = "";
	DISPLAYED_COLUMNS : string[] = ["date", "time", "punctuality"];
	SCHOOL_BEGINS : string = "07:30:00";

	dataSource : any;

	@ViewChild(MatSort) sort : MatSort | undefined;

	constructor(private service : RestService) { }

	ngOnChanges() {
		this.service.getStudentRecords(this.ID).subscribe(
			data => {
				console.log(data);
				this.dataSource = new MatTableDataSource(data as Student[]);
				this.dataSource.sort = this.sort;
			}
		);
	}

	checkStatus(input:string) {
		if(input > this.SCHOOL_BEGINS) {
			return "Late";
		}
		else {
			return "On Time";
		}
	}
}
