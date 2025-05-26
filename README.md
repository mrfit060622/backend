# MrFit - Backend

Backend do projeto **MrFit**, desenvolvido em Flask, responsável por toda a lógica de negócio, cálculos nutricionais, geração de relatórios personalizados e integração com serviços externos.

---

## Tecnologias utilizadas

- Python 3.x
- Flask 3.x
- Flask-SQLAlchemy
- Flask-Mail
- MercadoPago SDK para Python
- Gunicorn para deploy em produção

---

## Funcionalidades principais

- API REST para cálculo e análise nutricional
- Geração de relatórios PDF personalizados para usuários pagos
- Integração com MercadoPago para gerenciamento de pagamentos
- Envio automático de e-mails com link para download do relatório gerado
---

## Estrutura do projeto

O backend está organizado em camadas para facilitar manutenção, testes e escalabilidade:

- **mrfit_app/**: Código principal do aplicativo Flask
  - **modelos/**: Definição das entidades e modelos ORM (relatórios, pagamentos, alimentos, plano_alimentar)
  - **rotas/**: Rotas e endpoints da API REST
  - **controles/**: Controladores que fazem a mediação entre rotas e serviços, garantindo separação clara das responsabilidades, além da possibilidade flexibilização simples de regras de negócio
  - **servicos/**: Lógica de negócio, cálculos nutricionais, geração de PDFs e integração com MercadoPago
  - **utils/**: Funções auxiliares, helpers e utilitários
- **config/**: Configurações da aplicação, variáveis de ambiente e setups

---

## Hospedagem

- Backend hospedado no **Render**

---

## Sobre o projeto

O backend oferece toda a inteligência do MrFit, permitindo entregar relatórios nutricionais e planos alimentares personalizados de acordo com as metas e dados de cada usuário, além de ser responsável por gerênciar toda a parte de integração com metodos de pagamento.

---

## Contato

Paulo Henrique de Freitas Matos  
[LinkedIn](https://www.linkedin.com/in/mr-pmatos/)