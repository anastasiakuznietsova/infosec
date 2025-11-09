import { Component, ElementRef, inject, signal, ViewChild } from '@angular/core';
import { Lab2Service } from './lab2.service';
import { take } from 'rxjs';
import { FileSystemService } from '../shared/file-sestem.service';
import { HashCompare, TypeService } from '../labs.interfaces';

@Component({
  selector: 'app-lab2',
  templateUrl: './lab2.component.html',
  styleUrls: ['./lab2.component.scss']
})
export class Lab2Component {
  @ViewChild("fileinput") fileInputField!: ElementRef;
  @ViewChild("compareFileInput") compareFileInput!: ElementRef;
  @ViewChild("testFileInput") testFileInput!: ElementRef;
  
  private fileSystem = inject(FileSystemService);
  private server = inject(Lab2Service);
  protected readonly TypeService = TypeService;
  isDisabled = false;
  inputText = '';
  selectedFile: File|null = null;
  compareFile: File|null = null;
  testFile: File|null = null;
  hashValue = signal<string>('');
  compareTest: HashCompare|null = null;

  fileName?:string;
  savePath?:Promise<string>;
  isSaveParameters = false;

  onFileSelected(event: Event, typeService:TypeService): void {
    const inputElement = event.target as HTMLInputElement;
    if (inputElement.files && inputElement.files.length > 0) {      
      this.inputText='';
      if (typeService===TypeService.HashValue){
        this.selectedFile = inputElement.files[0];
        this.compareFileInput.nativeElement.value = null;
        this.testFileInput.nativeElement.value = null;
      }
      if (typeService===TypeService.ControlIntegrity){
        this.compareFile = inputElement.files[0];
        this.fileInputField.nativeElement.value = null;
      }
      if (typeService===TypeService.TestIntegrity){
        this.testFile = inputElement.files[0];
        this.fileInputField.nativeElement.value = null;
      }
    }
  }

  onInputChange(){
    if (this.selectedFile || this.compareFile || this.testFile){
      this.selectedFile = null;
      this.compareFile = null;
      this.testFile = null;
      this.fileInputField.nativeElement.value = null;
    }
  }

  hashInput(){
    if (this.inputText || this.selectedFile){
      this.isDisabled = true;
      this.server.createHashSequence(this.inputText, this.selectedFile).pipe(take(1)).subscribe({
        next: (resData) => {
          if (resData.hashValue){
            this.hashValue.set(resData.hashValue);

            this.inputText='';
            this.selectedFile = null;
            this.compareFile = null;
          }
        },
        error: (error) => {
          console.log(error);
        },
        complete:()=>{
          this.isDisabled = false;
          this.compareFileInput.nativeElement.value = null;
          this.testFileInput.nativeElement.value = null;
        }
      });
    }
  }

  async onPathSelect() {
    const dirName = await this.fileSystem.openPathPicker();
    if (dirName){
      this.savePath = dirName;
    }
  }

  async saveFile() {
    const hash = this.hashValue();
    const blob = new Blob([hash], { type: 'text/plain' });
    await this.fileSystem.saveToFile(this.fileName +'.txt', blob);
    this.fileName='';
  }

  openSaveParameters(){
    this.isSaveParameters=true;
  }

  checkIntegrity(){
    if (this.testFile && this.compareFile){
      this.isDisabled = true;
      this.server.checkFileIntegrity(this.testFile, this.compareFile).pipe(take(1)).subscribe({
        next: (resData) => {
          if (resData.hashValue){
            this.compareTest = resData;
          }
        },
        error: (error) => {
          console.log(error);
        },
        complete:()=>{
          this.isDisabled = false;
          this.fileInputField.nativeElement.value = null;
        }
      });
    }
  }
}
