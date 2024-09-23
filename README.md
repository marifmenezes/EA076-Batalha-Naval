# EA076-Batalha-Naval

## Descrição

O jogo de Batalha Naval é um clássico jogo de estratégia para dois jogadores, onde cada jogador tenta afundar a frota de navios do adversário, adivinhando as posições no tabuleiro onde estão localizados os navios.

## Detalhamento do jogo
O objetivo da Batalha Naval é ser o primeiro jogador a afundar todos os navios do oponente. Os jogadores se alternam tentando adivinhar as coordenadas no tabuleiro do adversário onde os navios estão posicionados. Se acertar a posição de um navio, a jogada é considerada um "acerto" e, se não, é um "erro".

O tabuleiro de cada jogador é uma grade de 5x5 e cada jogador irá jogar da sua própria BitDogLab, de forma que elas irão conversar entre si. Para os navios teremos:
 	- Um navio de 3 células.
 	- Dois navios de 2 células.
 	- Dois navios de 1 célula.
Os navios são colocados horizontalmente ou verticalmente, sem sobreposição. Antes de começar a jogar, cada jogador posiciona seus navios em seu tabuleiro, as células serão marcadas de branco. E quando terminar, irá aparecer seus navios no OLED.

Os jogadores se alternam para "atacar" uma posição no tabuleiro do adversário. Quando o jogador acertar o barco, a sua célula ficará vermelha e no oponente aparecerá um X na célula do navio no OLED. Se errar, ficará azul, pois caiu na água. O jogo termina quando um jogador afunda todos os navios do adversário. Esse jogador é o vencedor.
