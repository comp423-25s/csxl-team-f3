import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { StudyBuddyPageComponent } from './study-buddy-page/study-buddy-page.component';

const routes: Routes = [{ path: '', component: StudyBuddyPageComponent }];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class StudyBuddyRoutingModule {}
