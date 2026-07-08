import { Routes } from '@angular/router';
import { Dashboard } from './pages/dashboard/dashboard';
import { Receipts } from './pages/receipts/receipts';

export const routes: Routes = [
    { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
    { path: 'dashboard', component: Dashboard },
    { path: 'receipts', component: Receipts },
];
