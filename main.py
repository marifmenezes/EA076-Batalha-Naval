from machine import Pin, SoftI2C, UART, ADC
import neopixel
from ssd1306 import SSD1306_I2C
import time

# Configuração do UART (Tx: GPIO0, Rx: GPIO1)
uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))

# Configuração do OLED
i2c = SoftI2C(scl=Pin(15), sda=Pin(14))
oled = SSD1306_I2C(128, 64, i2c)

# Configuração da Matriz de LEDs
NUM_LEDS = 25
np = neopixel.NeoPixel(Pin(7), NUM_LEDS)

# Definindo a matriz de LEDs (5x5)
LED_MATRIX = [
    [24, 23, 22, 21, 20],
    [15, 16, 17, 18, 19],
    [14, 13, 12, 11, 10],
    [5, 6, 7, 8, 9],
    [4, 3, 2, 1, 0]
]

# Configuração dos botões e joystick
button_A = Pin(5, Pin.IN, Pin.PULL_UP)
button_B = Pin(6, Pin.IN, Pin.PULL_UP)
joystick_x = ADC(Pin(27))
joystick_y = ADC(Pin(26))

# Variáveis de controle
current_x, current_y = 2, 2  # Posição inicial do cursor
game_phase = 'placement'  # Fase inicial é de posicionamento
placement_done_local = False  # Verifica se o jogador local terminou de posicionar
placement_done_remote = False  # Verifica se o jogador remoto terminou de posicionar
turno = 'local'  # Controla de quem é a vez de jogar

# Matrizes de controle
my_ships = [[0 for _ in range(5)] for _ in range(5)]  # Barcos do jogador local
opponent_hits = [[0 for _ in range(5)] for _ in range(5)]  # Acertos do oponente no jogador local
my_hits = [[0 for _ in range(5)] for _ in range(5)]  # Acertos no oponente
misses = [[0 for _ in range(5)] for _ in range(5)]  # Erros do jogador (acertos no mar)

# Tamanhos dos navios
ship_sizes = [3, 2, 2, 1, 1]
current_ship = 0
placed_ships = []
game_over = False  # Variável que indica se o jogo acabou

# Funções de comunicação UART

def send_command(command):
    """Envia um comando via UART para o oponente."""
    uart.write(command + '\n')
    print(f"Comando enviado: {command}")  # Debug para verificar comandos enviados

def receive_command():
    """Recebe um comando via UART com tratamento seguro."""
    try:
        if uart.any():
            command = uart.read().decode('utf-8').strip()  # Tenta decodificar o comando
            print(f"Comando recebido: {command}")  # Debug para verificar comandos recebidos
            return command
    except UnicodeError:
        print("Erro de decodificação, ignorando dados inválidos.")  # Trata erros de decodificação
    return None  # Retorna None se não houver um comando válido

# Funções de Desenho

def draw_oled():
    """Desenha os navios do jogador no OLED e os ataques do oponente."""
    oled.fill(0)
    for y in range(5):
        for x in range(5):
            if my_ships[y][x]:  # Desenha o navio
                oled.fill_rect(x * 24, y * 12, 24, 12, 1)
            if opponent_hits[y][x]:  # Se foi atingido, desenha um "X"
                oled.text('X', x * 24 + 8, y * 12 + 2)
    oled.show()

def clear_led_matrix():
    """Apaga todos os LEDs da matriz."""
    for i in range(NUM_LEDS):
        np[i] = (0, 0, 0)
    np.write()

def draw_led_matrix_for_placement():
    """Desenha os navios durante a fase de posicionamento e o cursor branco."""
    for y in range(5):
        for x in range(5):
            led_index = LED_MATRIX[y][x]
            if my_ships[y][x]:  # Barco posicionado
                np[led_index] = (0, 50, 0)  # LED verde suave para navio
            elif (x, y) == (current_x, current_y):
                np[led_index] = (50, 50, 50)  # LED branco suave para o cursor de seleção
            else:
                np[led_index] = (0, 0, 0)  # Apaga os outros LEDs
    np.write()

def draw_led_matrix_for_attack():
    """Mostra o ataque na matriz de LEDs, indicando acertos ou erros."""
    for y in range(5):
        for x in range(5):
            led_index = LED_MATRIX[y][x]
            if my_hits[y][x]:  # Ataque bem-sucedido
                np[led_index] = (50, 0, 0)  # LED vermelho suave para acerto
            elif misses[y][x]:  # Jogada errada (acertou o mar)
                np[led_index] = (0, 0, 50)  # LED azul suave para erro
            elif (x, y) == (current_x, current_y):
                np[led_index] = (50, 50, 50)  # LED branco suave para cursor
            else:
                np[led_index] = (0, 0, 0)  # LED apagado
    np.write()

# Funções do Joystick com ajustes de sensibilidade

def read_joystick():
    """Leitura do Joystick e atualização das coordenadas com controle de sensibilidade."""
    global current_x, current_y
    x_value = joystick_x.read_u16()
    y_value = joystick_y.read_u16()

    deadzone = 20000  # Definindo a zona morta para evitar movimentações indesejadas

    if x_value < (32768 - deadzone):  # Movimento para a esquerda
        current_x = max(0, current_x - 1)
        time.sleep(0.3)  # Pequeno intervalo para desacelerar o movimento
    elif x_value > (32768 + deadzone):  # Movimento para a direita
        current_x = min(4, current_x + 1)
        time.sleep(0.3)

    if y_value < (32768 - deadzone):  # Movimento para cima
        current_y = max(0, current_y - 1)
        time.sleep(0.3)
    elif y_value > (32768 + deadzone):  # Movimento para baixo
        current_y = min(4, current_y + 1)
        time.sleep(0.3)

