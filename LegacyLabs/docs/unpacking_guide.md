# 🔍 Guia de Experimento: Unpacking e Análise de Strings

Este guia descreve os passos para descompactar o `PegaJogo.exe` e extrair informações críticas de rede e banco de dados.

## 1. Identificação do Packer
Antes de tentar descompactar, use uma das seguintes ferramentas para confirmar o assinante do packer:
- **Detect It Easy (DIE):** Altamente recomendado para identificar assinaturas de compressores.
- **PEiD:** Alternativa clássica (embora datada).

## 2. Procedimento de Unpacking (UPX)
Se o DIE confirmar que o arquivo está em **UPX**, utilize o terminal:
```bash
upx -d PegaJogo.exe -o PegaJogo_unpacked.exe
```
*Nota: Se o binário foi modificado para impedir o unpacking automático (UPX scrambling), será necessário um depurador.*

## 3. Extração de Strings e URLs
Após descompactar (ou se o unpacking falhar), execute a extração de strings para procurar por padrões de conexão:

### Comandos Úteis:
Usando o `Strings.exe` (Sysinternals):
```bash
strings.exe -n 6 PegaJogo.exe > strings_output.txt
```

### O que procurar no `strings_output.txt`:
- **URLs:** Procurar por `http://`, `https://` ou `.php`.
- **SQL:** Procurar por `SELECT`, `INSERT`, `UPDATE` ou nomes de tabelas.
- **Firebird:** Procurar por caminhos de arquivos `.fdb` ou `.gdb`.
- **IPs:** Padrões de endereços IP (ex: `200.xxx.xxx.xxx`).

## 4. Próximos Passos se o Arquivo estiver Protegido
Se ferramentas automáticas falharem (indicação de MoleBox ou Aspack), o próximo passo envolve:
1. Realizar um **Memory Dump** do processo enquanto ele está rodando (com o Scylla ou Process Hacker).
2. Analisar o dump de memória em busca das strings que são descriptografadas apenas durante o tempo de execução.

---
*LegacyLabs - Pesquisa de Software Legado*