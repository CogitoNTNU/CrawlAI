import pygame


class Button:
    """General button functions"""

    def __init__(
        self,
        text,
        pos,
        width,
        height,
        font,
        color,
        hover_color,
        text_color,
        active_color=None,
        callback=None,
    ):
        """Initializes a button with the function name as input"""
        self.text = text
        self.pos = pos
        self.width = width
        self.height = height
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.active_color = active_color if active_color else color
        self.rect = pygame.Rect(pos[0], pos[1], width, height)
        self.callback = callback
        self.toggled = False

    def render(self, screen):
        """mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)
        color = self.hover_color if is_hovered else self.color"""
        current_color = self.active_color if self.toggled else self.color
        pygame.draw.rect(screen, current_color, self.rect)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event) -> bool:
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)
    
    def is_paused_clicked(self, event) -> bool: 
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.toggled = not self.toggled
                if self.callback:  # Check if there’s a function to call
                    self.callback()  # Call the button's callback function
                return True
        return False
    
    def activate(self):
        """Activate button (sets toggled state to True)."""
        self.toggled = True
        if self.callback:
            self.callback()


    def deactivate(self):
        self.toggled = False

class Interface:
    def __init__(self):
        """Initializes the elements in the interface"""

        self.buttons: list[Button] = [] #for all buttons in the interface 
        self.active_button = Button|None
        self.only_one_simultaneously_buttons = [] #buttons that can't be active simultaneously 


    def add_button(self, button: Button) -> Button:
        self.buttons.append(button)
        return button

    def remove_button(self, button: Button) -> Button: 
        if button in self.buttons:
            self.buttons.remove(button)
            return button
        
    def add_only_one_simultaneously_buttons(self, button: Button) -> Button:
        self.only_one_simultaneously_buttons.append(button)
        self.buttons.append(button) #don't have to append on both lists manually
        return button
    
    def remove_only_one_simultaneously_buttons(self, button: Button) -> Button: 
        if button in self.only_one_simultaneously_buttons:
            self.buttons.remove(button)
            return button

    def render(self, screen):
        """Render all UI elements."""
        for button in self.buttons:
            button.render(screen)

    def handle_events(self, event):
        """Handle events for all UI elements."""
        for button in self.buttons:
            button.is_clicked(event)

    def handle_pause_events(self, event): 
        for button in self.buttons:
            if button.text == "Pause": 
                button.is_paused_clicked(event)

    def is_any_button_clicked(self, event) -> bool:
        for button in self.buttons:
            if button.is_clicked(event):  # If any button is clicked
                return True  # Return True immediately
        return False

    """def handle_only_one_function(self, event) -> Button|None:
        Activates only one of the mutually exclusive buttons.
        for button in self.only_one_simultaneously_buttons:
            if button.is_clicked(event):  # If this button was clicked
                # If the button is not already active, activate it
                if not button.toggled:
                    button.toggled = True
                    self.active_button = button
                    # Deactivate all other mutually exclusive buttons
                    for other_button in self.only_one_simultaneously_buttons:
                        if other_button != button:
                            other_button.deactivate()
                    # Execute the callback for the newly activated button
                    if button.callback:
                        button.callback()
                else:
                    # Deactivate if it was already active
                    button.deactivate()
                    self.active_button = None
                return button  # Return the clicked (now active) button
        return None  # No button was clicked"""
    
    def handle_only_one_function(self, event) -> Button | None:
        """Manage toggling for mutually exclusive buttons."""
        for button in self.only_one_simultaneously_buttons:
            if button.is_clicked(event):  # If this button was clicked
                # Toggle button only if it's not already active
                if button != self.active_button:
                    # Activate the clicked button
                    button.activate()
                    # Deactivate previously active button, if any
                    if self.active_button:
                        self.active_button.deactivate()
                    # Set the clicked button as the new active button
                    self.active_button = button
                else:
                    # Deactivate the active button if it's clicked again
                    button.deactivate()
                    self.active_button = None
                return button  # Return the clicked button
        return None  # No button was clicked
    
    def any_active_only_one_simultaneously_buttons_active(self) -> bool:
        return any(button.toggled for button in self.only_one_simultaneously_buttons)


        
  
    

