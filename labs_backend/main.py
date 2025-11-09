from fastapi.responses import FileResponse
from fastapi import FastAPI, HTTPException, File, Form, UploadFile,status, Response
import filetype
import random
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import aiofiles
from config import CHECK_HEADER_RC5, ERROR_MSGS_BACKEND, MEDIA_TYPES
from utils.rand_num_gen import pseudo_rand_num, to_test_generator
from utils.md5 import start_hashing,compare_hash

from utils.rc5 import get_encoded_value, get_decoded_value
from utils.rsa import get_private_key, get_public_key, get_encryption_rsa, get_decrypted_rsa

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]
)

x = ""


@app.get("/pseudo_rand_num")
async def calc_rand_num(n:int):
    global x
    try:
        x, period, seq = pseudo_rand_num(n)
        return {
            'sequence': seq,
            'period': period
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Bad Request'
        )

@app.get("/pseudo_rand_num/test")
async def rand_num_test():
    global x
    try:
        prob,prob_act,pi_est,pi_act = to_test_generator(x)
        return {
            "probability" : prob,
            "actualProbability" : prob_act,
            "PIestimate" : pi_est,
            "PIactual" : pi_act
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No sequence were given to test'
        )

@app.post("/md5_hash")
async def md5_hash(
        input_str: str = Form(None),
        input_file: UploadFile = File(None)
):
    if input_str is not None:
        content = input_str
    elif input_file is not None:
        content = await input_file.read()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MSGS_BACKEND['NO_INPUT']
        )

    hash_val = start_hashing(content)
    return {"hashValue": hash_val}

@app.post("/md5_hash/check_integrity")
async def check_integrity_hash(
        input_file:UploadFile = File(None),
        control_file:UploadFile = File(None)
):
    try:
        content = await input_file.read()
        hash_compare = await control_file.read()
        hash_compare = hash_compare.decode('utf-8')
        hash_val = start_hashing(content)
        compare_res = compare_hash(hash_val, hash_compare)
        return {
            "hashValue" : hash_val,
            "hashCompare": hash_compare,
            "integrityPassed" : compare_res
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MSGS_BACKEND['NO_INPUT']
        )

@app.post("/rc5/encode")
async def rc5_hash(
        password_key: str = Form(None),
        input_str: str = Form(None),
        input_file: UploadFile = File(None)
):
    try:
        hex_key_string = start_hashing(password_key)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No password provided'
        )
    n_rand_nums,_,_ = pseudo_rand_num(random.randint(1, 100))
    rand_num = sum(n_rand_nums)
    if input_str is not None:
        content = bytes(input_str,'utf-8')
    elif input_file is not None:
        content = await input_file.read()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MSGS_BACKEND['NO_INPUT']
        )

    encrypted_line, iv = get_encoded_value(hex_key_string,rand_num,CHECK_HEADER_RC5+content)
    async with aiofiles.tempfile.NamedTemporaryFile(suffix=".txt",delete=False) as f:
        await f.write(iv)
        await f.write(b'\n')
        await f.write(encrypted_line)
        temp_path = f.name
    return FileResponse(
        path=temp_path,
        filename="encrypted_output.txt",
        media_type=MEDIA_TYPES['BYTES']
    )

@app.post("/rc5/decode")
async def rc5_decode(
        password_key: str= Form(None),
        encrypted_file: UploadFile = File(None)
):
    try:
        content = await encrypted_file.read()
        iv = content[:16]
        encoded_lines = content[17:]
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Input wasn’t provided"
        )
    hex_key_string = start_hashing(password_key)
    decrypted_line = get_decoded_value(hex_key_string,iv,encoded_lines)
    if not decrypted_line.startswith(CHECK_HEADER_RC5):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is incorrect"
        )
    decrypted_line = decrypted_line[len(CHECK_HEADER_RC5):]
    get_file_type = filetype.guess(decrypted_line)
    if get_file_type is None:
        try:
            to_text = decrypted_line.decode('utf-8')
            async with aiofiles.tempfile.NamedTemporaryFile(suffix=".txt", mode="w", encoding="utf-8",delete=False) as f:
                await f.write(to_text)
                temp_path = f.name
            return FileResponse(path=temp_path, filename="decrypted_line.txt", media_type="text/plain")
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password is incorrect"
            )
    else:
        file_extention = f".{get_file_type.extension}"
        async with aiofiles.tempfile.NamedTemporaryFile(suffix=file_extention,delete=False) as f:
            await f.write(decrypted_line)
            temp_path = f.name
        return FileResponse(path=temp_path, filename=f"decrypted_file{file_extention}", media_type=get_file_type.mime)


