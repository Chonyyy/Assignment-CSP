# Assignment-CSP

Uno de los problemas de optimización combinatoria más conocidos es el problema de asignación. Por ejemplo, supongamos que un grupo de trabajadores necesita realizar un conjunto de tareas y que hay un costo por asignar el trabajador a cada tarea. El problema es asignar a cada trabajador como máximo una tarea, sin que dos trabajadores realicen la misma tarea, y, al mismo tiempo, se minimiza el costo total.

## Soluciones Propuestas

### Modelo MIP (Mixed Integer Programming)

El primer enfoque utiliza un modelo de Programación Entera Mixta (MIP) para resolver el problema. Este modelo permite representar de manera precisa las restricciones del problema de asignación y optimizar el costo total de las asignaciones utilizando la biblioteca OR-Tools de Google.

#### Implementación

La clase `AssignmentProblem` define el modelo MIP, incluyendo la definición de variables, restricciones y la función objetivo. Se utiliza el solver SCIP a través de la API de OR-Tools para encontrar la solución óptima o factible al problema.

#### Ejemplo de Uso

El script `Solución_MIP.py` proporciona un ejemplo de cómo instanciar el problema, definir el modelo, añadir restricciones y resolverlo. La solución encontrada muestra qué trabajador se asigna a qué tarea y cuál es el costo total mínimo.

### Modelo CP-SAT (Constraint Programming SAT)

El segundo enfoque emplea la Satisfacción de Restricciones (CP) con soporte para SAT (Satisfiability) para modelar y resolver el problema de asignación. Este método es útil cuando se busca una solución que cumpla con todas las restricciones dadas, permitiendo una representación más flexible de las mismas.

#### Implementación

Similar al modelo MIP, la clase `AssignmentProblem` define el modelo de CP-SAT. Sin embargo, en este caso, se utilizan variables booleanas y restricciones específicas de CP para modelar el problema. La resolución se realiza mediante el solver de CP-SAT de OR-Tools.

#### Ejemplo de Uso

El script `Solución_CP_SAT.py` demuestra cómo instanciar el problema de asignación, definir el modelo de CP-SAT, añadir restricciones y resolverlo. Al igual que con el modelo MIP, se muestra la asignación de trabajadores a tareas y el costo total mínimo encontrado.

## Conclusión

Ambos modelos ofrecen soluciones efectivas para el problema de asignación, con diferencias en su enfoque y eficiencia dependiendo de las características específicas del problema y los datos disponibles. La elección entre uno u otro puede depender de preferencias personales, requisitos de rendimiento y complejidad del problema.