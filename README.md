<h1 align="center"> :white_check_mark: Checklist de Gerenciamento de Supermercado :shopping_cart: </h1>

<p align="center">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue" />
  <img src="https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white" />
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" />
  <img src="https://img.shields.io/badge/Sqlite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" />
</p>

## :brain: Visão do Projeto 

O projeto tem como propósito desenvolver um dashboard interativo utilizando a biblioteca Streamlit, voltado para o preenchimento diário de checklists operacionais em ambientes de supermercado. A aplicação foi pensada para atender a diferentes perfis de usuários, como Repositores e Gerentes de Loja, oferecendo para cada um uma interface personalizada com campos específicos. O objetivo central é digitalizar e simplificar tarefas de rotina, como verificação de estoque, conferência de escalas, inspeção de limpeza e registro de evidências visuais por meio de upload de imagens.

A solução foi planejada em duas etapas integradas. A primeira etapa envolveu a construção da interface funcional com foco na usabilidade, utilizando checkboxes, comentários opcionais e botões para salvar os dados localmente em formato JSON. Também foram implementadas funcionalidades como a exibição de data e hora, e uma aba dedicada à visualização de checklists anteriores. A segunda etapa consistiu na integração com banco de dados relacional, utilizando SQLAlchemy para criar um banco de dados local, com estrutura pronta para migração futura. Essa fase permitiu a centralização dos dados, além da organização dos arquivos enviados em diretórios apropriados. O projeto busca aliar praticidade, organização e escalabilidade, servindo como base para futuras melhorias voltadas à automação da gestão de supermercados.

## :clipboard: Instruções de Uso

### :calling: Pré-Requisitos

* Python
* Pandas
* SQLAlchemy

### :package: Instalação

1. Clone o Repositório:

    ```bash
    git clone https://github.com/AliceSBulhoes/checklist-supermercado.git
    ```

2. Entre no diretório do projeto:

    ```bash
    cd checklist-supermercado
    ```

3. Instale as dependências do projeto:

    ```bash
    pip install -r requirements.txt
    ```

4. Execute o projeto:

    ```bash
    streamlit run app.py
    ```

## :hammer_and_wrench: Funcionalidades

* Login simples por nome e cargo (sem senha)
* Perfis com visualizações distintas (Repositor e Gerente)
* Checklist diário com:
  * ✅ Checkbox de confirmação
  * 💬 Comentário opcional
  * 📷 Upload de imagem (JPG ou PNG)
* Página para visualizar checklists anteriores
* Interface estilizada e intuitiva
* Integração com banco de dados local 

## :crystal_ball: Melhorias para o Futuro

* Autenticação com login e senha
* Conexão de banco de dados não local
* Dashboard administrativo com gráficos e métricas
* Guardar imagem diretamente no banco de dados

## :bust_in_silhouette: Créditos

Projeto desenvolvido por [Alice Santos Bulhões](https://github.com/AliceSBulhoes) como solução prática e escalável para a rotina de operações de supermercado.