@app.get("/rsa/get_private_key")
async def rsa_get_private_key(
    password:str
):
    try:
        password_bits = password.encode('utf-8')
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MSGS_BACKEND['INCORRECT_PASSWORD_FORMAT']
        )
    try:
        prvt_ser_pem = get_private_key(password_bits)
        async with aiofiles.tempfile.NamedTemporaryFile(suffix=".pem", mode='wb',delete=False) as f:
            await f.write(prvt_ser_pem)
            temp_path = f.name
        return FileResponse(path=temp_path, filename="private_key.pem")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service is currently unavailable"
        )

@app.post("/rsa/get_public_key")
async def rsa_get_public_key(
    password:str= Form(None),
    private_file:UploadFile  = File(None)
):
    try:
        password_bits = password.encode('utf-8')
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MSGS_BACKEND['INCORRECT_PASSWORD_FORMAT']
        )
    try:
        pem_lines = await private_file.read()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MSGS_BACKEND['DAMAGED_OR_EMPTY_FILE']
        )
    try:
        pblc_ser_pem = get_public_key(pem_lines,password_bits)
        async with aiofiles.tempfile.NamedTemporaryFile(suffix=".pem", mode='wb',delete=False) as f:
            await f.write(pblc_ser_pem)
            temp_path = f.name
        return FileResponse(path=temp_path, filename="public_key.pem")

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service is currently unavailable"
        )

@app.post("/rsa/encrypt_file")
async def rsa_encrypt_file(
    public_file:UploadFile  = File(None),
    input_file: UploadFile  = File(None)
):
    try:
        input_bits = await input_file.read()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MSGS_BACKEND['DAMAGED_OR_EMPTY_FILE']
        )
    try:
        pem_lines = await public_file.read()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MSGS_BACKEND['DAMAGED_OR_EMPTY_FILE']
        )
    try:
        ciphertext = get_encryption_rsa(pem_lines, input_bits)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server wasn't able to encrypt the file",
            headers={"X-Error": "Internal Server Error"}
        )

    return Response(content=b''.join(ciphertext), media_type=MEDIA_TYPES['BYTES'])

@app.post("/rsa/decrypt_file")
async def rsa_decrypt_file(
    password:str= Form(None),
    private_file:UploadFile  = File(None),
    input_file: UploadFile  = File(None)
):
    try:
        password_bits = password.encode('utf-8')
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MSGS_BACKEND['INCORRECT_PASSWORD_FORMAT']
        )
    try:
        pem_lines = await private_file.read()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MSGS_BACKEND['DAMAGED_OR_EMPTY_FILE']
        )
    try:
        ciphertext = await input_file.read()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MSGS_BACKEND['DAMAGED_OR_EMPTY_FILE']
        )

    try:
        decrypted_bt = get_decrypted_rsa(pem_lines, ciphertext,password_bits)
        plaintext = b''.join(decrypted_bt)
        get_file_type = filetype.guess(plaintext)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server wasn't able to decrypt the file",
            headers={"X-Error": "Internal Server Error"}
        )
    file_extention = f".{get_file_type.extension}" if get_file_type else ".bin"
    media_type = get_file_type.mime if get_file_type else MEDIA_TYPES['BYTES']
    async with aiofiles.tempfile.NamedTemporaryFile(suffix=file_extention,delete=False) as f:
        await f.write(plaintext)
        temp_path = f.name
    return FileResponse(path=temp_path, filename=f"decrypted_file{file_extention}", media_type=media_type)