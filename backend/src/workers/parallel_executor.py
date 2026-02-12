"""
Phase 5: Parallel Execution Manager
Enables supervised parallel execution for multiple agents.
"""

from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
import asyncio
import logging

logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class TaskDependency:
    """Represents a dependency between tasks."""

    task_id: str
    depends_on: str
    dependency_type: str = "file"  # file, agent, resource


@dataclass
class Task:
    """Represents an executable task."""

    id: str
    agent_id: str
    description: str
    input_data: Dict[str, Any]
    dependencies: List[TaskDependency] = field(default_factory=list)
    priority: int = 0
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[Any] = None
    error: Optional[str] = None


@dataclass
class Conflict:
    """Represents a conflict between tasks."""

    task_a: str
    task_b: str
    resource: str
    conflict_type: str
    severity: str = "high"  # low, medium, high, critical


class DependencyResolver:
    """Maps and resolves task dependencies."""

    def __init__(self):
        self.dependency_graph: Dict[str, Set[str]] = {}
        self.resource_map: Dict[str, Set[str]] = {}

    def add_task(self, task: Task) -> None:
        """Add a task to the dependency graph."""
        self.dependency_graph[task.id] = set()
        for dep in task.dependencies:
            if task.id not in self.dependency_graph:
                self.dependency_graph[task.id] = set()
            self.dependency_graph[task.id].add(dep.depends_on)

            # Map resource dependencies
            if dep.dependency_type == "file":
                if dep.depends_on not in self.resource_map:
                    self.resource_map[dep.depends_on] = set()
                self.resource_map[dep.depends_on].add(task.id)

    def get_executable_tasks(self, completed_tasks: Set[str]) -> List[Task]:
        """Get tasks that have all dependencies satisfied."""
        executable = []
        for task_id, dependencies in self.dependency_graph.items():
            if dependencies.issubset(completed_tasks):
                executable.append(task_id)
        return executable

    def detect_conflicts(self, tasks: List[Task]) -> List[Conflict]:
        """Detect potential conflicts between tasks."""
        conflicts = []
        task_resources: Dict[str, Set[str]] = {}

        for task in tasks:
            task_resources[task.id] = set()
            for dep in task.dependencies:
                if dep.dependency_type == "file":
                    task_resources[task.id].add(dep.depends_on)

        # Check for resource conflicts
        for resource, tasks_using in self.resource_map.items():
            if len(tasks_using) > 1:
                task_list = list(tasks_using)
                for i in range(len(task_list)):
                    for j in range(i + 1, len(task_list)):
                        conflicts.append(
                            Conflict(
                                task_a=task_list[i],
                                task_b=task_list[j],
                                resource=resource,
                                conflict_type="file_access",
                                severity="high",
                            )
                        )

        return conflicts


class ParallelExecutor:
    """Manages parallel execution of agent tasks."""

    def __init__(self, max_parallel: int = 3):
        self.max_parallel = max_parallel
        self.dependency_resolver = DependencyResolver()
        self.task_queue: List[Task] = []
        self.active_tasks: Dict[str, Task] = {}
        self.completed_tasks: Dict[str, Task] = {}
        self.execution_semaphore = asyncio.Semaphore(max_parallel)

    async def submit_task(self, task: Task) -> None:
        """Submit a task for execution."""
        self.dependency_resolver.add_task(task)
        self.task_queue.append(task)

    async def execute_task(self, task: Task) -> Task:
        """Execute a single task with semaphore control."""
        async with self.execution_semaphore:
            task.status = TaskStatus.RUNNING
            self.active_tasks[task.id] = task

            logger.info(f"Executing task {task.id} with agent {task.agent_id}")

            # Simulate task execution
            # In production, this would call the actual agent
            await asyncio.sleep(0.1)

            task.status = TaskStatus.COMPLETED
            del self.active_tasks[task.id]
            self.completed_tasks[task.id] = task

            logger.info(f"Completed task {task.id}")
            return task

    async def run(self) -> Dict[str, Task]:
        """Execute all tasks with parallel execution."""
        completed = set()

        while self.task_queue or self.active_tasks:
            # Get executable tasks
            executable_ids = self.dependency_resolver.get_executable_tasks(completed)
            executable_tasks = [
                t
                for t in self.task_queue
                if t.id in executable_ids and t.status == TaskStatus.PENDING
            ]

            # Execute in parallel
            if executable_tasks and len(self.active_tasks) < self.max_parallel:
                for task in executable_tasks[
                    : self.max_parallel - len(self.active_tasks)
                ]:
                    asyncio.create_task(self.execute_task(task))

            # Wait for tasks to complete
            await asyncio.sleep(0.01)

            # Update completed set
            completed = set(self.completed_tasks.keys())

        return self.completed_tasks

    def get_status(self) -> Dict[str, Any]:
        """Get current execution status."""
        return {
            "queue_size": len(self.task_queue),
            "active_tasks": len(self.active_tasks),
            "completed_tasks": len(self.completed_tasks),
            "max_parallel": self.max_parallel,
        }


# Phase 5 Status
PARALLEL_EXECUTION_READY = True
DEPENDENCY_RESOLUTION_ENABLED = True
CONFLICT_DETECTION_ENABLED = True
