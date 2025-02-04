<!-- FlappyBird.svelte -->
<script>
  import { onMount, onDestroy } from "svelte";
  import { highScores } from "../stores/highscores";
  import { networkScores } from "../stores/networkScores";

  export let isUploading = false;
  export let progress = 0;
  export let username = "";
  export let password = '';
  let gameEnded = false;

  let gameContainer;
  let p5Instance;

  // Load p5 and p5.sound from CDN
  function loadP5Libraries() {
    return new Promise((resolve) => {
      const p5Script = document.createElement("script");
      p5Script.src = "https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/p5.js";

      const p5SoundScript = document.createElement("script");
      p5SoundScript.src =
        "https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/addons/p5.sound.js";

      p5Script.onload = () => {
        document.head.appendChild(p5SoundScript);
      };

      p5SoundScript.onload = () => {
        resolve(window.p5);
      };

      document.head.appendChild(p5Script);
    });
  }

  onMount(async () => {
    const p5 = await loadP5Libraries();

    const sketch = (p) => {
      // Global variables
      let sprite_flappy, sprite_pipe, sprite_city, sprite_floor, sprite_title;
      let sound_point, sound_wing, sound_hit, sound_die, sound_sweetwing;
      let font_flappy;

      let mousePress = false;
      let mousePressEvent = false;
      let mouseReleaseEvent = false;
      let keyPress = false;
      let keyPressEvent = false;
      let keyReleaseEvent = false;

      let pipes = [];
      let score = 0;
      let hightscore = 0;
      let speed = 3;
      let gap = 80;
      let gameover = false;
      let page = "MENU";
      let overflowX = 0;

      // Utility functions
      function clamp(value, min, max) {
        return Math.min(Math.max(value, min), max);
      }

      function smoothMove(pos, target, speed) {
        return pos + (target - pos) * speed;
      }

      function press(txt, x, y) {
        const tX = p.width / 2;
        const tY = p.height / 2;
        let this_h = false;

        if (
          p.mouseX > tX + x - p.textWidth(txt) / 2 - 10 &&
          p.mouseX < tX + x + p.textWidth(txt) / 2 + 10 &&
          p.mouseY > tY + y - p.textAscent() / 2 - 10 &&
          p.mouseY < tY + y + p.textAscent() / 2 + 10
        ) {
          this_h = true;
        }

        p.push();
        p.textSize(16);

        if (this_h && mousePress) {
          p.noStroke();
          p.fill(83, 56, 71);
          p.rect(x, y + 3, p.textWidth(txt) + 35, p.textAscent() + 20);

          p.fill(250, 117, 49);
          p.stroke(255);
          p.strokeWeight(3);
          p.rect(x, y + 2, p.textWidth(txt) + 25, p.textAscent() + 10);

          p.noStroke();
          p.fill(255);
          p.text(txt, x, y + 2);
        } else {
          p.noStroke();
          p.fill(83, 56, 71);
          p.rect(x, y + 2, p.textWidth(txt) + 35, p.textAscent() + 22);

          if (this_h) {
            p.fill(250, 117, 49);
          } else {
            p.fill(230, 97, 29);
          }
          p.stroke(255);
          p.strokeWeight(3);
          p.rect(x, y, p.textWidth(txt) + 25, p.textAscent() + 10);

          p.noStroke();
          p.fill(255);
          p.text(txt, x, y);
        }
        p.pop();

        if (this_h && mouseReleaseEvent) {
          try {
            sound_sweetwing.play();
          } catch (e) {}
        }

        return this_h && mouseReleaseEvent;
      }

      function resetGame() {
        gameEnded = false;
        gameover = false;
        gap = 80;
        speed = 3;
        score = 0;
        flappy_bird.y = p.height / 2;
        flappy_bird.falls = false;
        flappy_bird.velocityY = 0;
        flappy_bird.angle = 0;
        flappy_bird.flashAnim = 0;
        flappy_bird.flashReturn = false;
        pipes = [];
        flappy_bird.target = 10000;
        menu_gameover.ease = 0;
      }

      const handleGameOver = async () => {
        if (!gameEnded && score > 0) {
          gameEnded = true;
          // Update local high scores
          highScores.addScore(username, score);

          // Save to network scores - use the current FTP config
          try {
            await networkScores.addScore(username, score, {
              host: "dia.whatbox.ca",
              port: 25850,
              user: username,
              password: password, // We need to pass this from App.svelte
            });
          } catch (e) {
            console.warn("Error saving network score:", e);
          }
        }
      };

      const menu_gameover = {
        ease: 0,
        easing: false,
        open: false,

        display() {
          if (!gameEnded) {
            handleGameOver();
          }
          p.push();
          p.translate(p.width / 2, p.height / 2);
          p.scale(this.ease);

          p.stroke(83, 56, 71);
          p.strokeWeight(2);
          p.fill(222, 215, 152);
          p.rect(0, 0, 200, 200);

          p.noStroke();
          p.fill(83, 56, 71);
          p.text("Game Over", -0, -50);

          p.textSize(20);
          p.strokeWeight(5);
          p.stroke(83, 56, 71);
          p.fill(255);
          p.text("Flappy Bird", 0, -80);

          p.push();
          p.textAlign(p.LEFT, p.CENTER);
          p.textSize(12);
          p.noStroke();
          p.fill(83, 56, 71);
          p.text("score : ", -80, 0);
          p.text("hightscore : ", -80, 30);

          p.stroke(0);
          p.strokeWeight(3);
          p.fill(255);
          p.text(score, 20, 0);
          p.text(hightscore, 20, 30);
          p.pop();

          if (press("restart", 0, 140)) {
            resetGame();
          }

          if (press(" menu ", 0, 190)) {
            page = "MENU";
          }
          p.pop();
        },

        update() {
          if (this.easing) {
            this.ease += 0.1;
            if (this.ease > 1) {
              this.open = true;
              this.ease = 1;
              this.easing = false;
            }
          }
        },

        easein() {
          this.easing = true;
        },
      };

      const flappy_bird = {
        x: 100,
        y: 0,
        target: 0,
        velocityY: 0,
        fly: false,
        angle: 0,
        falls: false,
        flashAnim: 0,
        flashReturn: false,
        kinematicAnim: 0,

        display() {
          p.push();
          p.translate(this.x, this.y);
          p.rotate(p.radians(this.angle));
          if (!mousePress || this.falls) {
            p.image(
              sprite_flappy,
              0,
              0,
              sprite_flappy.width * 1.5,
              sprite_flappy.height * 3,
              0,
              0,
              sprite_flappy.width / 2,
              sprite_flappy.height * 3
            );
          } else {
            p.image(
              sprite_flappy,
              0,
              0,
              sprite_flappy.width * 1.5,
              sprite_flappy.height * 3,
              sprite_flappy.width / 2,
              0,
              sprite_flappy.width / 2,
              sprite_flappy.height * 3
            );
          }
          p.pop();
        },

        update() {
          if (this.falls) {
            if (this.flashAnim > 255) {
              this.flashReturn = true;
            }

            if (this.flashReturn) {
              this.flashAnim -= 60;
            } else {
              this.flashAnim += 60;
            }

            if (this.flashReturn && this.flashAnim === 0) {
              gameover = true;
              menu_gameover.easein();
              try {
                sound_die.play();
              } catch (e) {}

              if (score > hightscore) {
                hightscore = score;
              }
            }

            this.y += this.velocityY;
            this.velocityY += 0.4;
            this.angle += 4;

            if (speed > 0) {
              speed = 0;
            }

            if (this.angle > 90) {
              this.angle = 90;
            }
          } else {
            this.y += this.velocityY;
            this.angle += 2.5;

            if (this.angle > 90) {
              this.angle = 90;
            }

            if (mousePressEvent || (keyPressEvent && p.key === " ")) {
              try {
                sound_wing.play();
              } catch (e) {}

              this.velocityY = 0;
              this.fly = true;
              this.target = clamp(this.y - 60, -19, p.height);
              this.angle = -45;
            }

            if (this.y < this.target) {
              this.fly = false;
              this.target = 10000;
            }

            if (!this.fly) {
              this.velocityY += 0.4;
            } else {
              this.y -= 5;
            }

            if (this.y > p.height - 49) {
              if (!this.falls) {
                try {
                  sound_hit.play();
                } catch (e) {}
              }
              this.falls = true;
            }
          }
          this.y = clamp(this.y, -20, p.height - 50);
        },

        kinematicMove() {
          if (gameover) {
            this.x = p.width / 2;
            this.y = p.height / 2;
            gameover = false;
            score = 0;
            gap = 90;
          }

          this.y = p.height / 2 + p.map(p.sin(p.frameCount * 0.1), 0, 1, -2, 2);

          p.push();
          p.translate(this.x, this.y);
          p.image(
            sprite_flappy,
            0,
            0,
            sprite_flappy.width * 1.5,
            sprite_flappy.height * 3,
            0,
            0,
            sprite_flappy.width / 2,
            sprite_flappy.height * 3
          );
          p.pop();
        },
      };

      class Pipe {
        constructor() {
          this.gapSize = gap;
          this.y = p.random(150, p.height - 150);
          this.x = p.width + 50;
          this.potential = true;
        }

        display() {
          p.push();
          p.translate(
            this.x,
            this.y + this.gapSize + sprite_pipe.height / 2 / 2
          );
          p.image(
            sprite_pipe,
            0,
            0,
            sprite_pipe.width / 2,
            sprite_pipe.height / 2
          );
          p.pop();

          p.push();
          p.translate(
            this.x,
            this.y - this.gapSize - sprite_pipe.height / 2 / 2
          );
          p.rotate(p.radians(180));
          p.scale(-1, 1);
          p.image(
            sprite_pipe,
            0,
            0,
            sprite_pipe.width / 2,
            sprite_pipe.height / 2
          );
          p.pop();

          if (
            this.potential &&
            flappy_bird.x > this.x - 25 &&
            flappy_bird.x < this.x + 25
          ) {
            score++;
            try {
              sound_point.play();
            } catch (e) {}
            if (gap > 60) {
              gap--;
            }
            this.potential = false;
          }

          // Collision detection
          if (
            (flappy_bird.x + 20 > this.x - 25 &&
              flappy_bird.x - 20 < this.x + 25 &&
              flappy_bird.y + 20 >
                this.y - this.gapSize - sprite_pipe.height / 2 / 2 - 200 &&
              flappy_bird.y - 20 <
                this.y - this.gapSize - sprite_pipe.height / 2 / 2 + 200) ||
            (flappy_bird.x + 20 > this.x - 25 &&
              flappy_bird.x - 20 < this.x + 25 &&
              flappy_bird.y + 20 >
                this.y + this.gapSize + sprite_pipe.height / 2 / 2 - 200 &&
              flappy_bird.y - 20 <
                this.y + this.gapSize + sprite_pipe.height / 2 / 2 + 200)
          ) {
            if (!flappy_bird.falls) {
              try {
                sound_hit.play();
              } catch (e) {}
            }
            flappy_bird.falls = true;
          }
        }

        update() {
          this.x -= speed;
        }
      }

      function page_game() {
        overflowX += speed;
        if (overflowX > sprite_city.width / 2) {
          overflowX = 0;
        }

        p.image(
          sprite_city,
          sprite_city.width / 2 / 2,
          p.height - sprite_city.height / 2 / 2 - 40,
          sprite_city.width / 2,
          sprite_city.height / 2
        );

        if (!flappy_bird.falls && p.frameCount % 70 === 0) {
          pipes.push(new Pipe());
        }

        for (let i = pipes.length - 1; i >= 0; i--) {
          if (pipes[i].x < -50) {
            pipes.splice(i, 1);
            continue;
          }
          pipes[i].display();
          pipes[i].update();
        }

        p.image(
          sprite_floor,
          sprite_floor.width - overflowX,
          p.height - sprite_floor.height,
          sprite_floor.width * 2,
          sprite_floor.height * 2
        );

        flappy_bird.display();
        flappy_bird.update();
        flappy_bird.x = smoothMove(flappy_bird.x, 90, 0.02);

        if (!gameover) {
          p.push();
          p.stroke(0);
          p.strokeWeight(5);
          p.fill(255);
          p.textSize(30);
          p.text(score, p.width / 2, 50);
          p.pop();
        }

        p.push();
        p.noStroke();
        p.fill(255, flappy_bird.flashAnim);
        p.rect(p.width / 2, p.height / 2, p.width, p.height);
        p.pop();

        if (gameover) {
          menu_gameover.display();
          menu_gameover.update();
        }
      }

      function page_menu() {
        speed = 1;
        overflowX += speed;
        if (overflowX > sprite_city.width / 2) {
          overflowX = 0;
        }

        p.image(
          sprite_city,
          sprite_city.width / 2 / 2,
          p.height - sprite_city.height / 2 / 2 - 40,
          sprite_city.width / 2,
          sprite_city.height / 2
        );

        p.image(
          sprite_floor,
          sprite_floor.width - overflowX,
          p.height - sprite_floor.height,
          sprite_floor.width * 2,
          sprite_floor.height * 2
        );

        p.image(
          sprite_title,
          p.width / 2,
          100,
          sprite_title.width / 4,
          sprite_title.height / 4
        );

        flappy_bird.kinematicMove();

        p.push();
        p.fill(230, 97, 29);
        p.stroke(255);
        p.strokeWeight(3);
        p.text("Tap to play", p.width / 2, p.height / 2 - 50);
        p.pop();

        if (mousePressEvent || (keyPressEvent && p.key === " ")) {
          page = "GAME";
          resetGame();

          flappy_bird.velocityY = 0;
          flappy_bird.fly = true;
          flappy_bird.target = clamp(flappy_bird.y - 60, -19, p.height);
          flappy_bird.angle = -45;
          flappy_bird.update();
        }
        flappy_bird.x = p.width / 2;
      }

      p.preload = () => {
        const assetsPath = "src/assets";

        sprite_flappy = p.loadImage(`${assetsPath}/flappybird.png`);
        sprite_pipe = p.loadImage(`${assetsPath}/pipe.png`);
        sprite_city = p.loadImage(`${assetsPath}/city.png`);
        sprite_floor = p.loadImage(`${assetsPath}/floor.png`);
        sprite_title = p.loadImage(`${assetsPath}/title.png`);

        try {
          sound_point = p.loadSound(`${assetsPath}/sfx_point.wav`);
          sound_hit = p.loadSound(`${assetsPath}/sfx_hit.wav`);
          sound_die = p.loadSound(`${assetsPath}/sfx_die.wav`);
          sound_wing = p.loadSound(`${assetsPath}/sfx_wing.wav`);
          sound_sweetwing = p.loadSound(`${assetsPath}/sfx_swooshing.wav`);
        } catch (e) {
          console.warn("Sound loading failed:", e);
          const dummySound = { play: () => {} };
          sound_point =
            sound_hit =
            sound_die =
            sound_wing =
            sound_sweetwing =
              dummySound;
        }

        try {
          font_flappy = p.loadFont(`${assetsPath}/flappy-font.ttf`);
        } catch (e) {
          console.warn("Font loading failed:", e);
        }
      };

      p.setup = () => {
        const canvas = p.createCanvas(400, 400);
        canvas.parent(gameContainer);

        p.imageMode(p.CENTER);
        p.rectMode(p.CENTER);
        p.ellipseMode(p.CENTER);
        p.textAlign(p.CENTER, p.CENTER);
        p.noSmooth();

        try {
          p.textFont(font_flappy);
        } catch (e) {}

        flappy_bird.y = p.height / 2;
      };

      p.draw = () => {
        p.background(123, 196, 208);

        switch (page) {
          case "GAME":
            page_game();
            break;
          case "MENU":
            page_menu();
            break;
        }

        // Reset events
        mousePressEvent = false;
        mouseReleaseEvent = false;
        keyPressEvent = false;
        keyReleaseEvent = false;
      };

      // Event handlers
      p.mousePressed = () => {
        mousePress = true;
        mousePressEvent = true;
      };

      p.mouseReleased = () => {
        mousePress = false;
        mouseReleaseEvent = true;
      };

      p.keyPressed = () => {
        keyPress = true;
        keyPressEvent = true;
      };

      p.keyReleased = () => {
        keyPress = false;
        keyReleaseEvent = true;
      };
    };

    // Create new p5 instance
    p5Instance = new p5(sketch);
  });

  onDestroy(() => {
    if (p5Instance) {
      p5Instance.remove();
    }
  });
</script>

<div
  class="fixed inset-0 z-50 flex items-center justify-center transition-opacity"
  class:opacity-0={!isUploading}
  class:pointer-events-none={!isUploading}
>
  <div class="bg-grey-800 p-4 rounded-lg shadow-lg">
    <div class="text-center mb-4">
      <h3 class="text-lg font-bold">Uploading... {progress}%</h3>
      <p class="text-sm text-gray-600">Play while you wait!</p>
    </div>
    <div bind:this={gameContainer} class="w-[400px] h-[400px]" />
  </div>
</div>

