# Como servir aplicativos Flask com o uWSGI e o Nginx no Ubuntu 18.04   

https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04-pt

## Introducao   

Neste guia, você construirá um aplicativo Python usando o microframework do Flask no Ubuntu 18.04. A maior parte deste artigo será sobre como configurar o [servidor do aplicativo uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/) e como iniciar o aplicativo e configurar o [Nginx](https://www.nginx.com/) para atuar como um proxy reverso no front-end.

## Pré-requisitos   
Antes de iniciar este guia, você deve ter:   
* Um servidor com o Ubuntu 18.04 instalado e um usuário não raiz com privilégios sudo. Siga nosso [guia de configuração inicial do servidor](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-18-04) para orientação.
* O Nginx instalado, seguindo os Passos 1 e 2 de [Como Instalar o Nginx no Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-18-04).
* Um nome de domínio configurado para apontar para o seu servidor. Você pode comprar um no [Namecheap](https://namecheap.com) ou obter um de graça no [Freenom](http://www.freenom.com/en/index.html). Você pode aprender como apontar domínios para o DigitalOcean seguindo a relevante [documentação para domínios e DNS](https://www.digitalocean.com/docs/networking/dns/). Certifique-se de criar os seguintes registros DNS:
    * Um registro com o ```your_domain <^>``` apontando para o endereço IP público do seu servidor.
    * Um registro com o ```www.your_domain``` apontando para o endereço IP público do seu servidor.
* Familiaridade com a uWSGI, nosso servidor do aplicativo, e as especficiações da WSGI. [Este debate](https://www.digitalocean.com/community/tutorials/how-to-set-up-uwsgi-and-nginx-to-serve-python-apps-on-ubuntu-14-04#definitions-and-concepts) sobre definições e conceitos examinará ambos em detalhes.

---

# Passo 1 — Instalando os componentes dos repositórios do Ubuntu
Nosso primeiro passo será instalar todas as partes dos repositórios do Ubuntu que vamos precisar. Vamos instalar o ```pip``` e o gerenciador de pacotes Python para gerenciar nossos componentes Python. Também vamos obter os arquivos de desenvolvimento do Python necessários para construir a uWSGI.

Primeiramente, vamos atualizar o índice local de pacotes e instalar os pacotes que irão nos permitir construir nosso ambiente Python. Estes incluem o ```python3-pip```, junto com alguns outros pacotes e ferramentas de desenvolvimento necessários para um ambiente de programação robusto:

```
$ sudo apt update
$ sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
```

Com esses pacotes instalados, vamos seguir em frente para criar um ambiente virtual para nosso projeto.

---

## Passo 2 — Criando um Ambiente Virtual em Python
Em seguida, vamos configurar um ambiente virtual para isolar nosso aplicativo Flask dos outros arquivos Python no sistema.

Inicie instalando o pacote ```python3-venv```, que instalará o módulo ```venv```:

```
$ sudo apt install virtualenv
$ sudo apt install python3.8 python3.8-dev
```

Em seguida, vamos fazer um diretório pai para nosso projeto Flask. Acesse o diretório após criá-lo:

```
mkdir ~/myproject
cd ~/myproject
```

Crie um ambiente virtual para armazenar os requisitos Python do projeto Flask digitando:

```
$ virtualenv myprojectenv -p python3.8
```

Isso instalará uma cópia local do Python e do ```pip``` para um diretório chamado myprojectenv dentro do diretório do seu projeto.

Antes de instalar aplicativos no ambiente virtual, você precisa ativá-lo. Faça isso digitando:

```
$ source myprojectenv/bin/activate
```

Seu prompt mudará para indicar que você agora está operando no ambiente virtual. Ele se parecerá com isso ```(myprojectenv)user@host:~/myproject$```.

---

## Passo 3 — Configurando um aplicativo Flask
Agora que você está no seu ambiente virtual, instale o Flask e a uWSGI e comece a projetar o seu aplicativo.

Primeiramente, vamos instalar o ```wheel``` com a instância local do ```pip``` para garantir que nossos pacotes serão instalados mesmo se estiverem faltando arquivos wheel:

```
$ pip install wheel
```

Em seguida, vamos instalar o Flask e a uWSGI:

```
$ pip install uwsgi flask
```

### Criando um App de exemplo
Agora que você tem o Flask disponível, você pode criar um aplicativo simples. O Flask é um microframework. Ele não inclui muitas das ferramentas que os frameworks mais completos talvez tenham. Ele existe, principalmente, como um módulo que você pode importar para seus projetos para ajudá-lo na inicialização de um aplicativo Web.

Embora seu aplicativo possa ser mais complexo, vamos criar nosso app Flask em um único arquivo, chamado ```myproject.py```:

```
$ vi ~/myproject/myproject.py
```

O código do aplicativo ficará neste arquivo. Ele importará o Flask e instanciará um objeto Flask. Você pode usar isto para definir as funções que devem ser executadas quando uma rota específica for solicitada:

```
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
```

Isso define basicamente qual conteúdo apresentar quando o domínio raiz for acessado. Salve e feche o arquivo quando você terminar.

Se você seguiu o guia de configuração inicial do servidor, você deverá ter um firewall UFW ativado. Para testar o aplicativo, você precisa permitir o acesso à porta ```5000```:

```
$ sudo ufw allow 5000
```

Agora, você pode testar seu app Flask digitando:

```
$ python myproject.py
```

Você verá um resultado como o seguinte, incluindo um aviso útil lembrando você para não usar essa configuração do servidor na produção:

```
Output
* Serving Flask app "myproject" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

Visite o endereço IP do seu servidor seguido de :5000 no seu navegador Web:

```
http://your_server_ip:5000
```

Você deve ver algo como isto: (Lembrando que se voce ja copiou seu projeto inteiro do github, vera a landing page do seu projeto)

```
<h1>Hello There!</h1>
```

Quando terminar, tecle CTRL-C na janela do seu terminal para parar o servidor de desenvolvimento Flask.

---

### Criando o ponto de entrada da WSGI

Em seguida, vamos criar um arquivo que servirá como o ponto de entrada para nosso aplicativo. Isso dirá ao nosso servidor uWSGI como interagir com ele.

Vamos chamar o arquivo de ```wsgi.py```:

```
$ vi ~/myproject/wsgi.py
```

Neste arquivo, vamos importar a instância Flask do nosso aplicativo e então executá-lo:

```
from myproject import app

if __name__ == "__main__":
    app.run()
```

Salve e feche o arquivo quando você terminar.

---

## Passo 4 — Configurando a uWSGI
Seu aplicativo agora está gravado com um ponto de entrada estabelecido. Podemos agora seguir em frente para configurar a uWSGI.

### Testando o atendimento à uWSGI
Vamos testar para ter certeza de que a uWSGI pode atender nosso aplicativo.

Podemos fazer isso simplesmente passando-lhe o nome do nosso ponto de entrada. Criamos esse ponto de entrada através do nome do módulo (menos a extensão .py) mais o nome do objeto callable dentro do aplicativo. No nosso caso, trata-se do ```wsgi:app```.

Vamos também especificar o soquete, de modo que ele seja iniciado em uma interface disponível publicamente, bem como o protocolo, para que ele use o HTTP em vez do protocolo binário ```uwsgi```. Vamos usar o mesmo número de porta, ```5000```, que abrimos mais cedo:

```
$ uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app
```

Visite o endereço IP do seu servidor com :5000 anexo ao final no seu navegador Web novamente:

```
http://your_server_ip:5000
```

Você deve ver o resultado do seu aplicativo novamente: (Ou a landing page do seu app que foi clonado)

```
<h1>Hello There</h1>
```

Quando você tiver confirmado que ele está funcionando corretamente, pressione CTRL-C na janela do seu terminal.

Acabamos agora o nosso ambiente virtual, para que possamos desativá-lo:

```
$ deactivate
```

Agora, qualquer comando Python voltará a usar o ambiente do sistema Python.

### Criando um arquivo de configuração da uWSGI
Você testou e viu que a uWSGI pode atender o seu aplicativo. Porém, em última instância, você irá querer algo mais robusto para o uso a longo prazo. Você pode criar um arquivo de configuração da uWSGI com as opções relevantes para isso.

Vamos colocar aquele arquivo no diretório do nosso projeto e chamá-lo de ```myproject.ini```:

```
$ vi ~/myproject/myproject.ini

or

$ vi ~/flask_blog/application.ini
```

Dentro, vamos começar com o cabeçalho ```[uwsgi]```, para que a uWSGI saiba aplicar as configurações. Vamos especificar duas coisas: o módulo propriamente dito, recorrendo ao arquivo ```wsgi.py``` (menos a extensão) e ao objeto callable dentro do arquivo, ```app```:

```
[uwsgi]
module = wsgi:app
```

Em seguida, vamos dizer à uWSGI para iniciar em modo mestre e gerar cinco processos de trabalho para atender a pedidos reais:

```
[uwsgi]
module = wsgi:app

master = true
processes = 5

```

Quando você estava testando, você expôs a uWSGI em uma porta da rede. No entanto, você usará o Nginx para lidar com conexões reais do cliente, as quais então passarão as solicitações para a uWSGI. Uma vez que esses componentes estão operando no mesmo computador,é preferífel usar um soquete Unix porque ele é mais rápido e mais seguro. Vamos chamar o soquete de ```application<^>.sock``` e colocá-lo neste diretório.

Vamos alterar também as permissões no soquete. Mais tarde, iremos atribuir a propriedade do grupo Nginx sobre o processo da uWSGI. Dessa forma, precisamos assegurar que o proprietário do grupo do soquete consiga ler as informações que estão nele e gravar nele. Quando o processo parar, também limparemos o soquete, adicionando a opção ```vacuum```:

```
[uwsgi]
module = wsgi:app

master = true
processes = 5

socket = application.sock
chmod-socket = 660
vacuum = true

```

A última coisa que vamos fazer é definir a opção ```die-on-term```. Isso pode ajudar a garantir que o sistema init e a uWSGI tenham as mesmas suposições sobre o que cada sinal de processo significa. Configurar isso alinha os dois componentes do sistema, implementando o comportamento esperado:

```
[uwsgi]
module = wsgi:app

master = true
processes = 5

socket = application.sock
chmod-socket = 660
vacuum = true

die-on-term = true
```

Você pode ter notado que não especificamos um protocolo como fizemos a partir da linha de comando. Isso acontece porque, por padrão, a uWSGI fala usando o protocolo uwsgi, um protocolo binário rápido projetado para se comunicar com outros servidores. O Nginx pode falar este protocolo de maneira nativa, então é melhor usar isso do que forçar a comunicação pelo HTTP.

Quando você terminar, salve e feche o arquivo.

---

## Passo 5 — Criando um arquivo de unidade systemd

Em seguida, vamos criar o arquivo de unidade systemd. Criar um arquivo de unidade systemd permitirá que o sistema init do Ubuntu inicie automaticamente a uWSGI e atenda o aplicativo Flask sempre que o servidor for reinicializado.

Para começar, crie um arquivo de unidade que termine com .service dentro do diretório ```/etc/systemd/system```:

```
$ sudo vi /etc/systemd/system/application.service
```

Ali, vamos começar com a seção ```[Unit]```, que é usada para especificar os metadados e dependências. Vamos colocar uma descrição do nosso serviço aqui e dizer ao sistema init para iniciar isso somente após o objetivo da rede ter sido alcançado:

```
[Unit]
Description=uWSGI instance to serve application
After=network.target
```

Em seguida, vamos abrir a seção ```[Service]```. Isso especificará o usuário e o grupo sob o qual que queremos que o processo seja executado. Vamos dar à nossa conta de usuário regular a propriedade sobre o processo, uma vez que ela possui todos os arquivos relevantes. Vamos também dar propriedade sobre o grupo ao grupo ```www-data``` para que o Nginx possa se comunicar facilmente com os processos da uWSGI. Lembre-se de substituir esse nome de usuário pelo seu nome de usuário:

```
[Unit]
Description=uWSGI instance to serve application
After=network.target

[Service]
User=wesley
Group=www-data
```

Em seguida, vamos mapear o diretório de trabalho e definir a variável de ambiente PATH para que o sistema init saiba que os executáveis do processo estão localizados dentro do nosso ambiente virtual. Vamos também especificar o comando para iniciar o serviço. O systemd exige que seja dado o caminho completo para o executável uWSGI, que está instalado dentro do nosso ambiente virtual. Vamos passar o nome do arquivo de configuração ```.ini``` que criamos no nosso diretório de projeto.

Lembre-se de substituir o nome de usuário e os caminhos do projeto por seus próprios dados:

```
[Unit]
Description=uWSGI instance to serve application
After=network.target

[Service]
User=wesley
Group=www-data
WorkingDirectory=/home/wesley/flask_blog
Environment="PATH=/home/wesley/flask_blog/venv/bin"
ExecStart=/home/wesley/flask_blog/venv/bin/uwsgi --ini application.ini
```

Finalmente, vamos adicionar uma seção ```[Install]```. Isso dirá ao systemd ao que vincular este serviço se nós o habilitarmos para iniciar na inicialização. Queremos que este serviço comece quando o sistema regular de vários usuários estiver funcionando:

```
[Unit]
Description=uWSGI instance to serve application
After=network.target

[Service]
User=wesley
Group=www-data
WorkingDirectory=/home/wesley/flask_blog
Environment="PATH=/home/wesley/flask_blog/venv/bin"
ExecStart=/home/wesley/flask_blog/venv/bin/uwsgi --ini application.ini

[Install]
WantedBy=multi-user.target
```

Com isso, nosso arquivo de serviço systemd está completo. Salve e feche-o agora.

Podemos agora iniciar o serviço uWSGI que criamos e habilitá-lo para que ele seja iniciado na inicialização:

```
$ sudo systemctl start application
$ sudo systemctl enable application
```

Vamos verificar o status:

```
sudo systemctl status application
```

Você deve ver um resultado como este:

```
Output
● myproject.service - uWSGI instance to serve myproject
   Loaded: loaded (/etc/systemd/system/myproject.service; enabled; vendor preset: enabled)
   Active: active (running) since Fri 2018-07-13 14:28:39 UTC; 46s ago
 Main PID: 30360 (uwsgi)
    Tasks: 6 (limit: 1153)
   CGroup: /system.slice/myproject.service
           ├─30360 /home/sammy/myproject/myprojectenv/bin/uwsgi --ini myproject.ini
           ├─30378 /home/sammy/myproject/myprojectenv/bin/uwsgi --ini myproject.ini
           ├─30379 /home/sammy/myproject/myprojectenv/bin/uwsgi --ini myproject.ini
           ├─30380 /home/sammy/myproject/myprojectenv/bin/uwsgi --ini myproject.ini
           ├─30381 /home/sammy/myproject/myprojectenv/bin/uwsgi --ini myproject.ini
           └─30382 /home/sammy/myproject/myprojectenv/bin/uwsgi --ini myproject.ini
```

Se encontrar erros, certifique-se de resolvê-los antes de continuar com o tutorial.

---

## Passo 6 — Configurando o Nginx para solicitações de proxy
Nosso servidor do aplicativo uWSGI agora deverá estar funcionando, esperando pedidos no arquivo do soquete, no diretório do projeto. Vamos configurar o Nginx para passar pedidos da Web àquele soquete, usando o protocolo ```uwsgi```.

Comece criando um novo arquivo de configuração do bloco do servidor no diretório ```sites-available``` do Nginx. Vamos chamá-lo de ```application``` para mantê-lo alinhado com o resto do guia:

```
sudo vi /etc/nginx/sites-available/application
```

Abra um bloco de servidor e diga ao Nginx para escutar na porta padrão ```80```. Vamos também dizer a ele para usar este bloco para pedidos para o nome de domínio do nosso servidor:

```
server {
    listen 80;
    server_name wesleybortolozo www.wesleybortolozo;
}
```

Em seguida, vamos adicionar um bloco de localização que corresponda a cada pedido. Dentro deste bloco, vamos incluir o arquivo ```uwsgi_params```, que especifica alguns parâmetros gerais da uWSGI que precisam ser configurados. Vamos então passar os pedidos para o soquete que definimos usando a diretiva ```uwsgi_pass```:

```
server {
    listen 80;
    server_name wesleybortolozo.com www.wesleybortolozo.com;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/home/wesley/flask_blog/application.sock;
    }
}
```

Salve e feche o arquivo quando você terminar.

Para habilitar a configuração do bloco do servidor Nginx que você acabou de criar, vincule o arquivo ao diretório ```sites-enabled```:

```
$ sudo ln -s /etc/nginx/sites-available/application /etc/nginx/sites-enabled
```

Com o arquivo naquele diretório, podemos realizar testes à procura de erros de sintaxe, digitando:

```
$ sudo nginx -t
```

Se esse procedimento retornar sem indicar problemas, reinicie o processo do Nginx para ler a nova configuração:

```
$ sudo systemctl restart nginx
```

Finalmente, vamos ajustar o firewall novamente. Já não precisamos de acesso através da porta ```5000```, então podemos remover essa regra. Podemos então conceder acesso total ao servidor Nginx:

```
$ sudo ufw delete allow 5000
$ sudo ufw allow 'Nginx Full'
```

Agora, você consegue navegar até o nome de domínio do seu servidor no seu navegador Web:

```
http://your_domain
```

---

## Passo 7 — Protegendo o aplicativo
Para garantir que o tráfego para seu servidor permaneça protegido, vamos obter um certificado SSL para seu domínio. Há várias maneiras de fazer isso, incluindo a obtenção de um certificado gratuito do Let’s Encrypt, gerando um certificado autoassinado ou comprando algum de outro provedor e configurando o Nginx para usá-lo, seguindo os Passos 2 a 6 de Como criar um certificado SSL autoassinado para o Nginx no Ubuntu 18.04. Vamos escolher a opção um por questão de conveniência.