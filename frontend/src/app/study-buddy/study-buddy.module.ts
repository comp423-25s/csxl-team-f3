import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { StudyBuddyRoutingModule } from './study-buddy-routing.module';
import { StudyBuddyPageComponent } from './study-buddy-page/study-buddy-page.component';
import { MatButtonModule } from '@angular/material/button';

@NgModule({
  declarations: [StudyBuddyPageComponent],
  imports: [CommonModule, StudyBuddyRoutingModule, MatButtonModule]
})
export class StudyBuddyModule {}
