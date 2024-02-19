import tkinter as tk
from tkinter import ttk
from SABM_Economics_Main import run_simulation

def create_gui():
    def on_submit():
        para_cost = [int(cost1_entry.get()), int(cost2_entry.get())]
        para_a = int(a_entry.get())
        para_d = float(d_entry.get())
        para_beta = float(beta_entry.get())
        initial_price = [int(p1_entry.get()), int(p2_entry.get())]
        load_data_key = load_data_entry.get()
        load_strategy = load_strategy_entry.get()
        has_conversation_data = has_conversation_entry.get()
        
        if load_data_key != '':
            load_data = f"Output/{load_data_key}/"
        else:
            load_data = ''
        
        if load_strategy == 'True': strategy = True
        else: strategy = False

        if has_conversation_data == 'True': has_conversation = True
        else: has_conversation = False

        run_simulation(para_cost, para_a, para_d, para_beta, initial_price, load_data, strategy, has_conversation)
    
    root = tk.Tk()
    root.title("Smart Agents Online: Collusion Simulation")

    cost_label = ttk.Label(root, text="Cost Parameters:")
    cost1_entry = ttk.Entry(root)
    cost2_entry = ttk.Entry(root)

    a_label = ttk.Label(root, text="Parameter 'a':")
    a_entry = tk.Entry(root, bg='gray')

    d_label = ttk.Label(root, text="Parameter 'd':")
    d_entry = ttk.Entry(root)

    beta_label = ttk.Label(root, text="Parameter 'β':")
    beta_entry = ttk.Entry(root)

    p_label = ttk.Label(root, text="Initial Prices:")
    p1_entry = ttk.Entry(root)
    p2_entry = ttk.Entry(root)

    load_data_label = ttk.Label(root, text="Load Data:")
    load_data_entry = ttk.Entry(root)

    load_strategy_label = ttk.Label(root, text = 'Load Strategy:')
    load_strategy_entry = ttk.Combobox(root, values = ['True', 'False'])

    has_conversation_label = ttk.Label(root, text = 'Conversation:')
    has_conversation_entry = ttk.Combobox(root, values = ['False', 'True'])


    submit_button = ttk.Button(root, text="Run Simulation", command=on_submit)

    # Set default values
    cost1_entry.insert(0, '2')
    cost2_entry.insert(0, '2')
    a_entry.insert(0, '14')
    d_entry.insert(0, '0.00333333333333')
    p1_entry.insert(0, '2')
    p2_entry.insert(0, '2')
    beta_entry.insert(0, '0.00666666666666')
    load_data_entry.insert(0, '')
    load_strategy_entry.insert(0, 'True')
    has_conversation_entry.insert(0, 'False')

    # Set interface
    cost_label.grid(row=0, column=0, sticky='w')
    cost1_entry.grid(row=0, column=1)
    cost2_entry.grid(row=0, column=2)

    a_label.grid(row=1, column=0, sticky='w')
    a_entry.grid(row=1, column=1)

    d_label.grid(row=2, column=0, sticky='w')
    d_entry.grid(row=2, column=1)

    beta_label.grid(row=3, column=0, sticky='w')
    beta_entry.grid(row=3, column=1)

    p_label.grid(row=4, column=0, sticky='w')
    p1_entry.grid(row=4, column=1)
    p2_entry.grid(row=4, column=2)

    load_data_label.grid(row=5, column=0, sticky='w')
    load_data_entry.grid(row=5, column=1)

    load_strategy_label.grid(row=6, column=0, sticky='w')
    load_strategy_entry.grid(row=6, column=1)

    has_conversation_label.grid(row=7, column=0, sticky='w')
    has_conversation_entry.grid(row=7, column=1)

    a_entry.config(state='readonly')

    submit_button.grid(row=8, column=0, columnspan=3, pady=10)

    root.mainloop()
