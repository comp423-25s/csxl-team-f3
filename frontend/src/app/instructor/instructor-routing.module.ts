import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { InstructorPageComponent } from './instructor-page.component';
import { permissionGuard } from '../permission.guard';


const routes: Routes = [{ path: '', component: InstructorPageComponent , canActivate: [permissionGuard('instructor.*',  '*')]}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class InstructorRoutingModule {}
