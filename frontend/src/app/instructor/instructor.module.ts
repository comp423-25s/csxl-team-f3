import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { InstructorRoutingModule } from './instructor-routing.module';
import { InstructorPageComponent } from './instructor-page.component';
import { MarkdownModule } from 'ngx-markdown';
import { SharedModule } from '../shared/shared.module';
import { permissionGuard } from '../permission.guard';




@NgModule({
  declarations: [InstructorPageComponent],
  imports: [CommonModule, InstructorRoutingModule, MatButtonModule, MarkdownModule.forChild()]
})
export class InstructorModule {}

