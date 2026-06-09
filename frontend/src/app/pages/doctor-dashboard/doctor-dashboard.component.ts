import { Component } from '@angular/core';

import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { OnInit, ChangeDetectorRef } from '@angular/core';

import {
  HttpClientModule,
  HttpClient
} from '@angular/common/http';

import { Router } from '@angular/router';

@Component({

  selector: 'app-doctor-dashboard',

  standalone: true,

  imports: [
    CommonModule,
    FormsModule,
    HttpClientModule
  ],

  templateUrl: './doctor-dashboard.component.html',

  styleUrls: ['./doctor-dashboard.component.css']

})

export class DoctorDashboardComponent implements OnInit {

  doctorName = '';

  loading = false;

  predictionResult: any = null;

  showAdvanced = false;

  patients: any[] = [];

  selectedPatientId: number = 0;

  patientMeasurements: any[] = [];

  patientHistory: any[] = [];

  constructor(

    private http: HttpClient,
    private router: Router,
    private cdr: ChangeDetectorRef

  ) {}

  ngOnInit(): void {

    this.doctorName =

      (localStorage.getItem('first_name') || '') +

      ' ' +

      (localStorage.getItem('last_name') || '');

    this.loadPatients();

    this.loadHistory();

  }

  formData: any = {

    age: 50,

    sex: 1,

    cp: 0,

    trestbps: 120,

    chol: 200,

    fbs: 0,

    restecg: 0,

    thalach: 150,

    exang: 0,

    oldpeak: 0,

    slope: 1,

    ca: 0,

    thal: 3

  };

  toggleAdvanced() {

    this.showAdvanced = !this.showAdvanced;

  }

  loadPatients() {

    this.http.get<any[]>(

      'http://localhost:5000/api/patients'

    )

    .subscribe({

      next: (res) => {

        this.patients = res;

      },

      error: (err) => {

        console.log(err);

      }

    });

  }

  loadHistory() {

    this.http.get<any[]>(

      'http://localhost:5000/api/history'

    )

    .subscribe({

      next: (res) => {

        this.patientHistory = res;

      },

      error: (err) => {

        console.log(err);

      }

    });

  }

  loadPatientHistory() {

    if (!this.selectedPatientId) {

      this.patientMeasurements = [];

      return;

    }

    this.http.get<any[]>(

      `http://localhost:5000/api/patient-history/${this.selectedPatientId}`

    )

    .subscribe({

      next: (res) => {

        this.patientMeasurements = res;

      },

      error: (err) => {

        console.log(err);

      }

    });

  }

  submit() {

    if (!this.selectedPatientId) {

      alert('Please select a patient');

      return;

    }

    this.formData.user_id = this.selectedPatientId;

    this.loading = true;

    const token = localStorage.getItem('token');

    this.http.post(

      'http://localhost:5000/api/predict',

      this.formData,

      {

        headers: {

          Authorization:
          `Bearer ${token}`

        }

      }

    )

    .subscribe({

      next: (res: any) => {

        this.predictionResult = res;

        this.loading = false;

        this.loadHistory();

        this.loadPatientHistory();
        this.cdr.detectChanges();

      },

      error: (err) => {

        console.error(err);

        this.loading = false;
        this.cdr.detectChanges();

      }

    });

  }

  getRiskLabel(): string {

    const risk =

      this.predictionResult?.probability || 0;

    if (risk < 30) {

      return 'LOW RISK';

    }

    if (risk < 70) {

      return 'MODERATE RISK';

    }

    return 'HIGH RISK';

  }

  goToHistory() {

  this.router.navigate([
    '/doctor-history'
  ]);

 }
  

  logout() {

    localStorage.clear();

    this.router.navigateByUrl(
      '/',
      {
        replaceUrl: true
      }
    );

  }

}
