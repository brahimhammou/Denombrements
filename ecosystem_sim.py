"""
ecosystem_sim.py
================
Simulation d'un écosystème Proies / Prédateurs
Projet personnel réalisé en appliquant les concepts de la
certification "POO avec Python" (OpenClassrooms).

Concepts POO utilisés :
  - Classe de base  : Animal         (position, énergie, déplacement)
  - Sous-classe     : Proie          (fuite, pâturage, reproduction)
  - Sous-classe     : Predateur      (chasse, alimentation, reproduction)
  - Collections     : list[Animal]   gérée à chaque tick
  - Exceptions      : ImportError    pour tkinter optionnel

Dépendances : tkinter (stdlib Python >= 3.9)
Lancement   : python ecosystem_sim.py
"""

import tkinter as tk
import random
import math
from typing import Optional

# ── Constantes ──────────────────────────────────────────────────────
W, H           = 800, 500
FPS            = 30
INIT_PROIES    = 50
INIT_PRED      = 8
MAX_PROIES     = 200
MAX_PRED       = 30
PREY_COLOR     = "#4ade80"
PRED_COLOR     = "#f87171"
BG_COLOR       = "#1e1e2e"


# ── Classe de base ───────────────────────────────────────────────────
class Animal:
    """
    Représente un animal générique dans l'écosystème.
    Toutes les sous-classes héritent de cette base commune.
    """
    _next_id: int = 0

    def __init__(self, x: float, y: float, energy: float) -> None:
        Animal._next_id += 1
        self.id     = Animal._next_id
        self.x      = x
        self.y      = y
        self.vx     = random.uniform(-1.5, 1.5)
        self.vy     = random.uniform(-1.5, 1.5)
        self.energy = energy
        self.age    = 0
        self.alive  = True

    def se_deplacer(self) -> None:
        """Déplace l'animal et le fait rebondir sur les bords."""
        self.x += self.vx
        self.y += self.vy
        if not (0 < self.x < W):
            self.vx *= -1
            self.x = max(1.0, min(W - 1.0, self.x))
        if not (0 < self.y < H):
            self.vy *= -1
            self.y = max(1.0, min(H - 1.0, self.y))
        self.age += 1

    def distance_vers(self, autre: "Animal") -> float:
        return math.hypot(self.x - autre.x, self.y - autre.y)

    def est_vivant(self) -> bool:
        return self.alive and self.energy > 0

    def __repr__(self) -> str:
        return (f"<{self.__class__.__name__} id={self.id} "
                f"pos=({self.x:.1f},{self.y:.1f}) energie={self.energy:.1f}>")


# ── Sous-classe Proie ────────────────────────────────────────────────
class Proie(Animal):
    """
    Herbivore pacifique.
    Fuit les predateurs, mange l'herbe passivement, se reproduit.
    """
    VITESSE_MAX   = 2.8
    COUT_ENERGIE  = 0.40
    GAIN_HERBE    = 0.55
    ENERGIE_MAX   = 110.0
    ENERGIE_REPRO = 90.0
    PROBA_REPRO   = 0.002
    RAYON_FUITE   = 90.0

    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, energy=random.uniform(60, 90))

    def fuir(self, predateurs: list) -> None:
        """Force de repulsion vis-a-vis des predateurs proches."""
        fx = fy = 0.0
        for pred in predateurs:
            d = self.distance_vers(pred)
            if 0 < d < self.RAYON_FUITE:
                fx += (self.x - pred.x) / d * 2.5
                fy += (self.y - pred.y) / d * 2.5
        self.vx = self.vx * 0.88 + random.uniform(-0.5, 0.5) + fx * 0.35
        self.vy = self.vy * 0.88 + random.uniform(-0.5, 0.5) + fy * 0.35
        spd = math.hypot(self.vx, self.vy)
        if spd > self.VITESSE_MAX:
            self.vx = self.vx / spd * self.VITESSE_MAX
            self.vy = self.vy / spd * self.VITESSE_MAX

    def se_nourrir(self) -> None:
        self.energy = min(self.ENERGIE_MAX, self.energy + self.GAIN_HERBE)

    def peut_se_reproduire(self, population: int) -> bool:
        return (self.energy > self.ENERGIE_REPRO
                and random.random() < self.PROBA_REPRO
                and population < MAX_PROIES)

    def se_reproduire(self) -> "Proie":
        self.energy -= 30
        return Proie(self.x + random.uniform(-6, 6),
                     self.y + random.uniform(-6, 6))

    def tick(self, predateurs: list, population: int) -> "Optional[Proie]":
        self.energy -= self.COUT_ENERGIE
        self.fuir(predateurs)
        self.se_nourrir()
        self.se_deplacer()
        if not self.est_vivant():
            self.alive = False
            return None
        if self.peut_se_reproduire(population):
            return self.se_reproduire()
        return None


