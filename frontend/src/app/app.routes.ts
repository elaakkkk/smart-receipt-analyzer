import { Routes } from '@angular/router';
import { Dashboard } from './pages/dashboard/dashboard';
import { Receipts } from './pages/receipts/receipts';
import { ReceiptDetailComponent } from './pages/receipt-detail/receipt-detail';
import { Analytics } from './pages/analytics/analytics';

export const routes: Routes = [
    { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
    { path: 'dashboard', component: Dashboard },
    { path: 'receipts', component: Receipts },
    { path: 'receipts/:id', component: ReceiptDetailComponent },
    { path: 'analytics', component: Analytics },
];
