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

## Tutorial do Jogo
### Fases do Jogo
O jogo é dividido em duas fases principais:
Posicionamento dos Navios
Fase de Ataque

### 1. Posicionamento dos Navios
Antes de começar a atacar, cada jogador precisa posicionar seus navios no tabuleiro. Os navios têm os seguintes tamanhos:
- 1 navio de tamanho 3
- 2 navios de tamanho 2
- 2 navios de tamanho 1


#### Como Posicionar os Navios:

Use o Joystick: Movimente o cursor branco pela matriz de LEDs para selecionar a posição do seu navio.

Movimente o joystick para a esquerda/direita para mover o cursor na direção correspondente.

Movimente o joystick para cima/baixo para ajustar a posição vertical do cursor.

Pressione o Botão A: Quando a posição desejada for selecionada, pressione o botão A para colocar parte do navio naquela célula. Um LED verde suave aparecerá indicando que o navio foi colocado.

Complete o Navio: Continue posicionando partes do navio até que todas as células do navio estejam no tabuleiro. Quando o navio estiver completamente posicionado, o jogo automaticamente passará para o próximo navio.

Finalizar Posicionamento: Quando todos os navios forem posicionados, o jogo mudará para a fase de ataque. O jogador local também enviará uma mensagem ao oponente informando que terminou o posicionamento.

#### Nota:

Você verá seus navios no display OLED enquanto os posiciona.

Os LEDs só mostram os navios temporariamente durante o posicionamento.


### 2. Fase de Ataque
Após o posicionamento dos navios, a fase de ataque começa. Durante esta fase, os jogadores se alternam realizando ataques no tabuleiro do oponente.


#### Como Atacar:

Movimente o Cursor: Assim como na fase de posicionamento, use o joystick para mover o cursor branco pela matriz de LEDs.
Pressione o Botão A: Quando tiver selecionado a posição onde deseja atacar, pressione o botão A para confirmar o ataque. O ataque será enviado ao oponente via UART.


#### Receber Feedback:

Se o ataque acertar um navio inimigo, o LED correspondente ficará vermelho suave.
Se o ataque for em uma área sem navio (acertar o mar), o LED ficará azul suave.
Os resultados também serão exibidos no OLED.
Alternância de Turnos: Após seu ataque, será a vez do oponente atacar. Aguarde seu próximo turno.


#### Como Saber se Você Ganhou ou Perdeu

Vitória: Se você acertar todas as posições dos navios do oponente, uma mensagem de "Vitória" será exibida no seu OLED.
Derrota: Se todos os seus navios forem destruídos, "Game Over" aparecerá no seu OLED.


#### Dicas de Jogo

Use o Joystick com cuidado: Movimentar o joystick de maneira brusca pode fazer o cursor se mover mais rápido do que o esperado. Tenha paciência, pois o cursor se move célula por célula.
Estratégia de Posicionamento: Tente espalhar seus navios de maneira estratégica para dificultar que o oponente os acerte.
Preste Atenção ao Feedback Visual: O display OLED e a matriz de LEDs oferecem informações importantes sobre o status do jogo. Use isso a seu favor!

## Perguntas e Respostas sobre o jogo 

### Quantos navios posso posicionar?

Cada player deve selecionar 1 navio de 3 células, 2 navios de 2 células e 2 navios de 1 célula. As células devem ser selecionadas pressionando o botão A após cada posição escolhida .Ao final da seleção, o jogador verá seus navios no OLED e deverá esperar o oponente fazer o posicionamento dos seus navios para que a fase de ataque seja iniciada.


### Como sei que é minha vez de atacar?

Se for seu primeiro ataque, um led irá acender na sua matriz indicando que você deve escolher uma posição para atacar. Caso seja a vez do seu oponente, sua matriz estará completamente apagada e reacenderá após a jogada do oponente. 


### Como sei quais posições já ataquei?

Na sua matriz, a posição que você atacou acertando um navio oponente irá ficar acesa na cor vermelha, já a posição que você errou irá aparecer como azul. Essas posições estarão a mostra na matriz sempre que for sua vez de atacar, para que não haja ataques diferentes em uma mesma posição.  


### Como saber se meu navio foi atacado?
	
 Seus navios estarão posicionados no OLED, quando alguma célula do seus navios for atingida aparecerá um “X” na célula correspondente no OLED.


### Quando o jogo termina? E como jogar novamente?


Quando um dos jogadores ataca corretamente todos os navios oponentes. No OLED do vencedor deverá aparecer “Vitória” e no do perdedor “Game over”. Para dar início0 a um novo jogo basta apertar o botão “Reset” em ambas as placas.


### Como eu “instalo” o jogo?

Você deve ter duas placas BitDogLab e salvar o código presente no github como main nas suas placas. Além disso, deve ter conectado às portas da UART conectadas fisicamente, de modo que o TX de uma esteja conectado ao RX do outro.

