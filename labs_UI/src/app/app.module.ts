import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { MainPageComponent } from './main-page/main-page.component';
import { Lab1Component } from './lab1/lab1.component';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { SlicePipe } from '@angular/common';
import { Lab2Component } from './lab2/lab2.component';
import { Lab3Component } from './lab3/lab3.component';
import { Lab4Component } from './lab4/lab4.component';

@NgModule({
  declarations: [
    AppComponent,
    MainPageComponent,
    Lab1Component,
    Lab2Component,
    Lab3Component,
    Lab4Component
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule,
    SlicePipe
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
