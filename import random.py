import random
import customtkinter as ctk

# ตั้งค่าธีมการแสดงผลสีสันสบายตาแนวโลกมุสลิม (โทนเขียว-ทอง-เอิร์ธโทน)
ctk.set_appearance_mode("dark")


class SalahGame(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("เกมภารกิจเรียงลำดับการละหมาด 🕋")
        self.geometry("640x550")  # ขยายความกว้างหน้าต่างขึ้นเล็กน้อยเพื่อรองรับข้อความ
        self.resizable(False, False)
        self.configure(fg_color="#0f172a")

        # ปรับข้อความให้กระชับขึ้นเพื่อไม่ให้ยาวเกินขอบปุ่ม
        self.correct_sequence = [
            "1. ตักบีร่อตุ้ลเอี๊ยะห์รอม\n(กล่าวอัลลอฮุอักบัร)",
            "2. ยืนตรงและอ่าน\nสูเราะห์อัลฟะติฮะฮ์",
            "3. รุกัวะอ์\n(ก้มโน้มตัวไปข้างหน้า)",
            "4. เอี๊ยะอ์ติดาล\n(ยืนตรงขึ้นมาอีกครั้ง)",
            "5. สุญูด ครั้งที่ 1\n(กราบราบกับพื้น)",
            "6. นั่งระหว่าง\nสองสุญูด",
            "7. สุญูด ครั้งที่ 2\n(กราบอีกครั้ง)",
            "8. อ่านตะชะฮ์ฮุด\n(นั่งอ่านบทกล่าวก่อนจบ)",
            "9. ให้สลาม\n(หันหน้าขวาและซ้าย)",
        ]

        self.choices = self.correct_sequence.copy()
        random.shuffle(self.choices)

        self.current_step_index = 0
        self.score = 0

        self.setup_ui()

    def setup_ui(self):
        # 1. ส่วนหัวของเกม
        self.title_label = ctk.CTkLabel(
            self,
            text="🕌 Salah Sequence Game 🕌",
            font=("Segoe UI", 26, "bold"),
            text_color="#10b981",
        )
        self.title_label.pack(pady=(20, 5))

        self.desc_label = ctk.CTkLabel(
            self,
            text="ภารกิจ: จงคลิกเลือกขั้นตอนการละหมาดตามลำดับที่ถูกต้อง",
            font=("Sarabun", 15),
            text_color="#94a3b8",
        )
        self.desc_label.pack(pady=(0, 15))

        # 2. ส่วนแสดงสถานะและคะแนน
        self.status_frame = ctk.CTkFrame(self, fg_color="#1e293b", height=50)
        self.status_frame.pack(padx=30, pady=10, fill="x")

        self.step_label = ctk.CTkLabel(
            self.status_frame,
            text=f"ตามหาขั้นตอนที่: {self.current_step_index + 1} / 9",
            font=("Sarabun", 16, "bold"),
            text_color="#f59e0b",
        )
        self.step_label.pack(side="left", padx=20, pady=10)

        self.score_label = ctk.CTkLabel(
            self.status_frame,
            text=f"คะแนน: {self.score}",
            font=("Sarabun", 16, "bold"),
            text_color="#f8fafc",
        )
        self.score_label.pack(side="right", padx=20, pady=10)

        # 3. พื้นที่แสดงปุ่มตัวเลือก (Grid 3x3)
        self.grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_frame.pack(padx=30, pady=15, fill="both", expand=True)

        self.grid_frame.columnconfigure((0, 1, 2), weight=1, pad=10)
        self.grid_frame.rowconfigure((0, 1, 2), weight=1, pad=10)

        self.buttons = []
        self.create_choice_buttons()

        # 4. กล่องข้อความแสดงผลการกด
        self.feedback_label = ctk.CTkLabel(
            self,
            text="กดเริ่มเล่นได้เลยครับ บิสมิลลาฮ์...",
            font=("Sarabun", 15, "italic"),
            text_color="#38bdf8",
        )
        self.feedback_label.pack(pady=15)

    def create_choice_buttons(self):
        index = 0
        for r in range(3):
            for c in range(3):
                text_content = self.choices[index]
                # ลบ wraplength=140 ออกเรียบร้อยแล้ว และใช้การตัดบรรทัดด้วย \n ในตัวแปรแทน
                btn = ctk.CTkButton(
                    self.grid_frame,
                    text=text_content,
                    font=("Sarabun", 13, "bold"),
                    fg_color="#334155",
                    hover_color="#475569",
                    text_color="#f1f5f9",
                    corner_radius=12,
                    height=75,
                    command=lambda t=text_content: self.check_answer(t),
                )
                btn.grid(row=r, column=c, sticky="nsew", padx=5, pady=5)
                self.buttons.append(btn)
                index += 1

    def check_answer(self, selected_text):
        target_text = self.correct_sequence[self.current_step_index]

        if selected_text == target_text:
            self.score += 10
            self.feedback_label.configure(
                text="ถูกต้องล่ะฮะ! 🎉 (+10 คะแนน)", text_color="#10b981"
            )

            for btn in self.buttons:
                if btn.cget("text") == selected_text:
                    btn.configure(
                        fg_color="#059669",
                        state="disabled",
                        text_color="#a7f3d0",
                    )

            self.current_step_index += 1
            self.update_status()

            if self.current_step_index >= len(self.correct_sequence):
                self.end_game(victory=True)
        else:
            self.feedback_label.configure(
                text="อ๊ะ ลำดับนี้ยังไม่ถูกนะ ลองคิดใหม่อีกทีครับ สู้ๆ!",
                text_color="#ef4444",
            )
            if self.score > 0:
                self.score -= 2
            self.update_status()

    def update_status(self):
        self.score_label.configure(text=f"คะแนน: {self.score}")
        if self.current_step_index < len(self.correct_sequence):
            self.step_label.configure(
                text=f"ตามหาขั้นตอนที่: {self.current_step_index + 1} / 9"
            )

    def end_game(self, victory):
        if victory:
            self.step_label.configure(text="ภารกิจเสร็จสิ้น! ✨")
            self.feedback_label.configure(
                text=f"มาชาอัลลอฮ์! คุณเรียงลำดับการละหมาดได้ถูกต้องครบถ้วน คะแนนรวมของคุณคือ {self.score} คะแนน",
                text_color="#fbbf24",
            )

            for btn in self.buttons:
                btn.destroy()

            restart_btn = ctk.CTkButton(
                self.grid_frame,
                text="🔄 เล่นใหม่อีกครั้ง",
                font=("Sarabun", 16, "bold"),
                fg_color="#10b981",
                hover_color="#059669",
                command=self.reset_game,
            )
            restart_btn.pack(pady=40, ipadx=20, ipady=10)

    def reset_game(self):
        for widget in self.winfo_children():
            widget.destroy()

        random.shuffle(self.choices)
        self.current_step_index = 0
        self.score = 0
        self.setup_ui()


if __name__ == "__main__":
    app = SalahGame()
    app.mainloop()
