import { TestBed } from '@angular/core/testing';

import { StudyBuddyService } from './study-buddy.service';

describe('StudyBuddyService', () => {
  let service: StudyBuddyService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(StudyBuddyService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
