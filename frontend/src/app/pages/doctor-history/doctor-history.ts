import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({

  selector: 'app-doctor-history',

  standalone: true,

  imports: [
    CommonModule,
    FormsModule,
    HttpClientModule
  ],

  templateUrl: './doctor-history.html',

  styleUrls: ['./doctor-history.css']

})

export class DoctorHistoryComponent implements OnInit {

  patients: any[] = [];

  history: any[] = [];

  selectedPatientId = 0;

  constructor(

    private http: HttpClient,

    private router: Router

  ) {}

  ngOnInit(): void {

    this.loadPatients();

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

        console.error(err);

      }

    });

  }

  loadPatientHistory() {

    if (!this.selectedPatientId) {

      this.history = [];

      return;

    }

    this.http.get<any[]>(

      `http://localhost:5000/api/patient-history/${this.selectedPatientId}`

    )

    .subscribe({

      next: (res) => {

        this.history = res;

      },

      error: (err) => {

        console.error(err);

      }

    });

  }

  goBack() {

    this.router.navigate([
      '/doctor-dashboard'
    ]);

  }

}