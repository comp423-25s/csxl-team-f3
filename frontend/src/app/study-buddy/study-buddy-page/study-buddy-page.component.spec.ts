import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StudyBuddyPageComponent } from './study-buddy-page.component';

describe('StudyBuddyPageComponent', () => {
  let component: StudyBuddyPageComponent;
  let fixture: ComponentFixture<StudyBuddyPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StudyBuddyPageComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(StudyBuddyPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
