import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { InstructorPageComponent } from './instructor-page.component';

const routes: Routes = [{ path: '', component: InstructorPageComponent }];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class InstructorRoutingModule {}
