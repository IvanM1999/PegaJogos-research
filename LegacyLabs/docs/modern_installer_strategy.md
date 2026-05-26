# 📦 Estratégia para o Novo Instalador (Modern Deployment)

Este documento define como criaremos um instalador moderno para o PegaJogo que garanta o funcionamento em Windows 10/11.

## 1. Tecnologia Escolhida
- **Inno Setup (ou NSIS):** Pela robustez no registro de componentes COM e manipulação de arquivos de sistema.

## 2. Componentes do Pacote
O instalador deve empacotar e distribuir:
1.  **Binários Core:** `PegaJogo.exe`.
2.  **Runtime VB6:** `MSVBVM60.DLL` (instalada no diretório do app para portabilidade).
3.  **ActiveX Layer:** OCXs da pasta `bin` registradas via `regsvr32` silencioso.
4.  **Firebird Zero-Config:**
    - Utilizar o **Firebird Embedded** (`fbembed.dll` renomeada para `fbclient.dll`).
    - Incluir a `fbudf.dll` na subpasta `UDF/`.
5.  **Bypass de Rede:** Script para adicionar automaticamente o redirecionamento de `pegajogo.com.br` para `127.0.0.1` no arquivo `hosts`.

## 3. Script de Instalação (Draft de Lógica)
```pascal
[Files]
Source: "PegaJogo.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "bin\*.ocx"; DestDir: "{app}\bin"; Flags: regserver
Source: "bin\*.dll"; DestDir: "{app}\bin"; Flags: ignoreversion
Source: "db\pega.fdb"; DestDir: "{app}\db"; Flags: onlyifdoesntexist

[Run]
Filename: "{app}\PegaJogo.exe"; Description: "Lançar PegaJogo"; Flags: postinstall nowait
```

## 4. Vantagens do Novo Instalador
- **Instalação Silenciosa:** O usuário não precisa saber como registrar DLLs manualmente.
- **Isolação:** Ao colocar as DLLs na pasta do app (técnica de DLL redirection ou manifestos), evitamos "poluir" o `System32`.

---
*LegacyLabs - Planejamento de Reimplantação*