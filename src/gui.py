import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import threading
from PIL import Image, ImageTk

class NQueenGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("N-Queen Region Solver Visualizer")
        self.canvas_size = 500
        
        # Data State
        self.region_map = []
        self.image_refs = [] # Biar gambar gak hilang
        self.queen_img = None
        
        self.colors = {
            'A': '#FFADAD', 'B': '#FFD6A5', 'C': '#FDFFB6', 'D': '#CAFFBF',
            'E': "#A1F7FE", 'F': '#A0C4FF', 'G': "#8576DA", 'H': '#FFC6FF',
            'I': "#B0B092", 'J': "#D8F0E9", 'K': "#BBCDFF", 'L': "#E6E3D7",
            'M': '#FDE2E4', 'N': '#FAD2E1', 'O': '#E2F0CB', 'P': '#C5DEDD',
            'Q': "#66F7D3", 'R': "#EDA7E6", 'S': "#599ACC", 'T': '#99C1DE',
            'U': '#A2D2FF', 'V': '#B8C0FF', 'W': '#FFD8BE', 'X': '#ECE4DB',
            'Y': '#FFE5D9', 'Z': '#FFCAD4'
        }

        self.load_queen()
        self.setup_ui()

    def load_queen(self):
        try:
            self.queen_img = Image.open("image/queen.png")
        except:
            print("Icon tidak ditemukan, menggunakan simbol bulat")

    def setup_ui(self):
 
        frame_top = tk.Frame(self.root)
        frame_top.pack(pady=10)

        tk.Label(frame_top, text="File:").grid(row=0, column=0)
        self.file_entry = tk.Entry(frame_top, width=30)
        self.file_entry.grid(row=0, column=1, padx=5)
        tk.Button(frame_top, text="Generate", command=self.submit).grid(row=0, column=2)

        self.algo_var = tk.StringVar(value="optimization")
        tk.Radiobutton(frame_top, text="Brute Force", variable=self.algo_var, value="bruteforce").grid(row=1, column=1)
        tk.Radiobutton(frame_top, text="Optimization", variable=self.algo_var, value="optimization").grid(row=1, column=2)

        tk.Button(self.root, text="RUN SOLVER", bg="#7bc3fe", fg="black", font=('Arial', 11, 'bold'), command=self.start_solving).pack(pady=5)

        # Board
        self.canvas = tk.Canvas(self.root, width=self.canvas_size, height=self.canvas_size, bg="#f0f0f0")
        self.canvas.pack(pady=10, padx=20)

        stats_frame = tk.Frame(self.root)
        stats_frame.pack(pady=5)
        self.step_label = tk.Label(stats_frame, text="Steps: 0", font=('Courier', 10, 'bold'))
        self.step_label.pack(side=tk.LEFT, padx=20)
        self.time_label = tk.Label(stats_frame, text="Time: 0 ms", font=('Courier', 10, 'bold'))
        self.time_label.pack(side=tk.LEFT, padx=20)


    def submit(self):
        file_raw = self.file_entry.get().strip()
        
        if not file_raw:
            messagebox.showwarning("Warning", "Tulis nama file")
            return

        filename = f"../test/{file_raw}.txt"
        
        self.load_region_map(filename)

    def load_region_map(self, filename):
        try:
            with open(filename, 'r') as f:
                self.region_map = [line.strip() for line in f if line.strip()]
            
            self.draw_matrix([[0]*len(self.region_map) for _ in self.region_map])
            
            self.step_label.config(text="Steps: 0")
            self.time_label.config(text="Time: 0 ms")
            
        except FileNotFoundError:
            messagebox.showerror("Error", f"File tidak ditemukan: {filename}\nPastikan file ada di folder ../test/")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal membaca board: {e}")

    def draw_matrix(self, matrix):
        if not self.region_map: return
        self.canvas.delete("all")
        self.image_refs = [] # Reset referensi gambar
        n = len(self.region_map)
        cell_size = self.canvas_size // n
        

        render_queen = None
        if self.queen_img:
            img_size = int(cell_size * 0.75)
            resized = self.queen_img.resize((img_size, img_size), Image.Resampling.LANCZOS)
            render_queen = ImageTk.PhotoImage(resized)
            self.image_refs.append(render_queen)

        for r in range(n):
            for c in range(n):
                char = self.region_map[r][c].upper()
                color = self.colors.get(char, "#FFFFFF")
                
                # Kotak Region
                self.canvas.create_rectangle(c*cell_size, r*cell_size, (c+1)*cell_size, (r+1)*cell_size, fill=color, outline="#666")
                
                # Gambar Queen
                if matrix[r][c] == 1:
                    if render_queen:
                        self.canvas.create_image(c*cell_size + cell_size//2, r*cell_size + cell_size//2, image=render_queen)
                    else: # jika icon gagal dimuat jadinya pakai buletan
                        padding = cell_size // 4
                        self.canvas.create_oval(c*cell_size+padding, r*cell_size+padding, (c+1)*cell_size-padding, (r+1)*cell_size-padding, fill="black")

    def start_solving(self):
        if not self.file_entry.get(): 
            messagebox.showwarning("Warning", "Pilih file dulu!")
            return
        threading.Thread(target=self.run_cpp_solver, daemon=True).start()

    def run_cpp_solver(self):
        file_raw = self.file_entry.get()
        file_path = "../test/" + file_raw +".txt"
        algo = self.algo_var.get()
        exe = "./solver.exe" 
        
        found_sol = False
        try:
            process = subprocess.Popen([exe, file_path, algo], stdout=subprocess.PIPE, text=True)
            curr_board = []
            is_reading = False
            
            for line in process.stdout:
                line = line.strip()
                
                if line.startswith("INVALID BOARD:"):
                    error_msg = line.split(":", 1)[1]
                    self.root.after(0, lambda m=error_msg: messagebox.showerror("Board Invalid", m))
                    return # Langsung keluar dari fungsi agar tidak memproses board kosong
                if line.startswith("STEPS:"):
                    self.root.after(0, lambda v=line.split(":")[1]: self.step_label.config(text=f"Steps: {v}"))
                elif line.startswith("TIME:"):
                    self.root.after(0, lambda v=line.split(":")[1]: self.time_label.config(text=f"Time: {v} ms"))
                elif line == "RESULT:FOUND":
                    found_sol = True
                elif line == "START_BOARD":
                    curr_board = []
                    is_reading = True
                elif line == "END_BOARD":
                    is_reading = False
                    if curr_board: self.root.after(0, self.draw_matrix, curr_board)
                elif is_reading:
                    curr_board.append([int(x) for x in line.split(",")])

            process.wait()
            if not found_sol:
                self.root.after(0, lambda: self.draw_matrix([[0]*len(self.region_map) for _ in self.region_map]))
                self.root.after(0, lambda: messagebox.showinfo("Hasil", "Tidak ada solusi yang valid!"))
            else:
                # Fungsi internal untuk menangani logika pop-up
                def ask_save():
                    jawab = messagebox.askyesno("Solusi Ditemukan", "Solusi ditemukan! Apakah Anda ingin menyimpan hasilnya ke file?")
                    if jawab:
                        self.execute_save_command(file_path, algo)
                # Jalankan pop-up di thread utama
                self.root.after(0, ask_save)

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Gagal: {e}"))

    def execute_save_command(self, file_path, algo):
        try:
            # Jalankan C++ dengan mode save
            process = subprocess.Popen(["./solver.exe", file_path, algo, "save"], stdout=subprocess.PIPE, text=True)
            
            filename = ""
            curr_board = []
            is_reading = False

            for line in process.stdout:
                line = line.strip()
                if line.startswith("NAMA FILE:"):
                    filename = line.split(":", 1)[1].strip()
                elif line == "START_BOARD":
                    curr_board = []
                    is_reading = True
                elif line == "END_BOARD":
                    is_reading = False
                    if curr_board:
                        # Update tampilan board akhir di GUI
                        self.root.after(0, self.draw_matrix, curr_board)
                elif is_reading:
                    curr_board.append([int(x) for x in line.split(",")])
            
            process.wait()
            
            if filename:
                messagebox.showinfo("Sukses Simpan", f"Hasil disimpan & ditampilkan!\nFile: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal simpan: {e}")


if __name__ == "__main__":

    root = tk.Tk()
    app = NQueenGUI(root)
    root.mainloop()