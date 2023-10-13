for x in range(0, 8, 2):
    for y in range(0, 8, 2):
        print(f"""
self.buttons[{y}][{x}] = SquareButtonDark(self, ({y}, {x}))
self.buttons[{y}][{x}].configure(command=lambda: self.buttonCommand(self.buttons[{y}][{x}].location))
try:
    self.buttons[{y}][{x}].configure(bg_color="transparent", image=self.getPieceImageFromLocation(({y}, {x}), self.board))
except ValueError:
    pass
self.buttons[{y}][{x}].grid(column={y}, row={7-x})

self.buttons[{y+1}][{x}] = SquareButtonLight(self, ({y+1}, {x}))
self.buttons[{y+1}][{x}].configure(command=lambda: self.buttonCommand(self.buttons[{y+1}][{x}].location))
try:
    self.buttons[{y+1}][{x}].configure(bg_color="transparent", image=self.getPieceImageFromLocation(({y+1}, {x}), self.board))
except ValueError:
    pass
self.buttons[{y+1}][{x}].grid(column={y+1}, row={7-x})""")

for x in range(1, 8, 2):
    for y in range(0, 8, 2):
        print(f"""
self.buttons[{y}][{x}] = SquareButtonLight(self, ({y}, {x}))
self.buttons[{y}][{x}].configure(command=lambda: self.buttonCommand(self.buttons[{y}][{x}].location))
try:
    self.buttons[{y}][{x}].configure(bg_color="transparent", image=self.getPieceImageFromLocation(({y}, {x}), self.board))
except ValueError:
    pass
self.buttons[{y}][{x}].grid(column={y}, row={7-x})

self.buttons[{y+1}][{x}] = SquareButtonDark(self, ({y+1}, {x}))
self.buttons[{y+1}][{x}].configure(command=lambda: self.buttonCommand(self.buttons[{y+1}][{x}].location))
try:
    self.buttons[{y+1}][{x}].configure(bg_color="transparent", image=self.getPieceImageFromLocation(({y+1}, {x}), self.board))
except ValueError:
    pass
self.buttons[{y+1}][{x}].grid(column={y+1}, row={7-x})""")
