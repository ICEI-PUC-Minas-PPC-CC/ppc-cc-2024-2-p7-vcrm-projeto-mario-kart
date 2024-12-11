# Controle de Corrida por Gestos - Mario Kart

Vídeo do projeto: https://youtu.be/82MyaIUXg78

## Descrição do Projeto
Este projeto implementa um sistema de controle por gestos para o jogo Mario Kart no PC (disponível através do link [mario Kart PC](https://mkpc.malahieude.net/mariokart.php)), proporcionando uma experiência de jogo mais imersiva e intuitiva. Utilizando as bibliotecas OpenCV e MediaPipe, o sistema captura movimentos das mãos e da cabeça do jogador em tempo real, mapeando-os para ações específicas no jogo, como dirigir, acelerar, frear ou usar itens.

## Funcionalidades Principais
- Movimentação Direcional: Movimente as mãos horizontalmente para virar o carro.
- Aceleração: Estenda os dedos da mão para ativar o acelerador.
- Frenagem e Uso de Itens: Controle a frenagem inclinando a cabeça para baixo e o uso de itens rotacionando a cabeça.
  
## Tecnologias Utilizadas
- *Python*: Linguagem de programação principal do projeto.
- *OpenCV*: Biblioteca de visão computacional para processamento de vídeo em tempo real.
- *MediaPipe*: Framework para rastreamento e detecção de mãos e rosto.
- *Pynput*: Biblioteca para emular entradas do teclado.

## Como Instalar e Executar

### Pré-requisitos
- Python 3.8+ instalado.
  
### Pacotes necessários (instaláveis com pip):
- *opencv-python*
- *mediapipe*
- *numpy*
- *pynput*
  
### Passo a Passo
- Clone ou baixe este repositório.
- Instale os pacotes necessários:
      pip install -r requirements.txt
- Certifique-se de que o arquivo config.json está configurado corretamente com os mapeamentos das teclas de ação.
- Execute o programa:
      python main.py
- Certifique-se de que sua câmera está conectada, pois o programa usará o vídeo em tempo real como entrada.
  
## Estrutura do Projeto
- *main.py*: Código principal que processa os gestos e envia comandos para o jogo.
- *config.json*: Arquivo de configuração com o mapeamento das teclas do teclado.
- *requirements.txt*: Lista de dependências do projeto.
- *Documentação de Referência*: Detalhes da proposta e inspiração estão em Proposta Visão Computacional.pdf.

## Código-Fonte Principal
O script principal (main.py) realiza as seguintes funções:
- Captura de Vídeo: Usa a câmera para capturar imagens em tempo real.
- Detecção de Gestos:
    Mãos: Determinação de direção e aceleração.
    Cabeça: Controle de freio e itens.
- Mapeamento de Gestos para Comandos: Traduz os gestos detectados para ações no teclado.
- Renderização Visual: Exibe a imagem processada com as marcações das mãos e rosto.

## Como o Controle Funciona
- Direção: O ângulo entre as duas mãos determina se o carro deve virar à esquerda ou à direita.
- Aceleração: Todos os dedos da mão estendidos ativam o acelerador.
- Freio e Itens:
    Inclinar a cabeça para baixo pressiona o freio.
    Rotação lateral da cabeça ativa o uso de itens.
- Configuração: arquivo config.json foi projetado para permitir a configuração do mapeamento de teclas, possibilitando a adaptação do sistema para outros jogos. Basta alterar os valores de acordo com as teclas e comandos desejados no jogo alvo.

## Referências e Links Úteis
Jogo Base: Mario Kart PC https://mkpc.malahieude.net/mariokart.php

- Luís Guilherme Gomes Ferreira Rossi
- Luiz Pedro Marques Filho
  
## Orientador:
- Will Machado
  
Pontifícia Universidade Católica de Minas Gerais
Curso de Ciência da Computação
