import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from matplotlib.animation import FuncAnimation

DATABASE_PATH = 'orders_database.db'

def plot_price(ax):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    def animate(i):
        cursor.execute("SELECT price FROM orders")
        prices = cursor.fetchall()
        ax.clear()
        ax.plot(prices, label="Price")
        ax.legend()
    
    ani = FuncAnimation(ax.figure, animate, interval=10000, cache_frame_data=False)
    return ani

def markov_heatmap(ax):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    mapping = {'Sobrevendido': 0, 'Neutro': 1, 'Sobrecomprado': 2}
    state_names = ['Sobrevendido', 'Neutro', 'Sobrecomprado']
    n_states = len(mapping)
    
    def animate(i):
        cursor.execute("SELECT markov_state FROM orders")
        states = cursor.fetchall()
        states = [mapping[state[0]] for state in states]

        transition_matrix = np.zeros((n_states, n_states))
        for i in range(1, len(states)):
            transition_matrix[states[i-1], states[i]] += 1

        ax.clear()
        ax.matshow(transition_matrix, cmap='hot')
        ax.set_xticks(np.arange(n_states))
        ax.set_yticks(np.arange(n_states))
        ax.set_xticklabels(state_names)
        ax.set_yticklabels(state_names)
        ax.set_xlabel('From')
        ax.set_ylabel('To')
    
    ani = FuncAnimation(ax.figure, animate, interval=10000, cache_frame_data=False)
    return ani

def order_type_bar_graph(ax):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    def animate(i):
        cursor.execute("SELECT order_type, COUNT(*) FROM orders GROUP BY order_type")
        data = cursor.fetchall()
        
        ax.clear()
        ax.bar([row[0] for row in data], [row[1] for row in data])
        ax.set_xlabel("Order Type")
        ax.set_ylabel("Total Orders")
    
    ani = FuncAnimation(ax.figure, animate, interval=10000, cache_frame_data=False)
    return ani

def main():
    root = tk.Tk()
    root.title("Grafico Gestão de Ordens")
    
    fig_price = plt.Figure(figsize=(5, 4), dpi=100)
    ax_price = fig_price.add_subplot(111)
    canvas_price = FigureCanvasTkAgg(fig_price, master=root)
    canvas_price.draw()
    canvas_price.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

    fig_heatmap = plt.Figure(figsize=(5, 4), dpi=100)
    ax_heatmap = fig_heatmap.add_subplot(111)
    canvas_heatmap = FigureCanvasTkAgg(fig_heatmap, master=root)
    canvas_heatmap.draw()
    canvas_heatmap.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

    fig_order = plt.Figure(figsize=(5, 4), dpi=100)
    ax_order = fig_order.add_subplot(111)
    canvas_order = FigureCanvasTkAgg(fig_order, master=root)
    canvas_order.draw()
    canvas_order.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

    anim1 = plot_price(ax_price)
    anim2 = markov_heatmap(ax_heatmap)
    anim3 = order_type_bar_graph(ax_order)

    tk.mainloop()

if __name__ == '__main__':
    main()
