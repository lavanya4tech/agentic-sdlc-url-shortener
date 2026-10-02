from typing import Dict, List



from .task import Task



class DependencyGraph:



    """



    Represents the dependency graph for the SDLC workflow.



    Each task can depend on one or more upstream tasks.



    Tasks with satisfied dependencies can execute in parallel.



    """



    def __init__(self) -> None:



        self.tasks: Dict[str, Task] = {}



    def add_task(self, task: Task) -> None:



        if task.task_id in self.tasks:



            raise ValueError(f"Task already exists: {task.task_id}")



        self.tasks[task.task_id] = task



    def get_task(self, task_id: str) -> Task:



        if task_id not in self.tasks:



            raise KeyError(f"Task not found: {task_id}")



        return self.tasks[task_id]



    def get_ready_tasks(self, completed_tasks: set[str]) -> List[Task]:



        """



        Return tasks whose dependencies have all completed.



        """



        return [



            task



            for task in self.tasks.values()



            if task.status.value == "PENDING"



            and task.can_run(completed_tasks)



        ]



    def validate(self) -> None:



        """



        Validate that every declared dependency exists.



        """



        for task in self.tasks.values():



            for dependency in task.dependencies:



                if dependency not in self.tasks:



                    raise ValueError(



                        f"Task '{task.task_id}' depends on "



                        f"unknown task '{dependency}'"



                    )



    def get_all_tasks(self) -> List[Task]:



        return list(self.tasks.values())
