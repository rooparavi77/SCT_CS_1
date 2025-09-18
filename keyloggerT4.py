

import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
from datetime import datetime

class SafeKeyLoggerApp:
    def __init__(self, root):
        self.root = root
        root.title("Safe Key Recorder (Consent-Only)")
        root.geometry("700x450")

        # State
        self.recording = False
        self.log = []  # list of (timestamp_str, key_str)

        # UI
        toolbar = tk.Frame(root)
        toolbar.pack(fill="x", padx=6, pady=6)

        self.start_btn = tk.Button(toolbar, text="Start Recording", command=self.start)
        self.start_btn.pack(side="left", padx=4)
        self.stop_btn = tk.Button(toolbar, text="Stop Recording", command=self.stop, state="disabled")
        self.stop_btn.pack(side="left", padx=4)
        self.save_btn = tk.Button(toolbar, text="Save Log", command=self.save_log)
        self.save_btn.pack(side="left", padx=4)
        self.clear_btn = tk.Button(toolbar, text="Clear", command=self.clear_log)
        self.clear_btn.pack(side="left", padx=4)

        self.status_label = tk.Label(toolbar, text="Status: Idle")
        self.status_label.pack(side="right", padx=6)

        # Scrolled text to show captured keys
        self.output = scrolledtext.ScrolledText(root, wrap="word", height=20, state="disabled")
        self.output.pack(fill="both", expand=True, padx=6, pady=6)

        # Instruction / consent reminder
        instr = ("This app records keys pressed while the window is focused.\n"
                 "Only use this for your own testing or with explicit consent.")
        self.output.configure(state="normal")
        self.output.insert("end", instr + "\n\n")
        self.output.configure(state="disabled")

        # Bind key event to root (but we only log when recording)
        root.bind_all("<Key>", self._on_key_event, add="+")  # add so we don't overwrite other handlers

    def start(self):
        self.recording = True
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.status_label.config(text="Status: Recording — window must be focused")
        self._append_line("[Recording started at {}]\n".format(datetime.now().isoformat(timespec="seconds")))

    def stop(self):
        self.recording = False
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.status_label.config(text="Status: Idle")
        self._append_line("[Recording stopped at {}]\n".format(datetime.now().isoformat(timespec="seconds")))

    def _on_key_event(self, event):
        # Only record when recording is active and the window has focus
        if not self.recording:
            return

        # Check focus: only record if the event widget belongs to our app's toplevel
        focused = self.root.focus_displayof()  # None if not focused
        # Another check: ensure root is the focused window (works cross-platform)
        if focused is None:
            return

        # Construct a readable representation for special keys
        key_repr = event.keysym  # "a", "Return", "space", "BackSpace", etc.
        # For printable single-char keys, prefer event.char
        if event.char and event.char.isprintable():
            key_display = event.char
        else:
            key_display = f"<{key_repr}>"

        ts = datetime.now().isoformat(timespec="seconds")
        self.log.append((ts, key_display))

        # Append to UI
        self._append_line(f"{ts}  {key_display}")

    def _append_line(self, text):
        self.output.configure(state="normal")
        self.output.insert("end", text + "\n")
        self.output.see("end")
        self.output.configure(state="disabled")

    def save_log(self):
        if not self.log:
            messagebox.showinfo("Save Log", "No keystrokes recorded.")
            return

        # Ask user where to save
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save keystroke log (consensual)"
        )
        if not filename:
            return

        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("SafeKeyLogger — Authorized Use Only\n")
                f.write("Recorded entries:\n\n")
                for ts, key in self.log:
                    f.write(f"{ts}\t{key}\n")
            messagebox.showinfo("Save Log", f"Log saved to: {filename}")
        except Exception as e:
            messagebox.showerror("Save Log", f"Failed to save file: {e}")

    def clear_log(self):
        if messagebox.askyesno("Clear Log", "Clear recorded entries?"):
            self.log.clear()
            self.output.configure(state="normal")
            self.output.delete("2.0", "end")  # remove everything after the initial lines
            self.output.configure(state="disabled")
            self._append_line("[Log cleared at {}]".format(datetime.now().isoformat(timespec="seconds")))


if __name__ == "__main__":
    root = tk.Tk()
    app = SafeKeyLoggerApp(root)
    root.mainloop()
