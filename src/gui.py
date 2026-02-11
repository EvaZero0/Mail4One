import tkinter as tk
from tkinter import ttk
import webbrowser
import threading

from analyzer import analyze_emails


def show_gui(tb_profile):
    """Display GUI with loading screen, then show results."""
    
    # Initialize main window
    root = tk.Tk()
    root.title("Mail4One - Unsubscribe Tool (Thunderbird Edition)")
    root.geometry("1000x600")
    
    # Create main frame with padding
    main_frame = ttk.Frame(root, padding="10")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    # Configure grid weights for responsive resizing
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    
    # Display loading screen
    loading_label = ttk.Label(main_frame, text="Analyzing your emails and extracting unsubscribe links.\nThis may take a few minutes depending on your mailbox size.\nPlease be patient.", font=('Arial', 14))
    loading_label.pack(expand=True)
    
    # Show indeterminate progress bar
    progress = ttk.Progressbar(main_frame, mode='indeterminate')
    progress.pack(pady=20)
    progress.start()
    
    # Store email analysis results
    sender_data = {}
    
    def analyze_in_background():
        """Run email analysis in separate thread to keep GUI responsive."""
        nonlocal sender_data
        sender_data = analyze_emails(tb_profile)
        root.after(0, show_results)
    
    def show_results():
        """Display results after analysis is complete."""
        # Remove loading screen
        progress.stop()
        loading_label.destroy()
        progress.destroy()
        
        # Create results container
        frame = ttk.Frame(main_frame)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(frame, text="Here are your results. Caution is advised when clicking unsubscribe links.", font=('Arial', 14, 'bold'), anchor='w').pack(pady=10, fill=tk.X)
        
        # Set up scrollable canvas for results list
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        # Update scroll region when content changes
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Create header row
        header_frame = ttk.Frame(scrollable_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(header_frame, text="Count", width=8, font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        ttk.Label(header_frame, text="Sender", width=40, font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        ttk.Label(header_frame, text="Your Account", width=25, font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        ttk.Label(header_frame, text="Click to Open Browser", width=15, font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        
        # Sort senders by email count (descending)
        sorted_senders = sorted(sender_data.items(), key=lambda x: x[1]['count'], reverse=True)
        
        # Create row for each sender with unsubscribe link
        for key, data in sorted_senders:
            if data['unsubscribe']:
                row_frame = ttk.Frame(scrollable_frame)
                row_frame.pack(fill=tk.X, padx=10, pady=2)
                
                # Display email count, sender, and recipient
                ttk.Label(row_frame, text=str(data['count']), width=8).pack(side=tk.LEFT, padx=5)
                ttk.Label(row_frame, text=data['sender'][:50], width=40).pack(side=tk.LEFT, padx=5)
                ttk.Label(row_frame, text=data['recipient'][:30], width=25).pack(side=tk.LEFT, padx=5)
                
                # Create button that opens unsubscribe link in browser
                unsub_link = data['unsubscribe']
                btn = ttk.Button(row_frame, text="Unsubscribe", width=15, 
                            command=lambda link=unsub_link: webbrowser.open(link))
                btn.pack(side=tk.LEFT, padx=5)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    # Start analysis in background thread
    thread = threading.Thread(target=analyze_in_background, daemon=True)
    thread.start()
    
    # Start GUI event loop
    root.mainloop()
