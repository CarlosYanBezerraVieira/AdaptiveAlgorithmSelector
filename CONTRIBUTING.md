# Contributing Guide

Antes de começar, leia este guia para garantir que todas as contribuições sigam o mesmo padrão.

## Pré-requisitos

* Python 3.12
* Git
* Conta no GitHub

## Configurando o ambiente

Clone o repositório:

```bash
git clone <https://github.com/CarlosYanBezerraVieira/AdaptiveAlgorithmSelector.git>
cd AdaptiveAlgorithmSelector
```

Instale as dependências de desenvolvimento:

```bash
pip install -r requirements-dev.txt
```

## Fluxo de trabalho

### 1. Atualize sua branch local

```bash
git checkout main
git pull origin main
```

### 2. Crie uma branch para sua tarefa

Utilize um dos padrões abaixo:

```text
feature/nome-da-feature
fix/nome-do-bug
docs/documentacao
test/adicao-de-testes
```

Exemplos:

```bash
git checkout -b feature/questionario
git checkout -b fix/calculo-pontuacao
```

### 3. Desenvolva a funcionalidade

Realize as alterações necessárias no código.

### 4. Execute as verificações antes de enviar

Verifique a qualidade do código:

```bash
ruff check .
```

Execute os testes:

```bash
pytest
```

### 5. Faça o commit

Utilize Conventional Commits:

```text
feat: adiciona nova funcionalidade
fix: corrige erro de cálculo
docs: atualiza documentação
test: adiciona testes
refactor: melhora estrutura do código
chore: manutenção do projeto
ci: altera configuração de CI/CD
```

## link de referência: https://www.conventionalcommits.org/en/v1.0.0/

Exemplos:

```bash
git commit -m "feat: add questionnaire engine"
git commit -m "fix: correct score calculation"
```

### 6. Envie sua branch

```bash
git push origin nome-da-branch
```

### 7. Abra um Pull Request

Ao criar o Pull Request:

* Descreva claramente as alterações realizadas.
* Explique como testar a funcionalidade.
* Preencha o template de Pull Request.

## Regras do projeto

* Não faça push diretamente na branch `main`.
* Toda alteração deve ser feita através de Pull Request.
* Todo Pull Request precisa de aprovação.
* O GitHub Actions deve passar sem erros.
* O código deve passar no Ruff e nos testes.
