# 📦 Análise de Extração: Instalar_PegaJogo.exe

## 1. Perfil do Binário
- **Tipo:** PE32 (32-bit) GUI.
- **Compilador Identificado:** Borland Delphi (Seções `CODE`, `DATA`, `BSS`).
- **Payload:** 4.35 MB de dados em Overlay (Tamanho total 4.4 MB vs Stub de 80 KB).

## 2. Evidências de Empacotamento
O arquivo apresenta um comportamento de "Self-Extracting Archive" (SFX). As importações de `kernel32.dll` (`CreateProcessA`, `WriteFile`, `CreateDirectoryA`) confirmam que a função primária deste binário é descompactar arquivos em uma pasta temporária ou de destino e registrá-los no sistema.

## 3. Metodologia de Descompactação
Para obter os arquivos originais sem executar o instalador (evitando alterações indesejadas no registro do Windows Host):

1.  **Ferramenta Primária:** `innoextract`
    - **Status:** Testar para confirmar a versão do Inno Setup.
2.  **Ferramenta Secundária:** `innounp` (Inno Setup Unpacker)
    - **Objetivo:** Recuperar o script `.iss` original, se possível, para entender onde o instalador coloca cada DLL e OCX.
3.  **Análise de Recursos:** Utilizar o `Resource Hacker` para verificar se há arquivos comprimidos dentro da seção `.rsrc`.

## 4. Arquivos Esperados na Extração
Com base na análise do ecossistema, o instalador deve conter:
- `PegaJogo.exe` (O binário VB6 principal).
- `bin/*.ocx` e `bin/*.dll` (Componentes ActiveX).
- `db/*.fdb` ou `db/*.gdb` (O banco de dados Firebird).
- `Games/` (Pasta raiz com a estrutura de categorias).

---
*Documento técnico de laboratório - LegacyLabs*