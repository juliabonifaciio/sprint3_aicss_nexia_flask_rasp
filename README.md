## 🔐 Configuração de Variáveis de Ambiente

Para garantir a segurança da aplicação, as credenciais e configurações sensíveis não são armazenadas diretamente no código.

Crie um arquivo chamado `.env` na raiz do projeto e adicione as seguintes variáveis:

```
SECRET_KEY=supersegredo
ADMIN_USER=admin
ADMIN_PASS=123
```

### 📌 Descrição

* **SECRET_KEY**: chave utilizada pelo Flask para proteger sessões
* **ADMIN_USER**: usuário de acesso à área administrativa
* **ADMIN_PASS**: senha de acesso à área administrativa

### ⚠️ Importante

* O arquivo `.env` **não deve ser versionado** no repositório
* Certifique-se de que ele está incluído no `.gitignore`
* Nunca compartilhe suas credenciais publicamente

### ▶️ Carregamento no projeto

As variáveis são carregadas utilizando a biblioteca:

* python-dotenv

No código:

```python
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
```
