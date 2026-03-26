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

    const escapeCSV = (val: string | null | undefined): string => {
      if (val === null || val === undefined) return '';
      const str = String(val);
      if (str.includes(',') || str.includes('"') || str.includes('\n')) {
        return '"' + str.replace(/"/g, '""') + '"';
      }
      return str;
    };

    let csv = '';

    // Invoice header fields
    const headerFields = [
      'Invoice Number', 'Invoice Date', 'Place of Supply',
      'Seller Name', 'Seller GSTIN', 'Seller Address',
      'Buyer Name', 'Buyer GSTIN', 'Buyer Address',
      'Sub Total', 'CGST', 'SGST', 'IGST', 'Total Tax', 'Total Amount',
      'P.O. Number', 'Due Date', 'IRN',
    ];
    const headerValues = [
      d.invoice_number, d.invoice_date, d.place_of_supply,
      d.seller_name, d.seller_gstin, d.seller_address,
      d.buyer_name, d.buyer_gstin, d.buyer_address,
      d.sub_total, d.cgst_amount, d.sgst_amount, d.igst_amount, d.total_tax, d.total_amount,
      d.po_number, d.due_date, d.irn,
    ];

    csv += headerFields.map(escapeCSV).join(',') + '\r\n';
    csv += headerValues.map(escapeCSV).join(',') + '\r\n';

    // Line items
    if (d.line_items && d.line_items.length > 0) {
      csv += '\r\n';
      const itemHeaders = ['#', 'Description', 'HSN/SAC', 'Quantity', 'Unit Price', 'Taxable Amount', 'Tax Rate', 'Line Total'];
      csv += itemHeaders.map(escapeCSV).join(',') + '\r\n';

      d.line_items.forEach((item, i) => {
        const row = [
          String(i + 1),
          item.description,
          item.hsn_sac,
          item.quantity,
          item.unit_price,
          item.taxable_amount,
          item.tax_rate,
          item.line_total,
        ];
        csv += row.map(escapeCSV).join(',') + '\r\n';
      });
    }

    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    const slug = d.invoice_number ? d.invoice_number.replace(/[^a-z0-9_\-]/gi, '_') : 'invoice';
    a.href = url;
    a.download = `invoice_${slug}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }
}
