class StyledButton(Button):
    """Custom styled button with rounded corners and background color."""
    
    def __init__(self, bg_color, **kwargs):
        super(StyledButton, self).__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.bg_color = bg_color
        self.color = get_text_primary_color()
        self.bold = True
        
        self.bind(size=self.update_background, pos=self.update_background)
        
        Clock.schedule_once(lambda dt: self.update_background(), 0)
    
    def update_background(self, *args):
        """Update the button's background canvas."""
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=get_color_from_hex(self.bg_color))
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8)])