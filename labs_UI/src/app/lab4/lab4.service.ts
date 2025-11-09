import { inject, Injectable } from "@angular/core";
import { HttpClient } from '@angular/common/http';

@Injectable({providedIn: 'root'})
export class Lab4Service {
    private httpClient = inject(HttpClient);
    private baseUrl = 'http://localhost:8000';

    getEncryptionRSA(publicKeyFile:Blob,encryptInputFile:Blob){
        const formData = new FormData();
        formData.append('public_file', publicKeyFile);
        formData.append('inputFile', encryptInputFile);
        return this.httpClient.post(`${this.baseUrl}/rsa/encrypt_file`, formData, { responseType: 'blob' });
    }

    getDecryptionRSA(decryptPrivateFile:Blob,decryptInputFile:Blob,passwordKey:string) {
        const formData = new FormData();
        formData.append('private_file', decryptPrivateFile);
        formData.append('inputFile', decryptInputFile);
        formData.append('password', passwordKey);

        return this.httpClient.post(`${this.baseUrl}/rsa/decrypt_file`, formData, { responseType: 'blob', observe: 'response' });
    }

    getPublicKeyRSA(privateKeyFile:Blob,passwordKey:string){
        const formData = new FormData();
        formData.append('private_file', privateKeyFile);
        console.log(privateKeyFile);
        formData.append('password', passwordKey);
        return this.httpClient.post(`${this.baseUrl}/rsa/get_public_key`, formData, { responseType: 'blob' });
    }

    getPrivateKeyRSA(passwordKey:string){
        const params = { password: passwordKey };
        return this.httpClient.get(`${this.baseUrl}/rsa/get_private_key`, { params, responseType: 'blob' });
    }
}