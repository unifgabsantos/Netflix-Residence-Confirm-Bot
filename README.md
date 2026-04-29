# Netflix Household Confirm Bot

Automação em Python que monitora sua caixa de entrada do Gmail e confirma automaticamente solicitações de atualização de residência da Netflix.

---

## 🚀 O que o projeto faz

Este bot:

- Monitora sua caixa de entrada do Gmail em tempo real (polling)
- Filtra emails específicos da Netflix com o assunto:
  **"Importante: Como atualizar sua residência Netflix"**
- Verifica se o email foi recebido nos últimos 15 minutos
- Extrai o link correto do botão "Sim, fui eu"
- Abre o link automaticamente usando Selenium em modo invisível (headless)
- Clica automaticamente no botão **"Confirmar atualização"**

---

## 🧠 Como funciona

Fluxo completo: Gmail → API → Filtro de email → Parser HTML → Extração de link → Selenium → Clique automático

---

## 📦 Tecnologias utilizadas

- Python 3
- Gmail API (Google)
- BeautifulSoup (parsing HTML)
- Selenium (automação de navegador)
- WebDriver Manager

---

## ⚙️ Instalação

Clone o repositório:

git clone https://github.com/unifgabsantos/Netflix-Residence-Confirm-Bot.git

cd Netflix-Residence-Confirm-Bot

Instale as dependências: 

pip install -r requirements.txt

## 🔐 Configuração (Gmail API)

1. Acesse o Google Cloud Console  
2. Ative a **Gmail API**  
3. Crie credenciais OAuth 2.0  
4. Baixe o arquivo `credentials.json`  
5. Coloque o arquivo na raiz do projeto  

### Primeira execução

- Será aberto um navegador para login  
- Um arquivo `token.pkl` será gerado automaticamente

## ▶️ Como executar

bash
python main.py
O script irá:

- Rodar continuamente  
- Verificar novos emails a cada 30 segundos  

### 💡 Dica

Para melhor funcionamento, deixe o script rodando em um ambiente sempre ativo, como:

- Um Raspberry Pi  
- Um servidor/VPS  
- Um computador que fique ligado constantemente  

Exemplo: você pode rodar isso em um Raspberry Pi na sua rede e deixar o bot funcionando 24/7 sem depender do seu computador principal.

---

## ⚠️ Observações importantes

- O link da Netflix expira em ~15 minutos  
- O bot só processa emails dentro desse período  
- O navegador roda em modo invisível (headless)  
- Evita processar o mesmo email mais de uma vez  

---

## 🔒 Segurança

- Nunca compartilhe seu `credentials.json` ou `token.pkl`  
- Este projeto é para uso pessoal  
- Não recomendado para uso em larga escala ou produção sem ajustes  

---

## 📄 Licença

Uso livre para fins educacionais e pessoais.
