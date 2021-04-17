import { Component, Input, OnChanges, OnInit, ViewChild } from '@angular/core';
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
	@Input() id : string = "";
	punctuality : string = "";
	dataSource : any;

	DISPLAYED_COLUMNS : string[] = ["date", "time", "punctuality"];
	SCHOOL_BEGINS : string = "07:30:00";

	@ViewChild(MatSort) sort : MatSort | undefined;

	constructor(private service : RestService) { }

	ngOnChanges() {
		this.service.getStudentRecords(this.id).subscribe(
			data => {
				this.dataSource = new MatTableDataSource(data.data as Student[]);
				this.dataSource.sort = this.sort;
			}
		);
	}

	checkStatus(input:string) {
		if( input.endsWith("-") ) {
			return "Absent";
		}
		else if(input > this.SCHOOL_BEGINS) {
			return "Late";
		}
		else {
			return "On Time";
		}
	}
}
