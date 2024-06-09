import io
import pandas as pd
from ortools.sat.python import cp_model
from collections import namedtuple

# Definición de la estructura de datos para una asignación
Assignment = namedtuple('Assignment', ['worker', 'task', 'cost'])

def read_data():
    """Lee los datos de entrada y los convierte en una lista de asignaciones."""
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
    data = pd.read_table(io.StringIO(data_str), sep=r"\s+")
    assignments = [Assignment(row.worker, row.task, row.cost) for row in data.itertuples()]
    return assignments

def create_model(assignments):
    """Crea el modelo de optimización y define variables y restricciones."""
    model = cp_model.CpModel()
    variables = {}

    # Crear variables para cada posible asignación
    for i, assignment in enumerate(assignments):
        variables[i] = model.NewBoolVar(f"x_{assignment.worker}_{assignment.task}")

    # Restricción: Cada trabajador se asigna a lo sumo a una tarea
    workers = set(a.worker for a in assignments)
    for worker in workers:
        model.AddAtMostOne(variables[i] for i, a in enumerate(assignments) if a.worker == worker)

    # Restricción: Cada tarea se asigna exactamente a un trabajador
    tasks = set(a.task for a in assignments)
    for task in tasks:
        model.AddExactlyOne(variables[i] for i, a in enumerate(assignments) if a.task == task)

    # Función objetivo: Minimizar el costo total de las asignaciones
    model.Minimize(sum(a.cost * variables[i] for i, a in enumerate(assignments)))

    return model, variables

def solve_model(model, variables, assignments):
    """Resuelve el modelo y maneja el resultado."""
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print(f"Total cost = {solver.ObjectiveValue()}\n")
        for i, var in variables.items():
            if solver.BooleanValue(var):
                assignment = assignments[i]
                print(f"{assignment.task} assigned to {assignment.worker} with a cost of {assignment.cost}")
    elif status == cp_model.INFEASIBLE:
        print("No solution found")
    else:
        print("Something went wrong, check the status and the log of the solve")

def main():
    assignments = read_data()
    model, variables = create_model(assignments)
    solve_model(model, variables, assignments)

if __name__ == "__main__":
    main()