# ── Sous-classe Predateur ────────────────────────────────────────────
class Predateur(Animal):
    """
    Carnivore actif.
    Traque la proie la plus proche, mange en cas de contact, se reproduit.
    """
    VITESSE_MAX   = 3.2
    COUT_ENERGIE  = 0.65
    GAIN_CHASSE   = 65.0
    ENERGIE_REPRO = 190.0
    PROBA_REPRO   = 0.0008
    RAYON_MANGER  = 10.0

    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, energy=random.uniform(100, 150))

    def chasser(self, proies: list) -> "Optional[Proie]":
        """
        Oriente vers la proie la plus proche.
        Retourne la proie si attrapee (distance < RAYON_MANGER), sinon None.
        """
        if not proies:
            self.vx = self.vx * 0.9 + random.uniform(-0.4, 0.4)
            self.vy = self.vy * 0.9 + random.uniform(-0.4, 0.4)
            return None
        cible = min(proies, key=lambda p: self.distance_vers(p))
        d = self.distance_vers(cible)
        if d > 0:
            self.vx = self.vx * 0.82 + (cible.x - self.x) / d * 0.7
            self.vy = self.vy * 0.82 + (cible.y - self.y) / d * 0.7
        spd = math.hypot(self.vx, self.vy)
        if spd > self.VITESSE_MAX:
            self.vx = self.vx / spd * self.VITESSE_MAX
            self.vy = self.vy / spd * self.VITESSE_MAX
        if d < self.RAYON_MANGER:
            self.energy += self.GAIN_CHASSE
            cible.alive = False
            return cible
        return None

    def peut_se_reproduire(self, population: int) -> bool:
        return (self.energy > self.ENERGIE_REPRO
                and random.random() < self.PROBA_REPRO
                and population < MAX_PRED)

    def se_reproduire(self) -> "Predateur":
        self.energy -= 60
        return Predateur(self.x + random.uniform(-6, 6),
                         self.y + random.uniform(-6, 6))

    def tick(self, proies: list, population: int):
        self.energy -= self.COUT_ENERGIE
        mangee = self.chasser(proies)
        self.se_deplacer()
        if not self.est_vivant():
            self.alive = False
            return mangee, None
        bebe = self.se_reproduire() if self.peut_se_reproduire(population) else None
        return mangee, bebe


