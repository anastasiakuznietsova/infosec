import { inject, Injectable } from "@angular/core";
import { HttpClient } from '@angular/common/http';
import { HashCompare } from "../labs.interfaces";

@Injectable({providedIn: 'root'})
export class Lab2Service {
    private httpClient = inject(HttpClient);
    private baseUrl = 'http://localhost:8000';


    createHashSequence(inputStr: string, inputFile:File|null){
        const formData = new FormData();

        if (inputStr) formData.append('inputStr', inputStr);
        if (inputFile) formData.append('inputFile', inputFile);
  
        return this.httpClient.post<{ hashValue: string }>(`${this.baseUrl}/md5_hash`, formData);
    }

    checkFileIntegrity(inputFile: File, controlFile:File){
        const formData = new FormData();

        if (inputFile) formData.append('inputFile', inputFile);
        if (controlFile) formData.append('controlFile', controlFile);

        return this.httpClient.post<HashCompare>(`${this.baseUrl}/md5_hash/check_integrity`, formData);
    }
}