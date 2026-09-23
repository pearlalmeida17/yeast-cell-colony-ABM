from collections import defaultdict

class Lineage:
    def __init__(self):
        self.edges = defaultdict(list)
        self.next_subcolony_id = 0
        self.subcolony_of = {}

    def register_initial_cell(self, cell):
        if cell.subcolony_id is None:
            cell.subcolony_id = 0
        self.subcolony_of[cell.id] = cell.subcolony_id

    def update_ids(self, cell):
        if cell.parent_id == cell.founder_id:
            cell.subcolony_id = self.next_subcolony_id
            self.next_subcolony_id += 1
        else:
            cell.subcolony_id = self.subcolony_of.get(cell.parent_id, cell.subcolony_id)

        self.subcolony_of[cell.id] = cell.subcolony_id

        
    def add_edge(self, mother_id, daughter_id):
        self.edges[mother_id].append(daughter_id)

lineage = Lineage()