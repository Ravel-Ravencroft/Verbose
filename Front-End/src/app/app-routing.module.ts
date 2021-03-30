import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { MainmenuComponent} from './components/mainmenu/mainmenu.component';
import { DetailsmenuComponent} from './components/detailsmenu/detailsmenu.component';


const routes: Routes = [
  {path: 'mainmenu', component: MainmenuComponent},
  {path: 'detailsmenu', component: DetailsmenuComponent}
];

@NgModule({
  exports: [RouterModule],
  imports: [ 
    RouterModule.forRoot(routes) 
  ]
})
export class AppRoutingModule { }
