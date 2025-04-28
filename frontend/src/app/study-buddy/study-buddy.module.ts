import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { HttpClientModule } from '@angular/common/http';
import { MarkdownModule } from 'ngx-markdown';
import { SharedModule } from '../shared/shared.module';

import { StudyBuddyRoutingModule } from './study-buddy-routing.module';
import { StudyBuddyPageComponent } from './study-buddy-page/study-buddy-page.component';

@NgModule({
  declarations: [StudyBuddyPageComponent],
  imports: [
    CommonModule,
    SharedModule,
    StudyBuddyRoutingModule,
    ReactiveFormsModule,
    MatButtonModule,
    HttpClientModule,
    MarkdownModule.forChild()
  ]
})
export class StudyBuddyModule {}