# ── Simulation tkinter ───────────────────────────────────────────────
class Simulation:
    """Orchestre la boucle de simulation et le rendu tkinter."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        root.title("Simulation Proies / Predateurs — ecosystem_sim.py")
        root.configure(bg=BG_COLOR)
        root.resizable(False, False)

        self.status_var = tk.StringVar()
        tk.Label(root, textvariable=self.status_var, bg="#252538",
                 fg="white", font=("Courier", 11, "bold"),
                 anchor="w", padx=10).pack(fill="x")

        self.canvas = tk.Canvas(root, width=W, height=H,
                                bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack()

        ctrl = tk.Frame(root, bg="#252538", pady=6)
        ctrl.pack(fill="x")
        self.btn_pause = tk.Button(
            ctrl, text="Pause", command=self._toggle_pause,
            bg="#4F46E5", fg="white", font=("Noto Sans", 10, "bold"),
            relief="flat", padx=14, pady=4, cursor="hand2")
        self.btn_pause.pack(side="left", padx=10)
        tk.Button(ctrl, text="Reset", command=self._reset,
                  bg="#374151", fg="white", font=("Noto Sans", 10, "bold"),
                  relief="flat", padx=14, pady=4, cursor="hand2").pack(side="left")

        self._init_animals()
        self.paused = False
        self._loop()

    def _init_animals(self) -> None:
        self.animals = (
            [Proie(random.random() * W, random.random() * H)
             for _ in range(INIT_PROIES)]
            + [Predateur(random.random() * W, random.random() * H)
               for _ in range(INIT_PRED)]
        )

    def _reset(self) -> None:
        self._init_animals()
        self.paused = False
        self.btn_pause.config(text="Pause", bg="#4F46E5")

    def _toggle_pause(self) -> None:
        self.paused = not self.paused
        self.btn_pause.config(
            text="Reprendre" if self.paused else "Pause",
            bg="#059669"     if self.paused else "#4F46E5")

    def _tick(self) -> None:
        proies     = [a for a in self.animals if isinstance(a, Proie)     and a.est_vivant()]
        predateurs = [a for a in self.animals if isinstance(a, Predateur) and a.est_vivant()]
        nouveaux   = []

        for p in proies:
            bebe = p.tick(predateurs, len(proies))
            if bebe:
                nouveaux.append(bebe)

        for pred in predateurs:
            _, bebe = pred.tick(proies, len(predateurs))
            if bebe:
                nouveaux.append(bebe)

        self.animals = [a for a in self.animals if a.est_vivant()] + nouveaux

        # Re-introduction si effondrement
        if sum(1 for a in self.animals if isinstance(a, Proie)) < 4:
            self.animals += [Proie(random.random() * W, random.random() * H)
                             for _ in range(12)]
        if sum(1 for a in self.animals if isinstance(a, Predateur)) < 2:
            self.animals.append(Predateur(random.random() * W, random.random() * H))

    def _draw(self) -> None:
        c = self.canvas
        c.delete("all")
        c.create_rectangle(0, 0, W, H, fill=BG_COLOR, outline="")
        for x in range(0, W, 20):
            c.create_line(x, 0, x, H, fill="#ffffff06")
        for y in range(0, H, 20):
            c.create_line(0, y, W, y, fill="#ffffff06")

        for a in self.animals:
            r   = 4 if isinstance(a, Proie) else 6
            col = PREY_COLOR if isinstance(a, Proie) else PRED_COLOR
            c.create_oval(a.x - r, a.y - r, a.x + r, a.y + r,
                          fill=col, outline=col, width=0)

        nb_p = sum(1 for a in self.animals if isinstance(a, Proie))
        nb_d = sum(1 for a in self.animals if isinstance(a, Predateur))
        c.create_text(10, 12, anchor="w", fill=PREY_COLOR,
                      font=("Courier", 11, "bold"), text=f"Proies      : {nb_p}")
        c.create_text(10, 30, anchor="w", fill=PRED_COLOR,
                      font=("Courier", 11, "bold"), text=f"Predateurs  : {nb_d}")
        self.status_var.set(
            f"  Proies: {nb_p}   Predateurs: {nb_d}   Total: {len(self.animals)}")

    def _loop(self) -> None:
        if not self.paused:
            self._tick()
        self._draw()
        self.root.after(1000 // FPS, self._loop)


# ── Point d'entree ───────────────────────────────────────────────────
if __name__ == "__main__":
    try:
        root = tk.Tk()
        Simulation(root)
        root.mainloop()
    except ImportError as e:
        print(f"[Erreur] Module manquant : {e}")
        print("tkinter est inclus dans Python standard (>= 3.9).")
