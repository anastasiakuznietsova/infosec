import { inject, Injectable } from "@angular/core";
import { HttpClient } from '@angular/common/http';
import { HashCompare } from "../labs.interfaces";

@Injectable({providedIn: 'root'})
export class Lab3Service {
    private httpClient = inject(HttpClient);
    private baseUrl = 'http://localhost:8000';


    getEncryptionRC5(password_key:string, inputStr: string, inputFile:File|null){
        const formData = new FormData();
        if (password_key) formData.append('password_key', password_key);
        if (inputStr) formData.append('inputStr', inputStr);
        if (inputFile) formData.append('inputFile', inputFile);
  
        return this.httpClient.post<Blob>(`${this.baseUrl}/rc5/encode`, formData,{ responseType: 'blob' as 'json' });
    }

    getDecryptionRC5(password_key:string, encryptedFile:Blob){
        const formData = new FormData();

        if (password_key) formData.append('password_key', password_key);
        if (encryptedFile) formData.append('encryptedFile', encryptedFile);

        return this.httpClient.post(`${this.baseUrl}/rc5/decode`, formData, { responseType: 'blob', observe: 'response' });
    }
}