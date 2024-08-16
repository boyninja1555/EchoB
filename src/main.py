from http_handler import send_http_request
from html_parser import parse_html
import sys
import os
import tkinter as tk
import webbrowser
import config

window = ""
url_bar_entry = ""
viewer_frame = ""
plaintext_viewer_text = ""

def resource_path(relative_path: str):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("..")

    return os.path.join(base_path, relative_path)

def main():
    if len(sys.argv) > 1:
        open_browser_window(send_http_request(config.PROTOCOL, sys.argv[1], None)["body"])
    else:
        open_browser_window(send_http_request(config.PROTOCOL, config.HOME_PAGE, None)["body"])

def open_url(url: str):
    if url.startswith("http://") or url.startswith("https://"):
        webbrowser.open(url)
    elif url.startswith(f"{config.PROTOCOL}://"):
        url_parts = url.split(f"{config.PROTOCOL}://")[1].split("/")
        url_bar_entry.delete(0)
        url_bar_entry.insert(0, url.split(f"{config.PROTOCOL}://")[1])

        if len(url_parts) == 1:
            open_page("text/html", send_http_request(config.PROTOCOL, url_parts[0], None)["body"])
        elif len(url_parts) == 2:
            open_page("text/html", send_http_request(config.PROTOCOL, url_parts[0], url_parts[1])["body"])

def open_browser_window(page_contents: str):
    global window
    global url_bar_entry
    global viewer_frame
    global plaintext_viewer_text

    window = tk.Tk()
    window.title(config.NAME)
    window.iconphoto(False, tk.PhotoImage(file=resource_path(os.path.join("res", "icon.png"))))
    window.geometry("850x478")
    window.state("zoomed")
    window.configure(background="#222222")

    url_bar_frame = tk.Frame(window, background="#222222")
    url_bar_frame.pack(fill=tk.X)

    url_bar_entry = tk.Entry(url_bar_frame, width=50, background="#cccccc", foreground="#222222")
    url_bar_entry.pack(fill=tk.X, expand=True)
    url_bar_entry.bind("<Return>", lambda event: open_page("text/html", send_http_request(config.PROTOCOL, url_bar_entry.get(), None)["body"]))
    url_bar_entry.focus()

    viewer_frame = tk.Frame(window, background="#222222")
    viewer_frame.pack(fill=tk.BOTH, expand=True)

    open_page("text/html", page_contents)

    window.mainloop()

def open_page(mime_type: str, page_contents: str):
    global window
    global url_bar_entry
    global viewer_frame
    global plaintext_viewer_text

    for widget in viewer_frame.winfo_children():
        widget.destroy()

    if mime_type == "text/plain":
        plaintext_viewer_text = tk.Text(viewer_frame, background="#222222", foreground="#cccccc", font=("Consolas", 12))
        plaintext_viewer_text.pack(fill=tk.BOTH, expand=True)
        plaintext_viewer_text.insert(tk.END, page_contents)
        plaintext_viewer_text.config(state=tk.DISABLED)

        window.title(f"{url_bar_entry.get()} - {config.NAME}")
    elif mime_type == "text/html":
        html_viewer = tk.Frame(viewer_frame, background="#222222")
        html_viewer.pack(fill=tk.BOTH, expand=True)

        window.title(f"{page_contents.split("<title>")[1].split("</title>")[0]} - {config.NAME}")

        body = page_contents.split("<body>")[1].split("</body>")[0]
        lines = body.split("\n")

        parse_html(tk, window, html_viewer, lines, open_url)
    else:
        window.title(f"{url_bar_entry.get()} - {config.NAME}")

        plaintext_viewer_text = tk.Text(viewer_frame, background="#222222", foreground="#cccccc", font=("Consolas", 12))
        plaintext_viewer_text.pack(fill=tk.BOTH, expand=True)
        plaintext_viewer_text.insert(tk.END, page_contents)
        plaintext_viewer_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    main()
