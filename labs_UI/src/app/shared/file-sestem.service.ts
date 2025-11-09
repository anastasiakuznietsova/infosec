import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class FileSystemService {
    private dirHandle: any;

    async openPathPicker() {
        try {
            this.dirHandle = await (window as any).showDirectoryPicker();
            console.log(this.dirHandle);
            return this.dirHandle.name;
        } catch (error) {
            console.log(error);
        }
    }

    async saveToFile(saveName: string = 'sequence.txt', content: Blob) {
        if (!this.dirHandle) {
            return;
        }

        try {
            console.log(saveName);
            const fileHandle = await this.dirHandle.getFileHandle(saveName, { create: true });
            const writable = await fileHandle.createWritable();
            await writable.write(content);
            await writable.close();
            alert(`File saved in folder "${this.dirHandle.name}"`);
        } catch (error) {
            console.log(error);
        }
    }
}
