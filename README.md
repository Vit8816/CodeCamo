# CodeCamo

**CodeCamo** è uno strumento di offuscamento del codice progettato per rendere il tuo codice sorgente più difficile da analizzare e comprendere. Utilizzando tecniche di crittografia e inserimento di codice spazzatura, CodeCamo offre un modo semplice per proteggere il tuo codice AutoIt e aumentarne la sicurezza.

## Funzionalità

- **Crittografia XOR**: Il codice sorgente viene crittografato utilizzando una chiave di crittografia XOR.
- **Inserimento di codice spazzatura**: Aggiunge blocchi di codice casuali per confondere ulteriormente l'analizzatore.
- **Controlli anti-debugger**: Implementa controlli per rilevare se il codice viene eseguito in un ambiente di debug.
- **Controlli anti-reverse engineering**: Inserisce controlli per verificare eventuali manomissioni del codice.
- **Compressione**: Supporta l'offuscamento tramite compressione zlib e codifica Base64.

## Utilizzo

1. Salva il codice sorgente che desideri offuscare in un file `.au3`.
2. Esegui `CodeCamo` passando il nome del file come argomento:
   ```bash
   python CodeCamo.py nome_file.au3
   ```
3. Il codice offuscato verrà salvato con un suffisso `_enc.au3`.

## Esempio

Se il tuo file sorgente si chiama `script.au3`, puoi eseguire:
```bash
python CodeCamo.py script.au3
```
Il risultato sarà un file chiamato `script_enc.au3`, contenente il tuo codice offuscato.

## Installazione

Assicurati di avere Python installato. Puoi scaricarlo [qui](https://www.python.org/downloads/).

## Contributi

Se desideri contribuire a CodeCamo, sentiti libero di aprire un problema o una richiesta di pull.

---

# CodeCamo

**CodeCamo** is a code obfuscation tool designed to make your source code harder to analyze and understand. Using encryption techniques and junk code insertion, CodeCamo offers a simple way to protect your AutoIt code and enhance its security.

## Features

- **XOR Encryption**: The source code is encrypted using an XOR encryption key.
- **Junk Code Insertion**: Random blocks of code are added to further confuse the analyzer.
- **Anti-Debugger Checks**: Implements checks to detect if the code is being run in a debugging environment.
- **Anti-Reverse Engineering Checks**: Inserts checks to verify if the code has been tampered with.
- **Compression**: Supports obfuscation through zlib compression and Base64 encoding.

## Usage

1. Save the source code you want to obfuscate in a `.au3` file.
2. Run `CodeCamo` passing the file name as an argument:
   ```bash
   python CodeCamo.py filename.au3
   ```
3. The obfuscated code will be saved with a `_enc.au3` suffix.

## Example

If your source file is named `script.au3`, you can run:
```bash
python CodeCamo.py script.au3
```
The result will be a file named `script_enc.au3`, containing your obfuscated code.

## Installation

Make sure you have Python installed. You can download it [here](https://www.python.org/downloads/).

## Contributions

If you'd like to contribute to CodeCamo, feel free to open an issue or a pull request.
