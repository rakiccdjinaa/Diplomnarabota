import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({

  selector: 'app-patient-dashboard',

  standalone: true,

  imports: [
    CommonModule,
    HttpClientModule
  ],

  templateUrl: './patient-dashboard.component.html',

  styleUrls: ['./patient-dashboard.component.css']

})

export class PatientDashboardComponent implements OnInit {

  username = '';

  latestRisk = 0;

  alerts: string[] = [];

  history: any[] = [];

  constructor(
    private http: HttpClient,
    private router: Router,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {

    this.username =
      localStorage.getItem('username') || '';

    this.loadHistory();

  }

  loadHistory() {

    const userId =
      localStorage.getItem('user_id');

    if (!userId) {
      return;
    }

    this.http.get<any[]>(

      `http://localhost:5000/api/patient-history/${userId}`

    )
    .subscribe({

      next: (res) => {

        console.log('Patient history:', res);

        this.history = res;
        this.alerts = [];

        if (res.length > 0) {

          this.latestRisk =
            res[0].risk;
          
          if(this.latestRisk >= 70){
             this.alerts.push('High cardiovascular risk detected. Please consult your doctor.');
          }
        } else if(this.latestRisk >= 30){
          this.alerts.push('Moderate cardiovascular risk detected. Further monitoring is recommended.');
        }

        this.cdr.detectChanges();

      },

      error: (err) => {

        console.error(err);

        this.cdr.detectChanges();

      }

    });

  }

  getRiskLabel(risk: number): string {

    if (risk < 30) {
      return 'LOW RISK';
    }

    if (risk < 70) {
      return 'MODERATE RISK';
    }

    return 'HIGH RISK';
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