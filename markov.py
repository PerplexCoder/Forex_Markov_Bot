import MetaTrader5 as mt5
from datetime import datetime
import time
import pandas as pd
import logging
import matplotlib.pyplot as plt
from matplotlib import style
import sqlite3

print("Ok")
style.use('fivethirtyeight')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

# Configurações iniciais
logging.basicConfig(filename='markov_trading.log', level=logging.INFO)
logging.info("=======================================")
logging.info(f"Execução iniciada em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
logging.info("=======================================")

if not mt5.initialize():
    logging.error("Falha ao inicializar MT5")
    mt5.shutdown()
    quit()

symbol = "EURUSD"
symbol_info = mt5.symbol_info("EURUSD")

if symbol_info:
    spread = symbol_info.spread
TAKE = spread / 100000
lot_size = 0.01
rsi_period = 14
rsi_upper = 95
rsi_lower = 5
open_positions = {}
bid = mt5.symbol_info_tick(symbol).bid
ask = mt5.symbol_info_tick(symbol).ask
MAX_ORDERS = 10
ORDER_DISTANCE = 200  # Distância em pontos


conn = sqlite3.connect('orders_database.db')
cursor = conn.cursor()


# Cadeia de Markov - matriz de transição inicial
transition_matrix = {
    'Sobrevendido': {'Sobrevendido': 0, 'Neutro': 0, 'Sobrecomprado': 0},
    'Neutro': {'Sobrevendido': 0, 'Neutro': 0, 'Sobrecomprado': 0},
    'Sobrecomprado': {'Sobrevendido': 0, 'Neutro': 0, 'Sobrecomprado': 0}
}


'''
tabela para armazenar as ordens
'''


cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_number INTEGER PRIMARY KEY,
    ticket INTEGER,
    price REAL,
    sl REAL,
    tp REAL,
    markov_state TEXT,
    order_type TEXT,
    closure INTEGER DEFAULT NULL
)
""")
conn.commit()




''' Inicio funções '''


# contar o número de ordens abertas para um determinado tipo de ordem
def count_open_orders(order_type):
    cursor.execute("SELECT COUNT(*) FROM orders WHERE closure IS NULL AND order_type=?", (order_type,))
    count = cursor.fetchone()[0]
    return count


def manage_orders(symbol, order_type):
    """Gerencia ordens com base no tipo de ordem e nas condições especificadas"""

    print("Ok -- manager orders")
    bid = mt5.symbol_info_tick(symbol).bid

    open_buy_orders = count_open_orders('B')
    open_sell_orders = count_open_orders('S')

    if order_type == mt5.ORDER_TYPE_BUY:
        if open_buy_orders >= 1:
            logging.info("Número máximo de ordens de COMPRA atingido.")
            return
        else:
            open_order(symbol, mt5.ORDER_TYPE_BUY, lot_size)

    elif order_type == mt5.ORDER_TYPE_SELL:
        if open_sell_orders >= 1:
            logging.info("Número máximo de ordens de VENDA atingido.")
            return
        else:
            open_order(symbol, mt5.ORDER_TYPE_SELL, lot_size)

    # Pegar todas as ordens abertas do SQLite

    cursor.execute("SELECT ticket, price, order_type, tp FROM orders WHERE closure IS NULL")
    open_orders_from_db = cursor.fetchall()


    for order_db in open_orders_from_db:
        ticket_db, price_db, order_type_db, tp_db = order_db  # Corrigido para desempacotar todos os quatro valores


        # Verificar ordens de compra
        if order_type_db == mt5.ORDER_TYPE_BUY and bid >= tp_db:
            print(f"Ordem de COMPRA {ticket_db} atingiu o TP no preço: {bid}. Atualizando a coluna closure.")
            cursor.execute("UPDATE orders SET closure = 1 WHERE ticket = ?", (ticket_db,))
            conn.commit()

        # Verificar ordens de venda
        elif order_type_db == mt5.ORDER_TYPE_SELL and ask <= tp_db:
            print(f"Ordem de VENDA {ticket_db} atingiu o TP no preço: {ask}. Atualizando a coluna closure.")
            cursor.execute("UPDATE orders SET closure = 1 WHERE ticket = ?", (ticket_db,))
            conn.commit()


'''
Funcao para checar todas as ordens abertas regulamente.
'''
def check_orders_status():
    logging.info("Iniciando verificação de status da ordem...")
    
    # Atualizar os valores de bid2 e ask2
    tick_info = mt5.symbol_info_tick(symbol)
    bid2 = tick_info.bid
    ask2 = tick_info.ask
    logging.info(f"Valores atualizados - Bid2: {bid2}, Ask2: {ask2}")

    # Pegar todas as ordens abertas do SQLite
    cursor.execute("SELECT ticket, price, order_type, tp FROM orders WHERE closure IS NULL")
    open_orders_from_db = cursor.fetchall()

    logging.info(f"Número de ordens abertas a verificar: {len(open_orders_from_db)}")

    for order_db in open_orders_from_db:
        ticket_db, price_db, order_type_db, tp_db = order_db

        logging.info(f"Verificando ordem - Ticket: {ticket_db}, Tipo: {order_type_db}, Bid2: {bid2}, Ask2: {ask2}, TP: {tp_db}")

        # Verificar ordens de compra
        if order_type_db == 'B' and bid2 >= tp_db:
            logging.info(f"Ordem de COMPRA {ticket_db} atingiu o TP no preço: {bid2}. Atualizando a coluna closure.")
            cursor.execute("UPDATE orders SET closure = 1 WHERE ticket = ?", (ticket_db,))
            conn.commit()
        elif order_type_db == 'B':
            logging.info(f"Condição para fechar ordem de COMPRA {ticket_db} não atendida. Bid2: {bid2}, TP: {tp_db}")

        # Verificar ordens de venda
        elif order_type_db == 'S' and bid2 <= tp_db:
            logging.info(f"Ordem de VENDA {ticket_db} atingiu o TP no preço: {ask2}. Atualizando a coluna closure.")
            cursor.execute("UPDATE orders SET closure = 1 WHERE ticket = ?", (ticket_db,))
            conn.commit()
        elif order_type_db == 'S':
            logging.info(f"Condição para fechar ordem de VENDA {ticket_db} não atendida. Bid2: {bid2}, TP: {tp_db}")

    logging.info("Verificação de status da ordem concluída.")



def send_test_order(symbol, lot_size, sl_price_buy, tp_price_buy):
    price = mt5.symbol_info_tick(symbol).bid
    deviation = 20
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot_size,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl": sl_price_buy,
        "tp": tp_price_buy,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
    }
    result = mt5.order_send(request)
    if result.retcode == 0:
        logging.info(f"Ordem de teste enviada com sucesso. Order ID: {result.order}")
    else:
        logging.error(f"Erro ao enviar ordem de teste. Retcode: {result.retcode}")


def calculate_rsi(data, period):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def update_markov_chain(transition_matrix, old_state, new_state):
    print("Ok -- Atualizacao cadeia de markov")
    transition_matrix[old_state][new_state] += 1
    total_transitions = sum(transition_matrix[old_state].values())
    
    for state in transition_matrix[old_state]:
        transition_matrix[old_state][state] /= total_transitions

def get_next_state_probability(transition_matrix, current_state):
    return transition_matrix[current_state]

def determine_market_state(rsi, transition_matrix, current_state):
    rsi_upper_threshold = rsi_upper
    rsi_lower_threshold = rsi_lower
    
    if rsi > rsi_upper_threshold:
        next_state = 'Sobrecomprado'
    elif rsi < rsi_lower_threshold:
        next_state = 'Sobrevendido'
    else:
        next_state = 'Neutro'
    
    update_markov_chain(transition_matrix, current_state, next_state)
    return next_state

def open_order(symbol, order_type, lot_size):
    logging.info(f"Abertura de ordem solicitada: {symbol}, Tipo: {order_type}, Volume: {lot_size}")

    print("Ok - open order")
    # Recupere os valores bid e ask
    tick_info = mt5.symbol_info_tick(symbol)
    bid2 = tick_info.bid
    ask2 = tick_info.ask

    print(bid2)
    print(ask2)

    # Defina o entry_price
    entry_price = ask2 if order_type == mt5.ORDER_TYPE_BUY else bid2

    point = mt5.symbol_info(symbol).point
    deviation = 10
    sl_price_buy = entry_price - 0.00775
    tp_price_buy = entry_price + TAKE + 0.00002
    sl_price_sell = entry_price + 0.00775
    tp_price_sell = entry_price - TAKE - 0.00002


    logging.info(f"Preços definidos. SL Buy: {sl_price_buy}, TP Buy: {tp_price_buy}, SL Sell: {sl_price_sell}, TP Sell: {tp_price_sell}")

    order = {}
    if order_type == mt5.ORDER_TYPE_BUY:
        order = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot_size,
            "type": order_type,
            "price": ask,
            "sl": sl_price_buy,
            "tp": tp_price_buy,
            "deviation": deviation,
            "magic": 123456,
            "comment": "B",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        order_comment = "B"
        logging.info("Ordem de COMPRA configurada.")
    elif order_type == mt5.ORDER_TYPE_SELL:
        order = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot_size,
            "type": order_type,
            "price": bid,
            "sl": sl_price_sell,
            "tp":  tp_price_sell,
            "deviation": deviation,
            "magic": 123456,
            "comment": "S",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        order_comment = "S"
        logging.info("Ordem de VENDA configurada.")


    result = mt5.order_send(order)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        logging.error(f"Erro ao enviar ordem: {result.comment}")
    else:
        logging.info(f"Ordem enviada com sucesso. Ticket: {result.order}, Preço: {result.price}, Volume: {result.volume}")


        # Pegue o número da última ordem
        cursor.execute("SELECT MAX(order_number) FROM orders")
        last_order_number = cursor.fetchone()[0]
        if not last_order_number:
            last_order_number = 0
        new_order_number = last_order_number + 1

        # Adicione a nova ordem ao banco de dados
        cursor.execute("""
        INSERT INTO orders (order_number, ticket, price, sl, tp, markov_state, order_type)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (new_order_number, result.order, result.price, round(order['sl'], 5), round(order['tp'], 5), current_state, order_comment))


        conn.commit()



