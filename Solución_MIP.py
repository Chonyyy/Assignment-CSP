from ortools.linear_solver import pywraplp

class AssignmentProblem:
    def __init__(self, costs):
        self.costs = costs
        self.num_workers = len(costs)
        self.num_tasks = len(costs[0])
        self.solver = pywraplp.Solver.CreateSolver("SCIP")
        if not self.solver:
            raise ValueError("No se pudo crear el solver.")
        self.x = {}

    def define_variables(self):
        """Define las variables de decisión."""
        self.x = {(i, j): self.solver.IntVar(0, 1, f"x_{i}_{j}")
                  for i in range(self.num_workers)
                  for j in range(self.num_tasks)}

    def add_constraints(self):
        """Añade las restricciones al modelo."""
        # Cada trabajador es asignado a lo sumo a una tarea.
        for i in range(self.num_workers):
            self.solver.Add(sum(self.x[i, j] for j in range(self.num_tasks)) <= 1)

        # Cada tarea es asignada exactamente a un trabajador.
        for j in range(self.num_tasks):
            self.solver.Add(sum(self.x[i, j] for i in range(self.num_workers)) == 1)

    def set_objective(self):
        """Define la función objetivo."""
        self.solver.Minimize(
            sum(self.costs[i][j] * self.x[i, j] for i in range(self.num_workers) for j in range(self.num_tasks))
        )

    def solve(self):
        """Resuelve el modelo e imprime la solución."""
        print(f"Solving with {self.solver.SolverVersion()}")
        status = self.solver.Solve()
        
        if status in (pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE):
            print(f"Total cost = {self.solver.Objective().Value()}\n")
            for i in range(self.num_workers):
                for j in range(self.num_tasks):
                    if self.x[i, j].solution_value() > 0.5:
                        print(f"Worker {i} assigned to task {j}. Cost: {self.costs[i][j]}")
        else:
            print("No solution found.")

def main():
    costs = [
        [90, 80, 75, 70],
        [35, 85, 55, 65],
        [125, 95, 90, 95],
        [45, 110, 95, 115],
        [50, 100, 90, 100],
    ]
    
    problem = AssignmentProblem(costs)
    problem.define_variables()
    problem.add_constraints()
    problem.set_objective()
    problem.solve()

if __name__ == "__main__":
    main()
