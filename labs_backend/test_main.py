import os

from fastapi.testclient import TestClient
import main

client = TestClient(main.app)

def test_pseudo_rand_num_okay():
    response = client.get("pseudo_rand_num?n=49")
    assert response.status_code == 200
    assert response.json() == {
        'sequence': '3 1680 860304 74082 181410 607420 620836 1198375 1200052 2058676 1272454 1379782 1805792 1819208 299596 301273 1159897 373675 481003 907013 920429 1497968 1499645 261118 1572047 1679375 8234 21650 599189 600866 1459490 673268 780596 1206606 1220022 1797561 1799238 560711 1871640 1978968 307827 321243 898782 900459 1759083 972861 1080189 1506199 1519615',
        'period': 49
    }
def test_pseudo_rand_num_bad_request():
    response = client.get("pseudo_rand_num?n=test")
    assert response.status_code == 422
    assert response.json() == {
        'detail': [
            {
                'input': 'test',
                'loc': ['query', 'n',],
                'msg': 'Input should be a valid integer, unable to parse string as an integer',
                'type': 'int_parsing',
            },
        ],
    }
def test_rand_num_test_okay():
    main.x = [3, 1680, 860304, 74082, 181410, 607420, 620836, 1198375, 1200052, 2058676, 1272454, 1379782, 1805792, 1819208, 299596, 301273, 1159897, 373675, 481003, 907013, 920429, 1497968, 1499645, 261118, 1572047, 1679375, 8234, 21650, 599189, 600866, 1459490, 673268, 780596, 1206606, 1220022, 1797561, 1799238, 560711, 1871640, 1978968, 307827, 321243, 898782, 900459, 1759083, 972861, 1080189, 1506199, 1519615]
    response = client.get("pseudo_rand_num/test")
    assert response.status_code == 200
    assert response.json() == {
        "probability": 0.4166666666666667,
        "actualProbability": 0.6079271018540267,
        "PIestimate": 3.794733192202055,
        "PIactual": 3.141592653589793
    }
def test_rand_num_test_empty_x():
    main.x = []
    response = client.get("pseudo_rand_num/test")
    assert response.status_code == 400
    assert response.json() == {
        'detail': 'No sequence were given to test'
    }
def test_md5_hash_okay():
    response = client.post("md5_hash", data={"input_str": "babak"})
    assert response.status_code == 200
    assert response.json() == {
        "hashValue": "86c6f808481120d10b109c7fd60f8fac"
    }
