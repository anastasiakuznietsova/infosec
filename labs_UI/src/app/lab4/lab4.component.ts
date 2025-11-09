import { Component, ElementRef, inject, ViewChild } from '@angular/core';
import { Lab4Service } from './lab4.service';
import { FileSystemService } from '../shared/file-sestem.service';
import { TypeService } from '../labs.interfaces';

@Component({
  selector: 'app-lab4',
  templateUrl: './lab4.component.html',
  styleUrls: ['./lab4.component.scss']
})
export class Lab4Component {
  passwordKey = '';
  isDisabled = false;

  publicKeyFile: Blob | null = null;
  privateKeyFile: Blob | null = null;

  encryptInputFile: Blob | null = null;
  decryptInputFile: Blob | null = null;

  encryptedData: Blob | null = null;
  decryptedBlob: Blob | null = null;

  errorMessage = '';

  fileName_encr?: string;
  fileName_decr?: string;
  fileName_priv?: string;
  fileName_publ?: string;
  savePath?: Promise<string>;
  fileExtention?:string;

  isSaveParametersEncrypt = false;
  isSaveParametersDecrypt = false;
  isSaveParametersPriv = false;
  isSaveParametersPubl = false;

  isPrivateKey = false;
  isPublicKey = false;

  private service = inject(Lab4Service);
  private fileSystem = inject(FileSystemService);
  protected readonly TypeService = TypeService;
  
  @ViewChild('encryptInput') encryptInput!: ElementRef;
  @ViewChild('decryptInput') decryptInput!: ElementRef;
  @ViewChild('publicFile') publicFile!: ElementRef;
  @ViewChild('privateFile') privateFile!: ElementRef;

  onInputChange() {
    this.errorMessage = '';
    this.fileExtention='';
  }

  generatePrivateKey() {
    this.isDisabled = true;
    this.service.getPrivateKeyRSA(this.passwordKey).subscribe({
      next: (res) => {
        this.privateKeyFile = res;
        this.isPrivateKey = true;
        this.isDisabled = false;
      },
      error: () => this.isDisabled = false
    });
  }

  generatePublicKey() {
    if (!this.privateKeyFile) return;
    this.isDisabled = true;

    this.service.getPublicKeyRSA(this.privateKeyFile, this.passwordKey).subscribe({
        next: (res) => {
          this.publicKeyFile = res;
          this.isPublicKey = true;
          this.isDisabled = false;
        },
        error: () => this.isDisabled = false
      });
  }

  encryptRSA() {
    if (!this.publicKeyFile || !this.encryptInputFile) {
      return;
    }
    this.isDisabled = true;
    this.service.getEncryptionRSA(this.publicKeyFile,this.encryptInputFile).subscribe({
        next: (res) => {
          console.log(res);
          this.encryptedData = res;
          this.isDisabled = false;
        },
        error: () => this.isDisabled = false
      });
  }

  decryptRSA() {
    if (!this.privateKeyFile || !this.decryptInputFile) {
      return;
    }
    this.isDisabled = true;
    this.service.getDecryptionRSA(this.privateKeyFile,this.decryptInputFile,this.passwordKey).subscribe({
        next: async (res) => {
          const resFile = res.body;
          const contentDisposition = res.headers.get('content-disposition');
          const filename = contentDisposition?.includes('filename=') ? contentDisposition.split('filename=')[1].split(';')[0].replace(/"/g, '').split('.') : [];
          
          this.fileExtention = filename.length > 1 ? filename.pop()??'.txt' : '.txt';

          this.decryptedBlob = resFile;
          this.isDisabled = false;
        },
        error: () => {
          this.errorMessage = 'Failed to decrypt file.';
          this.isDisabled = false;
        }
      });
  }

  onFileSelected(event: Event, typeService: TypeService): void {
      const inputElement = event.target as HTMLInputElement;
      if (inputElement.files && inputElement.files.length > 0) {
        if (typeService === TypeService.Encryption) {
          this.encryptInputFile = inputElement.files[0];
          this.decryptInput.nativeElement.value = null;
        }
        if (typeService === TypeService.Decryption) {
          this.decryptInputFile = inputElement.files[0];
          this.encryptInput.nativeElement.value = null;
        }
        if (typeService === TypeService.PublicKey){
          this.publicKeyFile = inputElement.files[0];
        }
        if (typeService === TypeService.PrivateKey){
          this.privateKeyFile = inputElement.files[0];
        }
      }
    }

  async onPathSelect() {
      const dirName = await this.fileSystem.openPathPicker();
      if (dirName) {
        this.savePath = dirName;
      }
    }
  
  async saveFile(typeService: TypeService) {
    if (!this.publicKeyFile && !this.privateKeyFile && !this.encryptedData && !this.decryptedBlob) {
      return;
    }
    
    let file_name, file_type,file_extention;
    
    if (typeService === TypeService.Encryption) {
      file_name = this.fileName_encr;
      file_type = this.encryptedData;
      file_extention = 'pem';
      this.isSaveParametersEncrypt = false;
    }
    if (typeService === TypeService.Decryption) {
      file_name = this.fileName_decr;
      file_type = this.decryptedBlob;
      file_extention = this.fileExtention;
      this.isSaveParametersDecrypt = false;
    }
    if (typeService === TypeService.PublicKey){
      file_name = this.fileName_publ;
      file_type = this.publicKeyFile;
      file_extention = 'pem';
      this.isSaveParametersPubl = false;
    }
    if (typeService === TypeService.PrivateKey){
      file_name = this.fileName_priv;
      file_type = this.privateKeyFile;
      file_extention = 'pem';
      this.isSaveParametersPriv = false;
    }

    if (file_type){
      await this.fileSystem.saveToFile(
        file_name + "."+file_extention,
        file_type
      );
    }
    this.clearFileNames();
  }

  clearFileNames(){
    this.fileName_encr='';
    this.fileName_decr='';
    this.fileName_priv='';
    this.fileName_publ='';
  }
  
  openSaveParameters(encrypt:boolean, decrypt:boolean, priv:boolean, publ:boolean) {
    this.isSaveParametersEncrypt = encrypt ? encrypt:this.isSaveParametersEncrypt;
    this.isSaveParametersDecrypt = decrypt ? decrypt:this.isSaveParametersDecrypt;
    this.isSaveParametersPriv = priv ? priv:this.isSaveParametersPriv;
    this.isSaveParametersPubl = publ ? publ: this.isSaveParametersPubl;
  }
}
