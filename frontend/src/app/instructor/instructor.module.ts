import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { InstructorRoutingModule } from './instructor-routing.module';
import { InstructorPageComponent } from './instructor-page.component';

@NgModule({
  declarations: [InstructorPageComponent],
  imports: [CommonModule, InstructorRoutingModule, MatButtonModule]
})
export class InstructorModule {}
