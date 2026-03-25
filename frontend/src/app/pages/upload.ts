import { Component, signal } from '@angular/core';
import { Router } from '@angular/router';
import { InvoiceService } from '../services/invoice';

@Component({
  selector: 'app-upload',
  templateUrl: './upload.html',
  styleUrl: './upload.css',
})
export class Upload {
  selectedFile = signal<File | null>(null);
  loading = signal(false);
  errorMessage = signal('');
  dragOver = signal(false);

  constructor(
    private invoiceService: InvoiceService,
    private router: Router,
  ) {}

  onDragOver(event: DragEvent): void {
    event.preventDefault();
    this.dragOver.set(true);
  }

  onDragLeave(): void {
    this.dragOver.set(false);
  }

  onDrop(event: DragEvent): void {
    event.preventDefault();
    this.dragOver.set(false);
    const file = event.dataTransfer?.files[0];
    if (file && file.type === 'application/pdf') {
      this.selectFile(file);
    }
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files?.[0]) {
      this.selectFile(input.files[0]);
    }
  }

  selectFile(file: File): void {
    this.selectedFile.set(file);
    this.errorMessage.set('');
  }

  clearFile(): void {
    this.selectedFile.set(null);
  }

  submit(): void {
    const file = this.selectedFile();
    if (!file) return;

    this.loading.set(true);
    this.errorMessage.set('');

    this.invoiceService.extractInvoice(file).subscribe({
      next: (data) => {
        this.invoiceService.saveResult(data);
        this.router.navigate(['/result']);
      },
      error: (err) => {
        const detail = err.error?.detail || err.message || 'Extraction failed';
        this.errorMessage.set(detail);
        this.loading.set(false);
      },
    });
  }
}
