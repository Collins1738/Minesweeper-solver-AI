import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):
        mines = 14
        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

        self.mines = set()
        self.safes = set()
        self.unknown = set(cells)

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}, Mines = {self.mines}, Safes = {self.safes}, Unknown = {self.unknown}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        return self.mines

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        return self.safes

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.remove_unknown(cell)
            self.mines.add(cell)
        return

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.remove_unknown(cell)
            self.safes.add(cell)
        return

    def remove_unknown(self, cell):
        if cell in self.unknown:
            self.unknown.remove(cell)
        return

    def validate(self, model):
        temp_mine_count = len(self.mines)
        for node in model:
            if node.cell in self.unknown:
                if node.is_mine:
                    temp_mine_count+=1
                    # increase temp_mine_count
        # if temp_mine_count == self.count:
        #     print('validated set: {')
        #     for node in model:
        #         print(node)
        #     print("}")
        #     print(self.__str__)
        return temp_mine_count==self.count
        # a sentence can only validate a model if the model contains everything in the sentence

    # def validate_model(self, model): # a model is a set of UNKNOWN nodes
    #     temp_mines_length = len(self.mines)
    #     temp_safes_length = len(self.safes)
    #     temp_cells_length
    #     temp_unknown_length
    #     temp_unknown = set(self.unknown)
    #     temp_models = 

    #     for cell in temp_unknown:
    #         if node.cell in self.unknown:
    #             if node.is_mine:
    #                 temp_mines_length +=1
    #     if self.unk




class Node():
    def __init__(self, cell, is_mine):
        self.cell = cell
        self.is_mine = is_mine

    def __str__(self):
        return f"{self.cell} = {self.is_mine}"

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # keep track of cells that have not been played
        self.unplayed_cells = list(self.get_all_cells())
        
        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

        self.temp_possibility = [] #list of sets of different unplayed cells combinations/models (nodes)

    def get_all_cells(self):
        my_list = []
        for i in range(self.height):
            for j in range(self.width):
                my_list.append((i, j))
        return my_list


    def recurse(self, symbols, my_set = set(), index = 0):
        if index<len(symbols):
            node = Node(symbols[index], True)
            temp_set = set(my_set)
            temp_set.add(node)
            self.recurse(symbols, temp_set, index+1)
            node = Node(symbols[index], False)
            temp_set = set(my_set)
            temp_set.add(node)
            self.recurse(symbols, temp_set, index+1)
        else:
            self.temp_possibility.append(my_set)
        return

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        print("marking mine: ", cell)
        self.mines.add(cell)
        # print(self.unplayed_cells)
        # print(cell)
        if cell in self.unplayed_cells:
            self.unplayed_cells.remove(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        # print("marking safe: ", cell)
        self.safes.add(cell)
        if cell in self.unplayed_cells:
            self.unplayed_cells.remove(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        # 1
        self.moves_made.add(cell)
        # print(cell)
        # print(self.unplayed_cells)
        # self.unplayed_cells.remove(cell)
        # 2
        self.mark_safe(cell)
        # self.safes.add(cell)
        # 3
        surrounding_cells = self.get_surrounding_cells(cell)
        # filtered_cells = self.remove_played_cells(surrounding_cells)
        new_setence = Sentence(surrounding_cells, count)
        self.fix_sentence(new_setence)
        self.knowledge.append(new_setence)
        # 4
        self.update_knowledge()
        # 5
        return

    def fix_sentence(self, sentence):
        temp_unknown = set(sentence.unknown)
        for cell in temp_unknown:
            if cell in self.mines:
                sentence.mark_mine(cell)
            elif cell in self.safes:
                sentence.mark_safe(cell)
        return

    def update_knowledge(self):
        should_recurse = False
        for sentence in self.knowledge:
            if (len(sentence.unknown)+len(sentence.mines) == sentence.count) and sentence.count!=0:
                temp_unknown = set(sentence.unknown)
                for cell in temp_unknown:
                    self.mark_mine(cell)
                    should_recurse = True
                if should_recurse:
                    self.update_knowledge()
                    return
            if len(sentence.known_mines()) == sentence.count:
                # print(sentence)
                temp_unknown = set(sentence.unknown)
                for cell in temp_unknown:
                    # print("marking safe: ", cell)
                    self.mark_safe(cell)
                    should_recurse = True
                if should_recurse:
                    self.update_knowledge()
                    return
        return


    def query(self, cell):
        symbols = []
        knowledge_to_check = []
        for sentence in self.knowledge:
            if cell in sentence.unknown:
                # blah blah
                # add to sentence being checked
                symbols.extend(list(sentence.unknown))
                knowledge_to_check.append(sentence)
        self.temp_possibility.clear()
        self.recurse(symbols)
        good_models = []
        for model in self.temp_possibility:
            all_sentence_validated = True
            for sentence in knowledge_to_check:
                if sentence.validate(model):
                    continue
                else:
                    all_sentence_validated = False
            if all_sentence_validated:
                good_models.append(model)
        dictt =  {}
        unknown = set()
        for model in good_models:
            for node in model:
                if node.cell in unknown:
                    continue
                elif node.cell in dictt.keys():
                    if node.is_mine!= dictt[node.cell]:
                        del dictt[node.cell]
                        unknown.add(node.cell)
                else:
                    dictt[node.cell] = node.is_mine
        return dictt

    def remove_played_cells(self, cells):
        temp_cells = set(cells)
        for i in cells:
            if i in self.moves_made:
                temp_cells.remove(i)
        return temp_cells

    def get_surrounding_cells(self, cell):
        surrounding_cells = set()
        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the cell itself
                if (i, j) == cell:
                    continue
                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    surrounding_cells.add((i, j))
        return surrounding_cells

    def make_safe_move(self, called=False):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for move in self.safes:
            if move not in self.moves_made:
                return move
        print("No safe move bruh")
        if not called:
            self.run_this()
            return self.make_safe_move(True)
        return None

    def run_this(self):
        # get all the symbols you want to query
        # query each one
        for unknown_move in self.unplayed_cells:
            print("querying: ", unknown_move)
            dictt = self.query(unknown_move)
            print("Query result: ", dictt)
            if len(dictt.keys())>0:
                break

        for cell in dictt.keys():
            if dictt[cell]:
                self.mark_mine(cell)
            else:
                self.mark_safe(cell)
        self.update_knowledge()
        return

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        i = random.randrange(self.height)
        j = random.randrange(self.width)
        if ((i, j) in self.mines) or ((i, j) in self.moves_made):
            return self.make_random_move()
        return (i, j)


# a = MinesweeperAI()
# # print(a.get_all_cells())
# a.recurse()
# # print(a.temp_possibility)
# for mset in a.temp_possibility:
#     print("set: {")
#     for node in mset:
#         print(node)
#     print("}")