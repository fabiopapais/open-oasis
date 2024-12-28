import pygame
import torch
import time

# Define the actions
ACTION_KEYS = [
    "inventory",
    "ESC",
    "hotbar.1",
    "hotbar.2",
    "hotbar.3",
    "hotbar.4",
    "hotbar.5",
    "hotbar.6",
    "hotbar.7",
    "hotbar.8",
    "hotbar.9",
    "forward",
    "back",
    "left",
    "right",
    "camera",
    "jump",
    "sneak",
    "sprint",
    "swapHands",
    "attack",
    "use",
    "pickItem",
    "drop",
]

# Map pygame keys to actions (customize as needed)
KEY_MAP = {
    pygame.K_e: "inventory",
    pygame.K_ESCAPE: "ESC",
    pygame.K_1: "hotbar.1",
    pygame.K_2: "hotbar.2",
    pygame.K_3: "hotbar.3",
    pygame.K_4: "hotbar.4",
    pygame.K_5: "hotbar.5",
    pygame.K_6: "hotbar.6",
    pygame.K_7: "hotbar.7",
    pygame.K_8: "hotbar.8",
    pygame.K_9: "hotbar.9",
    pygame.K_w: "forward",
    pygame.K_s: "back",
    pygame.K_a: "left",
    pygame.K_d: "right",
    pygame.K_SPACE: "jump",
    pygame.K_LSHIFT: "sneak",
    pygame.K_LCTRL: "sprint",
    pygame.K_f: "swapHands",
    pygame.MOUSEBUTTONDOWN: "attack",
    pygame.MOUSEBUTTONUP: "use",
}

# Initialize pygame
pygame.init()

# Create a window
screen = pygame.display.set_mode((800, 600))  # Larger screen
pygame.display.set_caption("Action Recorder with Normal Mouse Movement")

# FPS and action storage
FPS = 20
clock = pygame.time.Clock()
actions = []

# Define constants for mouse movement normalization
MOUSE_MOVEMENT_RANGE = 160  # Mouse movement range for finer control
BOX_SIZE = 400  # Bounding box size
BOX_COLOR = (255, 0, 0)  # Red bounding box

def capture_actions():
    """
    Capture the current state of actions as a dictionary.
    """
    action_state = {key: 0 for key in ACTION_KEYS}  # Default all to 0
    keys = pygame.key.get_pressed()

    # Update key-based actions
    for pygame_key, action in KEY_MAP.items():
        if isinstance(pygame_key, int):  # For keyboard keys
            if keys[pygame_key]:
                action_state[action] = 1

    # Update mouse-based actions
    mouse_buttons = pygame.mouse.get_pressed()
    if mouse_buttons[0]:  # Left click
        action_state["attack"] = 1
    if mouse_buttons[2]:  # Right click
        action_state["use"] = 1

    # Get raw mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Clip values to the bounding box range
    clipped_x = max(0, min(MOUSE_MOVEMENT_RANGE, mouse_x * MOUSE_MOVEMENT_RANGE // 800))
    clipped_y = max(0, min(MOUSE_MOVEMENT_RANGE, mouse_y * MOUSE_MOVEMENT_RANGE // 600))

    # Normalize the mouse position to the range 0 to 80 for the camera
    camera_x = int((clipped_x / MOUSE_MOVEMENT_RANGE) * 80)  # Discrete value (integer)
    camera_y = int((clipped_y / MOUSE_MOVEMENT_RANGE) * 80)  # Discrete value (integer)

    action_state["camera"] = [camera_x, camera_y]

    return action_state


# Main loop
running = True
try:
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Check if the 'q' key is pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            running = False

        # Capture and store actions
        action_state = capture_actions()
        actions.append(action_state)

        # Display status
        screen.fill((30, 30, 30))
        font = pygame.font.Font(None, 36)
        text = font.render(f"Captured: {len(actions)} actions", True, (200, 200, 200))
        screen.blit(text, (50, 50))

        # Draw the bounding box
        box_x = (screen.get_width() - BOX_SIZE) // 2
        box_y = (screen.get_height() - BOX_SIZE) // 2
        pygame.draw.rect(screen, BOX_COLOR, (box_x, box_y, BOX_SIZE, BOX_SIZE), 2)

        # Draw the mouse position within the bounding box
        normalized_x = (pygame.mouse.get_pos()[0] / 800) * BOX_SIZE
        normalized_y = (pygame.mouse.get_pos()[1] / 600) * BOX_SIZE
        pygame.draw.circle(
            screen,
            (0, 255, 0),  # Green dot
            (int(box_x + normalized_x), int(box_y + normalized_y)),
            5,
        )

        pygame.display.flip()

        # Limit FPS
        clock.tick(FPS)

except KeyboardInterrupt:
    pass

finally:
    # Save the actions to a .pt file
    torch.save(actions, "captured.actions.pt")
    print(f"Saved {len(actions)} actions to captured.actions.pt")

    pygame.quit()








