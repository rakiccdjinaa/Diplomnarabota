import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClientModule, HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  step = 1;
  predictionResult: any = null;

  formData: any = {
    age: 50, sex: 1, cp: 0, trestbps: 120, chol: 200,
    fbs: 0, restecg: 0, thalach: 150, exang: 0,
    oldpeak: 0.0, slope: 1, ca: 0, thal: 3
  };

  constructor(private http: HttpClient) {}

  nextStep() { this.step++; }
  prevStep() { this.step--; }

  submit() {
    this.http.post('http://localhost:8080/api/predict', this.formData)
      .subscribe({
        next: (res: any) => {
          this.predictionResult = res;
          this.step = 4;
        },
        error: (err) => console.error('Error:', err)
      });
  }
}