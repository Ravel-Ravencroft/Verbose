import { TestBed } from '@angular/core/testing';
import { StudentDetailsComponent } from './student-details.component';

describe('AppComponent', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [
        StudentDetailsComponent
      ],
    }).compileComponents();
  });

  it('should create the app', () => {
    const fixture = TestBed.createComponent(StudentDetailsComponent);
    const app = fixture.componentInstance;
    expect(app).toBeTruthy();
  });

  it(`should have as title 'Verbose'`, () => {
    const fixture = TestBed.createComponent(StudentDetailsComponent);
    const app = fixture.componentInstance;
    expect(app.title).toEqual('Verbose');
  });

  it('should render title', () => {
    const fixture = TestBed.createComponent(StudentDetailsComponent);
    fixture.detectChanges();
    const compiled = fixture.nativeElement;
    expect(compiled.querySelector('.content span').textContent).toContain('Verbose app is running!');
  });
});
