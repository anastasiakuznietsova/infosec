export interface RandNum {
    sequence: string;
    period: number;
}

export interface TestGenerator {
    probability: number;
    actualProbability: number;
    PIestimate: number;
    PIactual: number;
}

export interface HashCompare {
    hashValue:string;
    hashCompare: string;
    integrityPassed:boolean;
}

export enum TypeService {
    ControlIntegrity,
    HashValue,
    TestIntegrity,
    Encryption,
    Decryption,
    PublicKey,
    PrivateKey
}