''' fim funções '''

current_state = 'Neutro'

# Loop principal
while True:

    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, rsi_period + 1)
    df = pd.DataFrame(rates)
    df['close'] = df['close']
    df['rsi'] = calculate_rsi(df['close'], rsi_period)
    last_rsi = df['rsi'].iloc[-1]
    
    logging.info(f"Taxas obtidas para {symbol}. Número de taxas: {len(rates)}")
    
    df = pd.DataFrame(rates)
    df['close'] = df['close']
    logging.info("DataFrame criado e coluna 'close' atualizada.")

    df['rsi'] = calculate_rsi(df['close'], rsi_period)
    logging.info("Coluna RSI calculada para o DataFrame.")
    
    last_rsi = df['rsi'].iloc[-1]
    logging.info(f"Último valor RSI: {last_rsi}")

    current_state = determine_market_state(last_rsi, transition_matrix, current_state)
    logging.info(f"Estado atual determinado como: {current_state}")

    state_probabilities = get_next_state_probability(transition_matrix, current_state)
    logging.info(f"Probabilidades de estado obtidas para o estado atual ({current_state}): {state_probabilities}")
    
    if current_state == 'Sobrecomprado' and state_probabilities['Sobrevendido'] < 0.2:
        manage_orders(symbol, mt5.ORDER_TYPE_BUY)

    elif current_state == 'Sobrevendido' and state_probabilities['Sobrecomprado'] < 0.2:
        manage_orders(symbol, mt5.ORDER_TYPE_SELL)

    # Chame a função check_orders_status a cada iteração do loop
    check_orders_status()

    print("Ok -- main loop")

    time.sleep(2)
