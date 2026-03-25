import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { InvoiceData } from '../models/invoice.model';

@Injectable({ providedIn: 'root' })
export class InvoiceService {
  constructor(private http: HttpClient) {}

  extractInvoice(file: File): Observable<InvoiceData> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post<InvoiceData>('/api/upload', formData);
  }

  saveResult(data: InvoiceData): void {
    localStorage.setItem('invoiceResult', JSON.stringify(data));
  }

  getResult(): InvoiceData | null {
    const raw = localStorage.getItem('invoiceResult');
    return raw ? JSON.parse(raw) : null;
  }

  clearResult(): void {
    localStorage.removeItem('invoiceResult');
  }
}
