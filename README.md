# Trabalho 2 - VV&T: Geração de Códigos e Testes Automatizados

Este projeto implementa um sistema de geração automática de códigos identificadores únicos para produtos, utilizando Python, MySQL e testes automatizados com Pytest.

## Estrutura do Projeto

- `schema.sql`: Script SQL para criação do banco de dados `db_produtos` e tabela `produtos`, incluindo dados de exemplo.
- `app.py`: Código Python principal contendo funções para conexão com MySQL, geração de códigos e inserção de produtos.
- `test_gerador_codigo.py`: Suíte de testes unitários para validar a lógica de geração de códigos.
- `pytest_output.txt`: Resultado da execução dos testes (8 passed).
- `ENTREGA_FINAL.docx`: Documento de entrega contendo códigos, testes e resultados.
- `gerar_entrega_docx_final.py`: Script para gerar o documento DOCX de entrega.

## Requisitos

- Python 3.8+
- MySQL Server (versão 8.0+ recomendada)
- Dependências Python listadas em `requirements.txt`

## Instalação e Configuração

1. **Instalar dependências Python:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configurar MySQL:**
   - Certifique-se de que o MySQL está rodando.
   - Execute o script `schema.sql` para criar o banco e tabela:
     ```bash
     mysql -u root -p < schema.sql
     ```

3. **Configurar variáveis de ambiente (opcional):**
   ```bash
   export MYSQL_HOST=localhost
   export MYSQL_USER=root
   export MYSQL_PASSWORD=sua_senha
   export MYSQL_DATABASE=db_produtos
   ```

## Como Executar

1. **Executar o script principal (inserir um produto de exemplo):**
   ```bash
   python app.py
   ```

2. **Executar os testes:**
   ```bash
   python -m pytest -q
   ```

## Funcionalidades

- **Geração de Código:** Calcula automaticamente o próximo código sequencial para um grupo de produtos, com formato `PAÍS+GRUPO+SEQUÊNCIA_4DIG+TIPO_ALIMENTO`.
- **Validação:** Verifica parâmetros de entrada e previne duplicidade.
- **Testes Isolados:** Utiliza mocks para testar sem depender de banco real.

## Resultados dos Testes

```
........                                                                 [100%]
8 passed in 0.05s
```

## Entrega

O documento `ENTREGA_FINAL.docx` contém todos os códigos, explicações e resultados conforme solicitado no enunciado.

## Autor

Samuel VPS (ou dupla, se aplicável)