def test_md5_hash_lab_cases():
    assert client.post("md5_hash", data={"input_str": ""}).json() == {"hashValue": "d41d8cd98f00b204e9800998ecf8427e"}
    assert client.post("md5_hash", data={"input_str": "a"}).json() == {"hashValue": "0cc175b9c0f1b6a831c399e269772661"}
    assert client.post("md5_hash", data={"input_str": "abc"}).json() == {"hashValue": "900150983cd24fb0d6963f7d28e17f72"}
    assert client.post("md5_hash", data={"input_str": "message digest"}).json() == {"hashValue": "f96b697d7cb7938d525a2f31aaf161d0"}
    assert client.post("md5_hash", data={"input_str": "abcdefghijklmnopqrstuvwxyz"}).json() == {"hashValue": "c3fcd3d76192e4007dfb496cca67e13b"}
    assert client.post("md5_hash", data={"input_str": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"}).json() == {"hashValue": "d174ab98d277d9f5a5611c2c9f419d9f"}
    assert client.post("md5_hash", data={"input_str": "12345678901234567890123456789012345678901234567890123456789012345678901234567890"}).json() == {"hashValue": "57edf4a22be3c955ac49da2e2107b67a"}
def test_md5_hash_without_input():
    response = client.post("md5_hash", data={})
    assert response.status_code == 400
    assert response.json() == {
        "detail":"Input wasn’t provided"
    }
def test_md5_hash_file_input():
    with open("labs_backend/test.txt", "rb") as f:
        response = client.post(
            "/md5_hash",
            files={"input_file": ("labs_backend/test.txt", f, "text/plain")}
        )
    assert response.status_code == 200
    assert response.json() == {'hashValue': '572f57cc76e4412bfe03da97a59f3db5'}
def test_check_integrity_okay_untouched():
    content = b"babak"
    hash_value = "86c6f808481120d10b109c7fd60f8fac"
    files = {
        "input_file": ("file.txt", content, "text/plain"),
        "control_file": ("hash.txt", hash_value.encode("utf-8"), "text/plain"),
    }
    response = client.post("/md5_hash/check_integrity", files=files)
    assert response.status_code == 200
    assert response.json() == {
        "hashValue": hash_value,
        "hashCompare": hash_value,
        "integrityPassed":True
    }
def test_check_integrity_okay_tempered():
    content = b"babak"
    wrong_hash = "bababoi"
    files = {
        "input_file": ("file.txt", content, "text/plain"),
        "control_file": ("hash.txt", wrong_hash.encode("utf-8"), "text/plain"),
    }
    response = client.post("/md5_hash/check_integrity", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["hashValue"] != wrong_hash
    assert data["hashCompare"] == wrong_hash
    assert data["integrityPassed"] is False
def test_check_integrity_no_file():
    response = client.post("/md5_hash/check_integrity")
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Input wasn’t provided"
    }
def test_rc5_encode_okay_str_input():
    response = client.post(
        "/rc5/encode", data={
            "password_key": "babak",
            "input_str": "babak"
        }
    )
    assert response.status_code == 200
    assert len(response.content) > 0
    assert response.headers["content-type"] == "application/octet-stream"
    assert response.headers["content-disposition"] == 'attachment; filename="encrypted_output.txt"'
def test_rc5_encode_okay_file_input(tmp_path):
    test_file = tmp_path/"input.txt"
    test_file.write_text("babak")
    with open(test_file, "rb") as f:
        response = client.post(
            "/rc5/encode",
            data={"password_key": "babak"},
            files={"input_file": ("input.txt", f, "text/plain")}
        )
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/octet-stream"
    assert "encrypted_output.txt" in response.headers["content-disposition"]
    assert len(response.content) > 0
def test_rc5_encode_no_input():
    response = client.post(
        "/rc5/encode",
        data={"password_key": "babak"}
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Input wasn’t provided"
    }
def test_rc5_encode_no_password():
    response = client.post(
        "/rc5/encode",
        data={"input_str": "babak"}
    )
    assert response.status_code == 400
    assert response.json() == {
        'detail':'No password provided'
    }
def test_rc5_decode_okay(tmp_path):
    test_file = tmp_path / "test_input.txt"
    test_file.write_text("babak", encoding="utf-8")
    with open(test_file, "rb") as f:
        enc_response = client.post(
            "/rc5/encode",
            data={"password_key": "babak"},
            files={"input_file": ("test_input.txt", f, "text/plain")},
        )
    assert enc_response.status_code == 200
    enc_file = tmp_path / "encrypted_test_output.txt"
    enc_file.write_bytes(enc_response.content)
    with open(enc_file, "rb") as f:
        dec_response = client.post(
            "/rc5/decode",
            data={"password_key": "babak"},
            files={"encrypted_file": ("encrypted_test_output.txt", f, "application/octet-stream")},
        )
    assert dec_response.status_code == 200
    assert dec_response.headers["content-type"] == "text/plain; charset=utf-8"
    assert dec_response.headers["content-disposition"] == 'attachment; filename="decrypted_line.txt"'
    assert dec_response.content == b'babak'
    os.remove(test_file)
    os.remove(enc_file)
def test_rc5_decode_no_file():
    response = client.post(
        "/rc5/decode",
        data={"password_key": "babak"},
        files={}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Input wasn’t provided"}
def test_rc5_decode_wrong_password(tmp_path):
    test_file = tmp_path / "wrongpass_input.txt"
    test_file.write_text("babak")
    with open(test_file, "rb") as f:
        enc_response = client.post(
            "/rc5/encode",
            data={"password_key": "babak"},
            files={"input_file": ("wrongpass_input.txt", f, "text/plain")},
        )
    assert enc_response.status_code == 200
    enc_file = tmp_path / "wrongpass_encrypted.txt"
    enc_file.write_bytes(enc_response.content)
    with open(enc_file, "rb") as f:
        dec_response = client.post(
            "/rc5/decode",
            data={"password_key": "HELLPPPPвпорлворпловапрловарполав"},
            files={"encrypted_file": ("wrongpass_encrypted.txt", f, "application/octet-stream")},
        )
    assert dec_response.status_code == 400
    assert dec_response.json() == {"detail": "Password is incorrect"}
    os.remove(test_file)
    os.remove(enc_file)
def test_rsa_get_private_key_success(tmp_path, ):
    response = client.get("/rsa/get_private_key", params={"password": "mybabak"})
    assert response.status_code == 200
    assert response.headers["content-disposition"].startswith("attachment; filename=")
    assert b"BEGIN ENCRYPTED PRIVATE KEY" in response.content
def test_rsa_get_private_key_bad_password():
    response = client.get("/rsa/get_private_key", params={})
    assert response.status_code == 422
    assert response.json() == {'detail': [{'input': None,
        'loc': [
            'query',
            'password'
        ],
        'msg': 'Field required',
        'type': 'missing',
        },
    ]}
def test_rsa_get_private_key_service_unavailable():
    response = client.get("/rsa/get_private_key", params={"password": ""})
    assert response.status_code == 503
    assert response.json() == {"detail": "Service is currently unavailable"}
def test_rsa_get_public_key_okay(tmp_path):
    private_response = client.get("/rsa/get_private_key", params={"password": "mybabak"})
    private_file_path = tmp_path / "private_key.pem"
    private_file_path.write_bytes(private_response.content)
    with open(private_file_path, "rb") as f:
        files = {"private_file": ("private_key.pem", f, "application/octet-stream")}
        response = client.post("/rsa/get_public_key", data={"password": "mybabak"}, files=files)
    assert response.status_code == 200
    assert response.headers["content-disposition"].startswith("attachment; filename=")
    assert b"BEGIN PUBLIC KEY" in response.content
def test_rsa_get_public_key_missing_password(tmp_path):
    private_response = client.get("/rsa/get_private_key", params={"password": "mybabak"})
    private_file_path = tmp_path / "private_key.pem"
    private_file_path.write_bytes(private_response.content)
    with open(private_file_path, "rb") as f:
        files = {"private_file": ("private_key.pem", f, "application/octet-stream")}
        response = client.post("/rsa/get_public_key", files=files)
    assert response.status_code == 400
    assert response.json()=={
        'detail':"Incorrect password format"
    }
def test_rsa_get_public_key_damaged_file():
    class BrokenUploadFile:
        async def read(self):
            raise ValueError("Value cannot be negative")
    files = {"private_file": BrokenUploadFile()}
    data = {"password": "mypassword"}
    response = client.post("/rsa/get_public_key", data=data, files=files)
    assert response.status_code == 400
    assert response.json() == {'detail': 'There was an error parsing the body'}
def test_rsa_encrypt_file_okay(tmp_path):
    private_response = client.get("/rsa/get_private_key", params={"password": "mybabak"})
    private_key_path = tmp_path / "private_key.pem"
    private_key_path.write_bytes(private_response.content)

    with open(private_key_path, "rb") as f:
        files = {"private_file": ("private_key.pem", f, "application/octet-stream")}
        public_res = client.post("/rsa/get_public_key", data={"password": "mybabak"}, files=files)
    public_key_path = tmp_path / "public_key.pem"
    public_key_path.write_bytes(public_res.content)

    with open(public_key_path, "rb") as pub_key, open("labs_backend/test.txt", "rb") as input_f:
        files = {
            "public_file": ("public.pem", pub_key, "application/octet-stream"),
            "input_file": ("input.txt", input_f, "text/plain")
        }
        response = client.post("/rsa/encrypt_file", files=files)

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/octet-stream"
def test_rsa_encrypt_file_empty_input_file(tmp_path):
    private_response = client.get("/rsa/get_private_key", params={"password": "mybabak"})
    private_key_path = tmp_path / "private_key.pem"
    private_key_path.write_bytes(private_response.content)

    with open(private_key_path, "rb") as f:
        files = {"private_file": ("private_key.pem", f, "application/octet-stream")}
        public_res = client.post("/rsa/get_public_key", data={"password": "mybabak"}, files=files)
    public_key_path = tmp_path / "public_key.pem"
    public_key_path.write_bytes(public_res.content)

    with open(public_key_path, "rb") as pub_key:
        files = {
            "public_file": ("public.pem", pub_key, "application/octet-stream"),
        }
        response = client.post("/rsa/encrypt_file", files=files)
    assert response.status_code == 400
    assert response.json() == {"detail": "File is damaged or empty"}
def test_rsa_encrypt_file_no_ile():
    response = client.post("/rsa/encrypt_file", files={})
    assert response.status_code == 400
    assert response.json() == {"detail": "File is damaged or empty"}
def test_rsa_decrypt_file_okay(tmp_path):
    private_response = client.get("/rsa/get_private_key", params={"password": "mybabak"})
    private_key_path = tmp_path / "private_key.pem"
    private_key_path.write_bytes(private_response.content)

    with open(private_key_path, "rb") as f:
        files = {"private_file": ("private_key.pem", f, "application/octet-stream")}
        public_res = client.post("/rsa/get_public_key", data={"password": "mybabak"}, files=files)
    public_key_path = tmp_path / "public_key.pem"
    public_key_path.write_bytes(public_res.content)

    with open(public_key_path, "rb") as pub_key, open("labs_backend/test.txt", "rb") as input_f:
        files = {
            "public_file": ("public.pem", pub_key, "application/octet-stream"),
            "input_file": ("input.txt", input_f, "text/plain")
        }
        encrypted_res = client.post("/rsa/encrypt_file", files=files)

    encrypted_file_path = tmp_path / "encrypted_file.bin"
    encrypted_file_path.write_bytes(encrypted_res.content)

    with open(private_key_path, "rb") as priv_key, open(encrypted_file_path, "rb") as enc_file:
        files = {
            "private_file": ("private_key.pem", priv_key, "application/octet-stream"),
            "input_file": ("encrypted_file.bin", enc_file, "application/octet-stream")
        }
        data = {"password": "mybabak"}
        response = client.post("/rsa/decrypt_file", data=data, files=files)

    assert response.status_code == 200
    assert response.headers["content-disposition"].startswith("attachment; filename=")
def test_rsa_decrypt_file_empty_input_file(tmp_path):
    private_response = client.get("/rsa/get_private_key", params={"password": "mybabak"})
    private_key_path = tmp_path / "private_key.pem"
    private_key_path.write_bytes(private_response.content)
    with open(private_key_path, "rb") as priv_key:
        files = {
            "private_file": ("private_key.pem", priv_key, "application/octet-stream"),
        }
        response = client.post("/rsa/decrypt_file", data={"password": "mybabak"}, files=files)
    assert response.status_code == 400
    assert response.json() == {"detail": "File is damaged or empty"}
def test_rsa_decrypt_file_empty_private_file(tmp_path):
    input_file_content = b"Encrypted content"
    files = {
        "input_file": ("input.bin", input_file_content, "application/octet-stream")
    }
    response = client.post("/rsa/decrypt_file", data={"password": "mybabak"}, files=files)
    assert response.status_code == 400
    assert response.json() == {"detail": "File is damaged or empty"}
def test_rsa_decrypt_file_no_file():
    response = client.post("/rsa/decrypt_file", data={"password": "mybabak"}, files={})
    assert response.status_code == 400
    assert response.json() == {"detail": "File is damaged or empty"}
