import { Routes } from '@angular/router';
import { Upload } from './pages/upload';
import { Result } from './pages/result';

export const routes: Routes = [
  { path: '', component: Upload },
  { path: 'result', component: Result },
  { path: '**', redirectTo: '' },
];
