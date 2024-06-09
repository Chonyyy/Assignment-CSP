import io
import pandas as pd
from ortools.sat.python import cp_model
from collections import namedtuple

# Definición de la estructura de datos para una asignación
Assignment = namedtuple('Assignment', ['worker', 'task', 'cost'])

class AssignmentProblem:
    def __init__(self, data_str):
        self.data_str = data_str
        self.assignments = self.read_data()
        self.model = cp_model.CpModel()
        self.variables = {}

    def read_data(self):
        """Lee los datos de entrada y los convierte en una lista de asignaciones."""
        data = pd.read_table(io.StringIO(self.data_str), sep=r"\s+")
        return [Assignment(row.worker, row.task, row.cost) for row in data.itertuples()]

    def create_model(self):
        """Crea el modelo de optimización y define variables y restricciones."""
        # Crear variables para cada posible asignación
        self.variables = {i: self.model.NewBoolVar(f"x_{assignment.worker}_{assignment.task}")
                          for i, assignment in enumerate(self.assignments)}

        # Restricción: Cada trabajador se asigna a lo sumo a una tarea
        workers = set(a.worker for a in self.assignments)
        for worker in workers:
            self.model.AddAtMostOne(self.variables[i] for i, a in enumerate(self.assignments) if a.worker == worker)

        # Restricción: Cada tarea se asigna exactamente a un trabajador
        tasks = set(a.task for a in self.assignments)
        for task in tasks:
            self.model.AddExactlyOne(self.variables[i] for i, a in enumerate(self.assignments) if a.task == task)

        # Función objetivo: Minimizar el costo total de las asignaciones
        self.model.Minimize(sum(a.cost * self.variables[i] for i, a in enumerate(self.assignments)))

    def solve_model(self):
        """Resuelve el modelo y maneja el resultado."""
        solver = cp_model.CpSolver()
        status = solver.Solve(self.model)

        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            print(f"Total cost = {solver.ObjectiveValue()}\n")
            for i, var in self.variables.items():
                if solver.BooleanValue(var):
                    assignment = self.assignments[i]
                    print(f"{assignment.task} assigned to {assignment.worker} with a cost of {assignment.cost}")
        elif status == cp_model.INFEASIBLE:
            print("No solution found")
        else:
            print("Something went wrong, check the status and the log of the solve")

    def solve(self):
        """Método principal para resolver el problema."""
        self.create_model()
        self.solve_model()

def main():
    data_str = """
    worker  task  cost
        w1    t1    90
        w1    t2    80
        w1    t3    75
        w1    t4    70
        w2    t1    35
        w2    t2    85
        w2    t3    55
        w2    t4    65
        w3    t1   125
        w3    t2    95
        w3    t3    90
        w3    t4    95
        w4    t1    45
        w4    t2   110
        w4    t3    95
        w4    t4   115
        w5    t1    50
        w5    t2   110
        w5    t3    90
        w5    t4   100
    """
    
    problem = AssignmentProblem(data_str)
    problem.solve()

if __name__ == "__main__":
    main()
