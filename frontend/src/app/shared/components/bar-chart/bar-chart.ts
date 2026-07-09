import { Component, Input } from '@angular/core';
import { ChartDataItem } from '../../../core/models/analytics.model';

@Component({
  selector: 'app-bar-chart',
  imports: [],
  templateUrl: './bar-chart.html',
  styleUrl: './bar-chart.css',
})
export class BarChart {
  @Input({ required: true }) title = '';
  @Input({ required: true }) description = '';
  @Input({ required: true }) items: ChartDataItem[] = [];
  @Input() variant: 'primary' | 'secondary' = 'primary';

  getMaxChartValue(): number {
    if (!this.items.length) {
      return 1;
    }

    return Math.max(...this.items.map((item) => item.value), 1);
  }
}
