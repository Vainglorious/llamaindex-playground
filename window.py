from dotenv import load_dotenv
import os
import logging
import sys
import os.path
from llama_index import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

# Load the .env file variables into the environment
load_dotenv()

# Load the OPENAI_API_KEY from the environment variable
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("The OPENAI_API_KEY environment variable has not been set.")

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

# Initialize the chat engine outside of the GUI application to avoid reloading it on each query
if (not os.path.exists('./storage')):
    documents = SimpleDirectoryReader('data').load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist()
else:
    storage_context = StorageContext.from_defaults(persist_dir='./storage')
    index = load_index_from_storage(storage_context)

#query_engine = index.as_chat_engine()
query_engine = index.as_query_engine()


class ChatApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chat with Index")
        self.geometry("800x600")  # Set a default size for the window

        # Text area with explicit text and background color for contrast
        self.text_area = ScrolledText(self, state='disabled', fg="black", bg="white")
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Input field with explicit text and background color for contrast
        self.input_field = tk.Entry(self, fg="black", bg="white")
        self.input_field.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)  # Ensure it expands to fill space
        self.input_field.bind("<Return>", self.on_enter)

        # Button to send the message
        self.send_button = tk.Button(self, text="Send", command=self.send_query)
        self.send_button.pack(padx=10, pady=10)

    def send_query(self):
        query = self.input_field.get()
        if query:
            self.append_text(f"You: {query}\n")
            # Print user input to the terminal
            print(f"You: {query}")
            self.input_field.delete(0, tk.END)
            try:
                response = query_engine.query(query)
                self.append_text(f"Bot: {response}\n")
                # Print bot response to the terminal
                print(f"Bot: {response}")
            except Exception as e:
                self.append_text(f"Error: {e}\n")
                # Print error to the terminal
                print(f"Error: {e}")

    def on_enter(self, event):
        self.send_query()

    def append_text(self, text):
        self.text_area.configure(state='normal')
        self.text_area.insert(tk.END, text + "\n")  # Added "\n" to insert a new line after the text
        self.text_area.configure(state='disabled')
        self.text_area.yview(tk.END)


if __name__ == "__main__":
    app = ChatApplication()
    app.mainloop()
