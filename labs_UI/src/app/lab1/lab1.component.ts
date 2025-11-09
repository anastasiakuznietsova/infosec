import { Component, inject, signal } from '@angular/core';
import { Lab1Service } from './lab1.service';
import { RandNum, TestGenerator } from '../labs.interfaces';
import { take } from 'rxjs';
import { FileSystemService } from '../shared/file-sestem.service';



@Component({
  selector: 'app-lab1',
  templateUrl: './lab1.component.html',
  styleUrls: ['./lab1.component.scss']
})
export class Lab1Component {
  private service = inject(Lab1Service);
  private fileSystem = inject(FileSystemService);

  noSequence: RandNum = {
    sequence: '',
    period: 0
  };
  noTest: TestGenerator = {
    probability: 0,
    actualProbability: 0,
    PIestimate: 0,
    PIactual: 0
  };

  randSequence = signal<RandNum>(this.noSequence);
  testResponse = signal<TestGenerator>(this.noTest);
  n?: number;
  fileName?:string;
  savePath?:Promise<string>;
  isSaveParameters = false;
  isExpanded = false;
  isDisabled = false;


  onExpandSequence() {
    if (this.isExpanded) {
      this.isExpanded = false;
    } else {
      this.isExpanded = true;
    }
  }

  async onPathSelect() {
    const dirName = await this.fileSystem.openPathPicker();
    console.log(dirName);
    if (dirName){
      this.savePath = dirName;
    }
  }

  async saveFile() {
    const seq = this.randSequence().sequence;
    const file = [`Sequence length: ${seq.length}`, `\nSequence period: ${this.randSequence().period}`, `\nSequence: \n${seq}`];
    const blob = new Blob(file, { type: 'text/plain' });
    await this.fileSystem.saveToFile(this.fileName +'.txt', blob);
  }


  createSequence() {
    if (this.n) {
      this.isDisabled = true;
      console.log(this.n);
      this.service.loadInfo(this.n).pipe(take(1)).subscribe({
        next: (resData: RandNum) => {
          this.randSequence.set(resData);
          this.n = undefined
        },
        error: (error) => {
          console.log(error);
        },
        complete:()=>{
          this.isDisabled = false;
        }
      });
    }
  }

  testGenerator() {
    this.service.testGenerator().pipe(take(1)).subscribe({
      next: (resData: TestGenerator) => {
        this.testResponse.set(resData);
      },
      error: (error) => {
        console.log(error);
      }
    });
  }

  openSaveParameters(){
    this.isSaveParameters=true;
  }
}