# Função de posicionamento de navio
def place_ship():
    """Coloca o navio na posição atual e acende o LED correspondente."""
    global current_ship, placed_ships, placement_done_local
    if my_ships[current_y][current_x] == 0:  # Se a célula estiver vazia
        my_ships[current_y][current_x] = 1  # Posiciona o barco
        np[LED_MATRIX[current_y][current_x]] = (0, 50, 0)  # Acende o LED verde suave para o barco
        np.write()
        placed_ships.append((current_x, current_y))
        if len(placed_ships) == ship_sizes[current_ship]:
            current_ship += 1
            placed_ships.clear()
            if current_ship == len(ship_sizes):  # Se todos os navios foram colocados
                placement_done_local = True
                send_command('placement_done')  # Informa o oponente que o posicionamento foi concluído
                print("Posicionamento completo! Barcos serão desenhados no OLED.")
                draw_oled()  # Desenha os barcos no OLED
                return True
    return False

# Função de ataque
def attack():
    """Envia as coordenadas de ataque ao oponente."""
    send_command(f'attack:{current_x},{current_y}')  # Envia o ataque ao oponente

# Função para verificar se o jogador venceu
def check_victory():
    """Verifica se o jogador atingiu todas as posições dos navios do oponente."""
    for y in range(5):
        for x in range(5):
            if my_ships[y][x] == 1:  # Ainda há navios restantes
                return False
    return True  # Todos os navios do oponente foram destruídos

# Função para exibir "Vitória" no OLED
def show_victory():
    """Exibe a mensagem de vitória no OLED."""
    oled.fill(0)
    oled.text("Vitoria!", 20, 30)  # Exibe "Vitória" no OLED do vencedor
    oled.show()

# Função para processar comandos recebidos via UART
def process_command(command):
    global game_phase, placement_done_remote, game_over, turno
    if command is None:  # Se o comando for None, ignora
        return

    if command.startswith('attack:'):
        # Extrai as coordenadas de ataque
        _, coords = command.split(':')
        x, y = map(int, coords.split(','))
        if my_ships[y][x] == 1:  # Se foi atingido
            my_ships[y][x] = 0  # Marca o barco como destruído
            opponent_hits[y][x] = 1
            send_command('hit')
            draw_oled()  # Atualiza o OLED para mostrar o "X" no barco atingido
            if check_victory():  # Verifica se o oponente venceu
                send_command('victory')  # Informa que o oponente venceu
                oled.fill(0)
                oled.text("Game Over", 20, 30)  # Exibe "Game Over" no OLED do perdedor
                oled.show()
                game_over = True
        else:
            send_command('miss')
        turno = 'local'  # Passa o turno para o jogador local

    elif command == 'hit':
        my_hits[current_y][current_x] = 1  # Marca o hit na matriz
        print("Você acertou o navio do oponente!")
        draw_led_matrix_for_attack()  # Mostra o acerto na matriz de LEDs
        time.sleep(1)
        clear_led_matrix()  # Apaga a matriz após o ataque
        if check_victory():  # Verifica se o jogador venceu
            show_victory()  # Exibe a mensagem de vitória
            game_over = True
        turno = 'remote'  # Passa o turno para o oponente

    elif command == 'miss':
        print("Você errou o navio do oponente!")
        misses[current_y][current_x] = 1  # Marca o erro na matriz (acerto no mar)
        draw_led_matrix_for_attack()  # Mostra o erro na matriz de LEDs
        time.sleep(1)
        clear_led_matrix()  # Apaga a matriz após o ataque
        turno = 'remote'  # Passa o turno para o oponente

    elif command == 'placement_done':
        placement_done_remote = True  # O oponente terminou o posicionamento
        print("Oponente terminou o posicionamento.")

    elif command == 'victory':  # O oponente venceu
        oled.fill(0)
        oled.text("Game Over", 20, 30)  # Exibe "Game Over" no OLED do perdedor
        oled.show()
        game_over = True

# Função para verificar se ambos os jogadores completaram o posicionamento
def check_both_placements_done():
    global game_phase
    if placement_done_local and placement_done_remote:
        print("Ambos os jogadores completaram o posicionamento. Fase de ataque.")
        game_phase = 'attack'

# Loop Principal
while True:
    if game_over:
        break  # Encerra o loop quando o jogo termina

    read_joystick()

    if game_phase == 'placement':
        draw_led_matrix_for_placement()  # Desenha os navios e o cursor branco suave
        if not placement_done_local:
            if not button_A.value():  # Se o botão A for pressionado
                if place_ship():
                    print("Todos os navios foram posicionados.")
                    time.sleep(0.5)
        # Verificar se o comando de 'placement_done' foi recebido
        command = receive_command()
        if command:
            process_command(command)
        # Verificar se ambos os jogadores terminaram de posicionar
        check_both_placements_done()

    elif game_phase == 'attack':
        if turno == 'local':  # Verifica se é a vez do jogador local
            draw_led_matrix_for_attack()
            if not button_A.value():  # Se o botão A for pressionado
                attack()  # Ataca o oponente
                time.sleep(0.5)

        command = receive_command()  # Recebe o comando do oponente
        if command:
            process_command(command)

    time.sleep(0.1)  # Pequena pausa para economizar processamento

