import { inject, Injectable } from "@angular/core";
import { HttpClient } from '@angular/common/http';
import { RandNum, TestGenerator } from "../labs.interfaces";

@Injectable({providedIn: 'root'})
export class Lab1Service {
    private httpClient = inject(HttpClient);
    private baseUrl = 'http://localhost:8000';


    loadInfo(n:number){
        return this.httpClient.get<RandNum>(`${this.baseUrl}/pseudo_rand_num?n=${n}`);
    }
    testGenerator(){
        return this.httpClient.get<TestGenerator>(`${this.baseUrl}/pseudo_rand_num/test`);
    }
}