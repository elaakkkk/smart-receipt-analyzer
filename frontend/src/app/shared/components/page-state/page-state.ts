import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-page-state',
  imports: [],
  templateUrl: './page-state.html',
  styleUrl: './page-state.css',
})
export class PageState {
  @Input({ required: true }) message = '';
  @Input() type: 'info' | 'success' | 'error' |'loading' = 'info';

  get icon(): string {
    switch (this.type) {
      case 'success':
        return '✓';
      case 'error':
        return '!';
      case 'loading':
        return '⟳';
      default:
        return 'i';
    }
  }
}
