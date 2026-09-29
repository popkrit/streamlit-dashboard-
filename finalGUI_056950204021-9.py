import tkinter as tk
from tkinter import messagebox
import csv
import os

# ฟังก์ชันบันทึกข้อมูลลง sciRMUTP.csv
def save_data():
    curriculum = entry_curriculum.get().strip()
    male = entry_male.get().strip()
    female = entry_female.get().strip()

    if not curriculum or not male or not female:
        messagebox.showerror("ข้อผิดพลาด", "กรุณากรอกข้อมูลให้ครบทุกช่อง")
        return

    try:
        male = int(male)
        female = int(female)
    except ValueError:
        messagebox.showerror("ข้อผิดพลาด", "จำนวนชายและหญิงต้องเป็นตัวเลขเท่านั้น")
        return

    # ตรวจสอบว่ามีไฟล์หรือยัง ถ้ายังไม่มีให้สร้างพร้อม Header
    file_exists = os.path.isfile('sciRMUTP.csv')

    with open('sciRMUTP.csv', mode='a', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        if not file_exists or os.path.getsize('sciRMUTP.csv') == 0:
            writer.writerow(['curriculum', 'male', 'female'])
        writer.writerow([curriculum, male, female])

    messagebox.showinfo("สำเร็จ", f"บันทึกข้อมูล {curriculum} เรียบร้อยแล้ว!")
    
    # เคลียร์ช่องกรอกข้อมูล
    entry_curriculum.delete(0, tk.END)
    entry_male.delete(0, tk.END)
    entry_female.delete(0, tk.END)
    entry_curriculum.focus()

# สร้างหน้าต่าง GUI
root = tk.Tk()
root.title("ระบบบันทึกข้อมูลนักศึกษา - sciRMUTP")
root.geometry("380x260")
root.configure(bg="#f8fafc")

# หัวข้อ
label_head = tk.Label(root, text="บันทึกข้อมูลนักศึกษา sciRMUTP", font=("Tahoma", 12, "bold"), bg="#f8fafc", fg="#0f172a")
label_head.pack(pady=10)

frame = tk.Frame(root, bg="#f8fafc")
frame.pack(pady=5)

# ช่องกรอก curriculum
tk.Label(frame, text="หลักสูตร (curriculum):", font=("Tahoma", 10), bg="#f8fafc").grid(row=0, column=0, sticky="e", padx=5, pady=5)
entry_curriculum = tk.Entry(frame, font=("Tahoma", 10), width=20)
entry_curriculum.grid(row=0, column=1, padx=5, pady=5)

# ช่องกรอก male
tk.Label(frame, text="ชาย (male):", font=("Tahoma", 10), bg="#f8fafc").grid(row=1, column=0, sticky="e", padx=5, pady=5)
entry_male = tk.Entry(frame, font=("Tahoma", 10), width=20)
entry_male.grid(row=1, column=1, padx=5, pady=5)

# ช่องกรอก female
tk.Label(frame, text="หญิง (female):", font=("Tahoma", 10), bg="#f8fafc").grid(row=2, column=0, sticky="e", padx=5, pady=5)
entry_female = tk.Entry(frame, font=("Tahoma", 10), width=20)
entry_female.grid(row=2, column=1, padx=5, pady=5)

# ปุ่มบันทึก
btn = tk.Button(root, text="บันทึกข้อมูลลง sciRMUTP.csv", command=save_data, font=("Tahoma", 10, "bold"), bg="#2563eb", fg="white", padx=10, pady=5, cursor="hand2")
btn.pack(pady=15)

root.mainloop()