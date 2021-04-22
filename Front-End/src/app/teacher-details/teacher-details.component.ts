import { Component, Input, OnChanges, ViewChild } from '@angular/core';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { RestService } from '../rest.service';
import { Attendance } from "../Attendance";

@Component({
	selector: 'app-teacher-details',
	templateUrl: './teacher-details.component.html',
	styleUrls: ['./teacher-details.component.css']
})

export class TeacherDetailsComponent implements OnChanges {
	title = 'Verbose';
	@Input() ID : string = "";
	@Input() DATE : string = "";
	punctuality : string = "";
	
	DISPLAYED_COLUMNS : string[] = ["id", "time", "punctuality"];
	SCHOOL_BEGINS : string = "07:30:00";

	dataSource : any;

	@ViewChild(MatSort) sort : MatSort | undefined;

	constructor(private service : RestService) { }

	ngOnChanges() {
		this.service.getTodayRecords(this.ID, this.DATE).subscribe(
			data => {
				console.log(data);
				this.dataSource = new MatTableDataSource(data as Attendance[]);
				this.dataSource.sort = this.sort;
				console.log(this.dataSource)
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
