import tkinter as tk

class CommentBuild:

    def __init__(self, comment_id, controller):

        self.controller = controller
        self.comment_info = self.controller.fetch_comment_info(comment_id)


    def build(self, frame, row):

        self.commenter_label = tk.Label(frame, text=self.comment_info[1], font=("SoleilSb", 12), bg="white")
        self.text_label = tk.Label(frame, text=self.comment_info[0], wraplength=400, font=("SoleilLt", 15), bg="white")

        self.comment_space = tk.Label(frame, text="", font=("Soleil-Bold", 12), bg="white")

        self.commenter_label.grid(column=0, row=row, sticky="w", padx=20, pady=0)
        self.text_label.grid(column=0, row=row + 1, sticky="w", padx=(20,0), pady=0, columnspan=10)
        self.comment_space.grid(column=0, row=row + 2, sticky="w", columnspan=10)

