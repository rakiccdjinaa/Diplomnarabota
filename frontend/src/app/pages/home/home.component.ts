import { Component, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({

  selector: 'app-home',

  standalone: true,

  imports: [
    CommonModule,
    FormsModule
  ],

  templateUrl: './home.component.html',

  styleUrls: ['./home.component.css']

})

export class HomeComponent {

  constructor(
    private http: HttpClient,
    private router: Router,
    private cdr: ChangeDetectorRef
  ) {}

  activeTab = 'login';

  loginError = '';
  registerError = '';

  loginUsername = '';
  loginPassword = '';

  registerData: any = {

    first_name: '',

    last_name: '',

    username: '',

    password: '',

    role: 'patient',

    license_number: ''

  };

  login() {

    this.loginError = '';

    if (
      !this.loginUsername ||
      !this.loginPassword
    ) {

      this.loginError =
        'Please enter username and password.';

      this.cdr.detectChanges();

      return;

    }

    this.http.post(

      'http://localhost:5000/login',

      {

        username: this.loginUsername,

        password: this.loginPassword

      }

    )

    .subscribe({

      next: (res: any) => {

        localStorage.setItem(
          'token',
          res.token
        );

        localStorage.setItem(
          'user_id',
          res.user_id
        );

        localStorage.setItem(
          'role',
          res.role
        );

        localStorage.setItem(
          'username',
          res.username
        );

        localStorage.setItem(
          'first_name',
          res.first_name
        );

        localStorage.setItem(
          'last_name',
          res.last_name
        );

        if (res.role === 'doctor') {

          this.router.navigate([
            '/doctor-dashboard'
          ]);

        } else {

          this.router.navigate([
            '/patient-dashboard'
          ]);

        }

      },

      error: (err) => {

        this.loginError =
          err.error?.message ||
          'Login failed';

        this.cdr.detectChanges();

      }

    });

  }

  register() {

    this.registerError = '';

    if (
      !this.registerData.first_name ||
      !this.registerData.last_name ||
      !this.registerData.username ||
      !this.registerData.password ||
      !this.registerData.role
    ) {

      this.registerError =
        'Please fill in all required fields.';

      this.cdr.detectChanges();

      return;

    }

    const passwordRegex =
      /^(?=.*[A-Z])(?=.*\d).{8,}$/;

    if (!passwordRegex.test(this.registerData.password)) {

      this.registerError =
        'Password must contain at least 8 characters, one uppercase letter and one number.';

      this.cdr.detectChanges();

      return;
    }

    if (
      this.registerData.role === 'doctor' &&
      !this.registerData.license_number
    ) {

      this.registerError =
        'Medical license is required for doctor registration.';

      this.cdr.detectChanges();

      return;

    }

    this.http.post(

      'http://localhost:5000/register',

      this.registerData

    )

    .subscribe({

      next: () => {

        this.registerData = {

          first_name: '',

          last_name: '',

          username: '',

          password: '',

          role: 'patient',

          license_number: ''

        };

        this.registerError = '';

        this.activeTab = 'login';

        this.cdr.detectChanges();

      },

      error: (err) => {

        this.registerError =
          err.error?.message ||
          'Registration failed';
        this.cdr.detectChanges();
      }

    });

  }

}