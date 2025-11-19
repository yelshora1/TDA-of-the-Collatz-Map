# collatz_ant_global_height.py

from typing import Tuple, Set, List

class CollatzAntGlobalHeight:
    def __init__(self, start_value: int):
        # ant state
        self.x = 0
        self.y = 0
        self.h = 0                   # global story height
        self.orientation = 0         # 0=up,1=right,2=down,3=left
        self.N = start_value         # current Collatz value
        
        # visited cells in the x-y plane
        self.visited: Set[Tuple[int, int]] = {(0, 0)}
        
        # record the path: list of (x, y, h, N)
        self.path: List[Tuple[int, int, int, int]] = [(0, 0, 0, self.N)]
        
        self.finished = False
    
    
    def step(self):
        """Perform one global-height Collatz step."""
        if self.finished:
            return None
        
        # STOP condition
        if self.N == 1:
            self.finished = True
            return None
        
        # 1. TURN based on parity of N
        if self.N % 2 == 0:
            # even -> turn right
            self.orientation = (self.orientation + 1) % 4
            new_N = self.N // 2
        else:
            # odd -> turn left
            self.orientation = (self.orientation - 1) % 4
            new_N = 3 * self.N + 1
        
        # 2. MOVE forward in the 2D plane
        if self.orientation == 0:      # up
            self.y += 1
        elif self.orientation == 1:    # right
            self.x += 1
        elif self.orientation == 2:    # down
            self.y -= 1
        else:                          # left
            self.x -= 1
        
        # 3. If revisiting any cell, increment global height
        pos = (self.x, self.y)
        if pos in self.visited:
            self.h += 1        # climb to a new story
        else:
            self.visited.add(pos)
        
        # 4. Update N to next Collatz value
        self.N = new_N
        
        # 5. Store path entry
        self.path.append((self.x, self.y, self.h, self.N))
        
        return (self.x, self.y, self.h, self.N)
    
    
    def run(self, max_steps=1_000_000):
        """Run until hitting 1 or max_steps."""
        for _ in range(max_steps):
            out = self.step()
            if out is None: break
        return self.path


if __name__ == "__main__":
    # Example usage: run the ant and export the recorded path
    ant = CollatzAntGlobalHeight(871)
    path = ant.run(10000)  # adjust steps as needed

    print("steps recorded:", len(path))
    print("last entries:", path[-10:])

    # Save path to CSV for downstream analysis
    import csv
    with open('points.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['x', 'y', 'h', 'N'])
        writer.writerows(path)
    print('Wrote points.csv')
