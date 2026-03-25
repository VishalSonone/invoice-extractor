import { Component, OnInit, signal } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { InvoiceService } from '../services/invoice';
import { InvoiceData } from '../models/invoice.model';

@Component({
  selector: 'app-result',
  imports: [RouterLink],
  templateUrl: './result.html',
  styleUrl: './result.css',
})
export class Result implements OnInit {
  data = signal<InvoiceData | null>(null);

  constructor(
    private invoiceService: InvoiceService,
    private router: Router,
  ) {}

  ngOnInit(): void {
    const result = this.invoiceService.getResult();
    if (!result) {
      this.router.navigate(['/']);
      return;
    }
    this.data.set(result);
  }

  safeVal(value: string | null | undefined): string {
    return value !== null && value !== undefined && value !== '' ? value : '\u2014';
  }

  downloadCsv(): void {
    const d = this.data();
    if (!d) return;

    const headers = ['Invoice ID', 'Name', 'From', 'To', 'Amount', 'CGST', 'SGST', 'Invoice Date'];
    const values = [
      d.invoice_id, d.name, d.from_entity, d.to_entity,
      d.amount, d.cgst, d.sgst, d.invoice_generated_date,
    ];

    const escapeCSV = (val: string | null | undefined): string => {
      if (val === null || val === undefined) return '';
      const str = String(val);
      if (str.includes(',') || str.includes('"') || str.includes('\n')) {
        return '"' + str.replace(/"/g, '""') + '"';
      }
      return str;
    };

    const csv = headers.map(escapeCSV).join(',') + '\r\n' + values.map(escapeCSV).join(',');
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    const slug = d.invoice_id ? d.invoice_id.replace(/[^a-z0-9_\-]/gi, '_') : 'invoice';
    a.href = url;
    a.download = `invoice_${slug}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }
}
