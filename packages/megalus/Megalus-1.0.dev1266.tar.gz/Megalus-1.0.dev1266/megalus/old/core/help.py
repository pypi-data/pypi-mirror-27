from textwrap import dedent
from megalus.core.utils import console
INICIAL = """
Este help mostra os comandos da ferramenta MEG-Tools.
Para apenas visualizar os comandos e suas opções, digite 'meg'.
Para ver a Ajuda de todos os comandos, digite 'meg help'.
Para ver a Ajuda de um comando específico digite 'meg help <comando>'.
"""

HELP_COMMANDS = [{'command': 'config',
                  'options': 'meg config [--clone-only]',
                  'description': '''
                  Use para configurar o ambiente de desenvolvimento local.
                  Use a opção `--clone-only` para clonar/baixar apenas
                  ''',
                  'examples': None,
                  'long_desc': None},
                 {'command': 'deploy',
                  'options': 'meg deploy',
                  'description': '''
                  Use para fazer o deploy de um ambiente local na Amazon.
                  É preciso rodar este comando na pasta-raiz de um dos repositorios
                  clonados pelo comando `meg config`
                  ''',
                  'examples': None,
                  'long_desc': None},
                 {'command': 'telnet',
                  'options': 'meg telnet <app> <port>',
                  'description': '''
                  Use para abrir a aplicação informada num TTY
                  que faz um telnet dentro do Docker no endereco 127.0.0.1
                  e a porta especificada.
                  Se não informar a aplicação a ferramenta irá perguntar
                  qual aplicação abrir, a partir dos containers em atividade.
                  Equivale ao comando "docker exec -ti _container_ telnet 127.0.0.1 _porta_"
                  ''',
                  'examples': 'meg telnet worker 6908',
                  'long_desc': None},
                 {'command': 'test',
                  'options': 'meg test [<app>] [--using=(django|nose|pytest)] [--rds] [-v]',
                  'description': '''
                  Use para rodar os testes unitários da aplicação.
                  Para usar este comandos as livrarias coverage, pydocstyle e pycodestyle devem
                  estar instaladas no container.
                  A ferramenta permite o uso das livrarias de teste:
                  - Django (pelo comando manage.py teste)
                  - Nose
                  - Pytest
                  Para isto basta informar qual utilizar com a opção "--using", em minúsculas. Estas
                  devem ser instaladas no container ou a ferramenta vai escolher a livraria
                  que estiver disponível.
                  Se nenhuma livraria estiver instalada no container ou nenhuma for selecionada,
                  será usado o Unittest padrão do Python.
                  Utilize as opções abaixo para configurar os testes:
                  * --using: Use uma das opções a seguir: nose, pytest, django
                  * --rds: Use o banco de dados na Amazon (utilizado pelo ambiente de Staging)
                    ao invés do banco de dados local, para rodar os testes
                  * -v use a opcao "verbose" para mostrar mais detalhes dos testes
                  ''',
                  'examples': '''
                  meg test painel (abre o Painel rodando a lib padrao e banco de dados local)
                  meg test site --using=django (abre o Site rodando django e banco de dados local)
                  ''',
                  'long_desc': None},
                 {'command': 'bash',
                  'options': 'meg bash <app>',
                  'description': '''
                  Use para abrir a aplicação informada num terminal bash (usuario root).
                  Se não informar a aplicação a ferramenta irá perguntar qual aplicação abrir,
                  a partir dos containers em atividade.

                  Equivale ao comando "docker exec -ti _container_ /bin/bash"
                  ''',
                  'examples': 'meg bash carrinho',
                  'long_desc': None},
                 {'command': 'run',
                  'options': 'meg run <app>',
                  'description': '''
                  Roda a aplicação informada e suas dependências ou todas as aplicações/containers
                  se não informar nenhuma aplicação.

                  Equivale ao comando "docker-compose stop && docker-compose up _aplicacao_"
                  ''',
                  'examples': '''
                  meg run (roda todos os containers)
                  meg run painel (roda o container do Painel e os containers dependentes
                  ''',
                  'long_desc': None},
                 {'command': 'build',
                  'options': 'meg build <app> [--no-cache]',
                  'description': '''
                  Use para fazer a build do container da aplicação selecionada.
                  Para atualizar somente a imagem base do Docker, use o comando 'meg build base'.
                  Se nenhuma aplicação for informada, será feito a build de todos os containers (mais
                  a imagem base). Opções:
                  * --no-cache: Durante a build, forçar o download de todas as livrarias/dependencias
                  Equivale ao comando "docker-compose stop && docker-compose build _aplicacao_"
                  ''',
                  'examples': '''
                  meg build (faz o build de todos os containers)
                  meg build loja (faz a build do container da Loja)
                  ''',
                  'long_desc': None},
                 {'command': 'update',
                  'options': 'meg update [--yes] [--production | --staging]',
                  'description': '''
                  Roda em cada repositório clonado pelo comando `meg config`
                  o comando "git remote update && git fetch && git pull --all",
                  desde que o repositorio esteja na branch prodution, staging,
                  beta, release ou master (repositórios que estejam em outros
                  branchs são ignorados).
                  Em adição ele clona novos repositórios que não estejam na pasta
                  do projeto informado.
                  Use a opção --yes ou -y para confirmar automaticamente as operações.
                  Use a opção --production para fazer o git checkout para a branch
                  mais estável do projeto (exemplo: production, master, etc) antes do update.
                  ''',
                  'examples': '''
                  meg update (atualiza todas as branchs atuais)
                  meg update --production (faz o checkout para a branch mais estável e atualiza)
                  meg update --staging (faz o checkout para staging/beta e atualiza os repositórios
                  ''',
                  'long_desc': None},
                 {'command': 'list',
                  'options': 'meg list [<libs>...]',
                  'description': '''
                  Lista as aplicações existentes no Docker-Compose, e informa as seguintes
                  informações:
                  * O nome da aplicação e se o container está rodando
                  * A branch em que o container está.
                  * As diferenças no branch, em relação ao VCS (commits a frente/atrás, etc...).
                  * A porta que está sendo exposta no container

                  Para listar outras livrarias, digite elas após o comando, separando com espaço.
                  ''',
                  'examples': '''
                  meg list (para a lista padrao)
                  meg list django flask gunicorn (Para listar as versões do Django,
                  Flask e Gunicorn que estão rodando dentro dos containers.)
                  ''',
                  'long_desc': None},
                 {'command': 'rebuild',
                  'options': 'meg rebuild',
                  'description': 'Este comando exclui todas as imagens e containers existentes na máquina.\nEm seguida atualiza os repositórios existentes e baixa os novos.\nApós isso, inicia a build de todos os containers.\nCertifique-se de ter feito um backup do seu banco de dados local, antes de iniciar esse comando.',
                  'examples': None,
                  'long_desc': None},
                 {'command': 'tunnel',
                  'options': 'meg tunnel <subdominio> <aplicacao>',
                  'description': 'Este comando cria um tunel reverso a partir de uma instância amazon (tunnel.awsli.com.br) para uma das aplicações rodando localmente.\nUse quando é necessário informar, em um serviço de terceiros, um endereço http ou https, ao invés de "localhost".\nO ngrok usa o <subdomínio> informado para criar a URL (subdominio.tunnel.awsli.com.br), tanto para http, quanto https e redireciona as chamadas para a porta da <aplicação> informada.\nEquivale ao comando "ngrok --subdomain=<subdominio informado> <porta informada>"',
                  'examples': 'meg tunnel retorno painel (Cria o tunel "http://retorno.tunnel.maisimovel.net" e redireciona as chamadas para a aplicação MaisPainel)\nmeg tunnel ret-facebook site (Cria o túnel "http://ret-facebook.maisimovel.net" e redireciona as requisições para o Site)',
                  'long_desc': None},
                 {'command': 'watch',
                  'options': 'meg watch <aplicacao>',
                  'description': 'Este comando indica ao Webpack para entrar em modo "watch".\nO webopack irá gerar os arquivos estáticos (html, css, png, etc...) para serem lidos pelo Django.\nCaso os arquivos sejam alterados o webpack atualizará automaticamente o arquivo comprimido.',
                  'examples': 'meg watch painel (comprime os arquivos estáticos do Painel)',
                  'long_desc': None},
                 {'command': 'ci',
                  'options': 'meg ci (major|minor|patch)',
                  'description': '''
                  Este comando inicia o Continuous Integration (CI).
                  O comando irá gerar um Pull Request para a branch 'master'
                  da aplicação onde o comando foi chamado.
                  É preciso estar na pasta raiz da aplicação.
                  A branch da aplicação deve ser a branch 'release'
                  O comando irá falhar se existirem modificações no git não commitadas.
                  O comando irá falhar se o último teste no Pipeline for falho.
                  O número da versão irá aumentar de acordo com a opção selecionada:
                  - major: x+1.0.0
                  - minor: 0.x+1.0
                  - patch: 0.0.x+1
                  Se nenhuma opção for selecionada, será usado a última tag criada.
                  ''',
                  'examples': 'meg ci patch (cria Pull Request e aumenta a versão x.x.Y+1)',
                  'long_desc': None},
                 {'command': 'resetdb',
                  'options': 'meg resetdb <application>',
                  'description': '''
                  Este comando irá apagar e recriar o banco de dados local da aplicação selecionada.
                  Certifique-se que qualquer dado importante tenha sido salvo antes de rodar este comando.
                  Após recriar o banco de dados, os comandos do Django, makemigrations, migrate e createdata
                  serão rodados no novo banco.''',
                  'examples': 'meg resetdb painel: recria o banco de dados do Painel',
                  'long_desc': None}]


def get_help(app=None):
    if app:
        command_help = [
            obj
            for obj in HELP_COMMANDS
            if obj.get('command') == app
        ]
        if command_help:
            show_help(command_help, show_long_desc=True)
            return True
        else:
            return True
    else:
        show_help(sorted(HELP_COMMANDS, key=lambda x: x['command']))
        return True


def show_help(help_list, show_long_desc=False):
    if not show_long_desc:
        print(dedent(INICIAL))
    for command in help_list:
        console(
            "Commando: ".format(
                command['command'].upper()),
            style="warning",
            use_prefix=False)
        if command['options']:
            console("Opções:", style="warning", use_prefix=False)
            print(command['options'])
        console("\nResumo:", style="warning", use_prefix=False)
        print(dedent(command['description']))
        if show_long_desc and command['long_desc']:
            print('\n{}'.format(dedent(command['long_desc'])))
        if command['examples']:
            console("\nExemplos:", style="warning", use_prefix=False)
            print(dedent(command['examples']))
