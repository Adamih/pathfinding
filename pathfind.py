import maze as m
import draw as d
import math

from typing import List, Tuple


def h(n, end) -> List[int]:
    return math.pow(end[0] - n[0], 2) + math.pow(end[1] - n[1], 2)



def A_star(board: m.CellGrid, start: Tuple[int], end: Tuple[int], max_distance=math.inf) -> m.CellGrid:
    nboard = board.clone()
    nboard.clear_dist(math.inf)

    # mark the start and end for the UI
    nboard.at(start).mark = m.CellMark.Start
    nboard.at(end).mark = m.CellMark.End

    # Set start
    nboard.at(start).dist = 0
    nboard.at(start).score = h(start, end)
    open_list = [start]

    while open_list:
        # Pop and update current pos
        open_list.sort(key=lambda x: nboard.at(x).score, reverse=True)
        cur_pos = open_list.pop()
        cur_cell = nboard.at(cur_pos)
        cur_cell.mark = m.CellMark.Current

        # (x,y) offsets from current cell
        neighbours = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        for neighbour in neighbours:
            ncell_pos = m.add_point(cur_pos, neighbour)
            if not nboard.is_valid_point(ncell_pos):
                continue  # Out of bounds

            cell = nboard.at(ncell_pos)

            if cell.type != m.CellType.Empty:
                continue  # Not valid walk square
            
            dist = cur_cell.dist + 1
            if cell.dist > dist:
                cell.dist = dist
                cell.score = dist + h(ncell_pos, end)
                cell.path_from = cur_cell  # Add return path
                open_list.append(ncell_pos)
                cell.mark = m.CellMark.Neighbour
        yield nboard
        cur_cell.mark = m.CellMark.No


def backtrack_to_start(board: m.CellGrid, end: Tuple[int]) -> List[m.Cell]:
    """ Returns the path to the end, assuming the board has been filled in via fill_shortest_path """
    cell = board.at(end)
    path = []
    while cell != None:
        path.append(cell)
        cell = cell.path_from
    return path


class MyFinder(d.Finder):
    """Integrate into the simple UI	"""
    
    def __init__(self):
        self.reset()

    def step(self, _):
        self.result = next(self.path_gen)
        self.set_board(self.result)
        self.set_path(backtrack_to_start(self.result, self.game.end))

    def reset(self):
        self.game = m.create_wall_maze(20, 12)
        self.path_gen = A_star(self.game.board, self.game.start, self.game.end)
        self.max_distance = 18
        self.step(None)

header_text = """Keys:
	Left - Lower maximum distance
	Right - Increase maximum distance
	R - create a new maze
	Esc - Exit"""
print( header_text )

finder = MyFinder()
finder.run()
