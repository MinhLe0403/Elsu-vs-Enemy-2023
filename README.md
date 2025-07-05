# Elsu vs Enemy - A Pygame Space Shooter

A classic space shooter game built with Python and the Pygame library. This project was created in 2023 as a fun way to learn game development principles. The player controls a spaceship at the bottom of the screen and must shoot down waves of incoming enemies.


## ✨ Features

- **Main Menu:** A welcoming main menu with options to play, view instructions, or quit.
- **Dynamic Gameplay:** Enemies move in waves, creating a challenging experience.
- **Scoring System:** Keep track of your points and try to beat your personal high score.
- **Sound Effects:** Immersive background music and shooting sounds.
- **"How to Play" Screen:** A dedicated screen explaining the game controls.
- **Object-Oriented Design:** The code is structured using classes for better organization and scalability.

## 🚀 Installation & How to Run

To run this game on your local machine, please follow these steps.

### Prerequisites

- [Python 3.x](https://www.python.org/downloads/)
- `pip` (Python package installer)

### Stepsgit push -u origin main

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/MinhLe0403/Elsu-vs-Enemy-2023.git
    cd your-repository-name
    ```

2.  **Install the required package (Pygame):**
    ```bash
    pip install pygame
    ```

3.  **Run the game:**
    ```bash
    python main.py
    ```

## 🎮 How to Play

- **Move Left:** Press the `LEFT` arrow key.
- **Move Right:** Press the `RIGHT` arrow key.
- **Shoot:** Press the `SPACE` bar to fire a bullet.
- **Quit to Menu:** During the game, press `Q` to return to the main menu.

The game is over when an enemy ship collides with your ship. Try to get the highest score possible!

## 📂 Project Structure

The project is organized into a clean and understandable structure:

```
ELS_VS_ENEMY/
├── assets/
│   ├── fonts/      # Game fonts
│   ├── images/     # All game images (player, enemy, backgrounds)
│   └── sounds/     # Background music and sound effects
├── button.py       # Class for creating clickable buttons
├── main.py         # Main game file containing the core logic
└── README.md       # This documentation file
```

## Acknowledgements

- This project was built using the [Pygame](https://www.pygame.org/news) library.
- Font styles used: Roboto Thin and Roboto Bold.
- All assets (images, sounds) were collected from various open-source platforms.
