import {
  Component,
  ElementRef,
  inject,
  signal,
  ViewChild,
} from '@angular/core';
import { Lab3Service } from './lab3.service';
import { TypeService } from '../labs.interfaces';
import { take } from 'rxjs';
import { FileSystemService } from '../shared/file-sestem.service';

@Component({
  selector: 'app-lab3',
  templateUrl: './lab3.component.html',
  styleUrls: ['./lab3.component.scss'],
})
export class Lab3Component {
  inputText: string = '';
  passwordKey: string = '';
  inputFile: File | null = null;
  inputFileUrl = '';
  decryptFile: Blob | null = null;
  isDisabled = false;
  errorDecryption:string = '';

  fileName_encr?: string;
  fileName_decr?: string;
  savePath?: Promise<string>;
  isSaveParameters = false;

  encrypted_line = signal('');
  decrypted_line = signal('');
  encrypted_file: Blob | null = null;
  decrypted_file: Blob | null = null;
  decrypted_extention = '';
  decrypted_file_link: string = '';

  protected readonly TypeService = TypeService;

  @ViewChild('fileinput') fileInputField!: ElementRef;
  @ViewChild('decryptFileInput') decryptFileInput!: ElementRef;

  private server = inject(Lab3Service);
  private fileSystem = inject(FileSystemService);

  onInputChange() {
    this.errorDecryption = '';
    this.inputFile = null;
    this.decryptFile = null;
    this.fileInputField.nativeElement.value = null;
    this.decryptFileInput.nativeElement.value = null;
    this.inputFileUrl = '';
    this.inputText='';
    this.decrypted_file_link = '';
    this.errorDecryption = '';
  }

  onFileSelected(event: Event, typeService: TypeService): void {
    const inputElement = event.target as HTMLInputElement;
    if (inputElement.files && inputElement.files.length > 0) {
      this.inputText = '';
      if (typeService === TypeService.Encryption) {
        this.inputFile = inputElement.files[0];
        if (this.inputFile.type == 'image/jpeg') {
          this.inputFileUrl = URL.createObjectURL(this.inputFile);
        }
        this.decryptFileInput.nativeElement.value = null;
      }
      if (typeService === TypeService.Decryption) {
        this.decryptFile = inputElement.files[0];
        this.fileInputField.nativeElement.value = null;
        this.decrypted_file_link = '';
      }
    }
  }

  inputClear(){
    if (this.inputText){
      this.inputFile=null;
      this.decryptFile = null;
      this.fileInputField.nativeElement.value = null;
      this.inputFileUrl = '';
    }else{
      this.inputText='';
    }
    this.decrypted_file_link = '';
    this.errorDecryption = '';
  }

  getRC5() {
    if ((!this.inputText && !this.inputFile) || !this.passwordKey) {
      return;
    }
    this.inputClear();
    this.isDisabled = true;
    this.server
      .getEncryptionRC5(this.passwordKey, this.inputText, this.inputFile)
      .pipe(take(1))
      .subscribe({
        next: async (fileBlob) => {
          this.encrypted_file = fileBlob;

          const buffer = await fileBlob.arrayBuffer();
          const view = new Uint8Array(buffer);

          const separatorIndex = view.indexOf(10);

          const encrypted_line_bytes = view.slice(separatorIndex + 1);
          if (encrypted_line_bytes) {
            this.encrypted_line.set(
              Array.from(encrypted_line_bytes, (byte) =>
                byte.toString(16).padStart(2, '0')
              ).join('')
            );
          }
          this.isDisabled = false;
          this.errorDecryption = '';
        },
        error: (error) => {
          console.error(error);
        },
      });
  }

  getRC5Decryption() {
    if (!this.decryptFile || !this.passwordKey) {
      return;
    }
    if (this.decryptFile.type != 'text/plain'){
      this.errorDecryption = 'Provided file is not a .txt file. Please choose a text file with encoded value';
      return;
    }
    this.errorDecryption = '';
    this.isDisabled = true;
    this.server
      .getDecryptionRC5(this.passwordKey, this.decryptFile)
      .pipe(take(1))
      .subscribe({
        next: async (res) => {
          const resFile = res.body;
          const contentDisposition = res.headers.get('content-disposition');
          const filename = contentDisposition?.includes('filename=') ? contentDisposition.split('filename=')[1].split(';')[0].replace(/"/g, '').split('.') : [];
          
          this.decrypted_extention = filename.length > 1 ? filename.pop()??'.txt' : '.txt';
          if (resFile?.type=='text/plain') {
            const reader = new FileReader();
            reader.onload = () => {
              this.decrypted_line.set(reader.result as string);
            };
            reader.onerror = (error) => {
              console.error('Error reading blob:', error);
            };
            reader.readAsText(resFile);
          }
          if (resFile?.type.startsWith("image/")) {
            this.decrypted_file_link = URL.createObjectURL(resFile);
          }
          this.decrypted_file = resFile;
        },
        error: (error) => {
          console.error(error);
          this.isDisabled = false;
          this.errorDecryption = 'Incorrect password';
        },
        complete: ()=>{
          this.isDisabled = false;
        }
      });
  }

  async onPathSelect() {
    const dirName = await this.fileSystem.openPathPicker();
    if (dirName) {
      this.savePath = dirName;
    }
  }

  async saveFile(typeService: TypeService) {
    if (!this.encrypted_file && !this.decrypted_file) {
      return;
    }
    const file_type = typeService === TypeService.Encryption ? this.encrypted_file:this.decrypted_file;
    const file_name = typeService === TypeService.Encryption ? this.fileName_encr:this.fileName_decr;
    if (file_type){
      await this.fileSystem.saveToFile(
        file_name + "."+(this.decrypted_extention ? this.decrypted_extention : 'txt'),
        file_type
      );
      this.fileName_encr = '';
      this.fileName_decr = '';
      this.decrypted_extention='';
    }
  }

  openSaveParameters() {
    this.isSaveParameters = true;
  }
}
