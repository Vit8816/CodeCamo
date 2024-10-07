import sys
import zlib
import random
import string
import base64

def xor_encrypt(data, key):
    return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data))

def insert_junk_code():
    junk_code = []
    for _ in range(random.randint(5, 15)):
        var_name = ''.join(random.choice(string.ascii_letters) for _ in range(5))
        junk_code.append(f"Local ${var_name} = {random.randint(1, 100)} * {random.randint(1, 100)}")
    return '\n'.join(junk_code)

def insert_random_junk_blocks(code_parts):
    code_with_junk = []
    for part in code_parts:
        code_with_junk.append(part)
        while random.random() > 0.30:
            junk = insert_junk_code()
            code_with_junk.append(junk)
    return '\n'.join(code_with_junk)

def anti_debugger_checks():
    return '''
Func _AntiDebugger()
    Local $iStartTime = TimerInit()
    For $i = 1 To 1000000
        ; Dummy loop
    Next
    If TimerDiff($iStartTime) > 1000 Then ; Check for slow execution (common in debugging)
        Exit ; Exit if debugging is detected
    EndIf
EndFunc

_AntiDebugger()
'''

def anti_reverse_engineering_checks():
    return '''
Func _CheckForTampering()
    Local $sFile = FileGetShortName(@ScriptFullPath)
    If FileExists($sFile & "_debugger") Or FileExists("/etc/ld.so.preload") Then
        Exit ; Exit if tampering is detected
    EndIf
EndFunc

_CheckForTampering()
'''

def obfuscate_autoit_code(code, encryption_key):
    encoded_code = base64.b64encode(xor_encrypt(code, encryption_key).encode()).decode()
    decryption_key_name = ''.join(random.choice(string.ascii_letters) for _ in range(random.randint(5, 10)))
    encrypted_data_name = ''.join(random.choice(string.ascii_letters) for _ in range(random.randint(5, 10)))
    obfuscated_code = f'''
Global $encrypted_code = "{encoded_code}"

Func _XorDecrypt($data, $key)
    Local $result = ""
    For $i = 1 To StringLen($data)
        $result &= Chr(BitXOR(Asc(StringMid($data, $i, 1)), Asc(StringMid($key, Mod($i - 1, StringLen($key)) + 1, 1))))
    Next
    Return $result
EndFunc

Global $decryption_key = "{encryption_key}"
Global $decrypted_code = BinaryToString(DecString(Base64Decode($encrypted_code)))

Func Base64Decode($s)
    Local $sData = BinaryToString($s, 4)
    Local $bin = Binary("")
    For $i = 1 To StringLen($sData)
        $bin &= Binary(StringMid($sData, $i, 1))
    Next
    Return $bin
EndFunc

Func DecString($s)
    Local $data = ""
    For $i = 1 To StringLen($s) Step 2
        $data &= Chr(Dec(StringMid($s, $i, 2)))
    Next
    Return $data
EndFunc

Execute($decrypted_code)
'''
    anti_debug_code = anti_debugger_checks()
    anti_reverse_code = anti_reverse_engineering_checks()
    code_parts = [
        anti_debug_code,
        anti_reverse_code,
        obfuscated_code
    ]
    final_code = insert_random_junk_blocks(code_parts)
    return final_code

def obfuscate_with_base64(code):
    enc = base64.b64encode(code.encode('utf-8')).decode('utf-8')
    obfuscated_code = f'Execute(BinaryToString(Base64Decode("{enc}")))'
    return obfuscated_code

def obfuscate_with_zlib(code):
    enc = base64.b64encode(zlib.compress(code.encode('utf-8'))).decode('utf-8')[::-1]
    obfuscated_code = f'Execute(BinaryToString(DecString(BinaryToString(Base64Decode("{enc}")))))'
    return obfuscated_code

try:
    code_name = sys.argv[1]
except:
    code_name = "main.au3"

with open(code_name, 'r') as f:
    code = f.read()

for _ in range(3):
    if random.random() > 0.5:
        code = obfuscate_with_base64(code)
        code = obfuscate_with_zlib(code)
    else:
        code = obfuscate_autoit_code(code, ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32)))

code = obfuscate_with_base64(code)
code = obfuscate_autoit_code(code, ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32)))

out_name = f"{code_name.split('.')[0]}_enc.au3"

with open(out_name, 'w') as f:
    f.write(code)

print(f"Obfuscated code saved as {out_name}")
