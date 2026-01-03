/** Home page component containing the main To-Do list. */
import { useEffect, useState } from "react";
import { Todo, TodoCreate, TodoUpdate } from "../types";
import { TodoApiService } from "../services/api";
import { TodoItem } from "../components/TodoItem";
import { TodoForm } from "../components/TodoForm";

/**
 * Home page component that displays and manages the To-Do list.
 * Handles all CRUD operations through the API service.
 */
export function Home() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  /**
   * Load todos from the server on component mount.
   */
  useEffect(() => {
    loadTodos();
  }, []);

  /**
   * Fetch all todos from the API.
   */
  const loadTodos = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await TodoApiService.getAllTodos();
      setTodos(data);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to load todos";
      setError(message);
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Create a new todo item.
   */
  const handleCreate = async (data: TodoCreate): Promise<Todo> => {
    const newTodo = await TodoApiService.createTodo(data);
    setTodos((prev) => [newTodo, ...prev]);
    return newTodo;
  };

  /**
   * Update an existing todo item.
   */
  const handleUpdate = async (id: string, data: TodoUpdate) => {
    const updatedTodo = await TodoApiService.updateTodo(id, data);
    setTodos((prev) =>
      prev.map((todo) => (todo.id === id ? updatedTodo : todo))
    );
  };

  /**
   * Delete a todo item.
   */
  const handleDelete = async (id: string) => {
    if (window.confirm("Are you sure you want to delete this task?")) {
      await TodoApiService.deleteTodo(id);
      setTodos((prev) => prev.filter((todo) => todo.id !== id));
    }
  };

  /**
   * Mark a todo item as completed.
   */
  const handleComplete = async (id: string) => {
    const updatedTodo = await TodoApiService.markCompleted(id);
    setTodos((prev) =>
      prev.map((todo) => (todo.id === id ? updatedTodo : todo))
    );
  };

  /**
   * Mark a todo item as failed.
   */
  const handleFail = async (id: string) => {
    const updatedTodo = await TodoApiService.markFailed(id);
    setTodos((prev) =>
      prev.map((todo) => (todo.id === id ? updatedTodo : todo))
    );
  };

  /**
   * Filter todos by status for display.
   */
  const pendingTodos = todos.filter((todo) => todo.status === "pending");
  const completedTodos = todos.filter((todo) => todo.status === "completed");
  const failedTodos = todos.filter((todo) => todo.status === "failed");

  return (
    <div className="home">
      <header className="app-header">
        <h1>To-Do App</h1>
        <p className="app-subtitle">Organize your tasks efficiently</p>
      </header>

      <main className="app-main">
        {/* Error message */}
        {error && (
          <div className="error-message">
            <span>{error}</span>
            <button onClick={loadTodos}>Retry</button>
          </div>
        )}

        {/* Create form */}
        <section className="create-section">
          <TodoForm onCreate={handleCreate} />
        </section>

        {/* Loading state */}
        {isLoading && (
          <div className="loading">
            <p>Loading your tasks...</p>
          </div>
        )}

        {/* Todo lists */}
        {!isLoading && !error && (
          <div className="todo-lists">
            {/* Pending todos */}
            {pendingTodos.length > 0 && (
              <section className="todo-section">
                <h2>
                  Pending ({pendingTodos.length})
                </h2>
                <div className="todo-list">
                  {pendingTodos.map((todo) => (
                    <TodoItem
                      key={todo.id}
                      todo={todo}
                      onUpdate={handleUpdate}
                      onDelete={handleDelete}
                      onComplete={handleComplete}
                      onFail={handleFail}
                    />
                  ))}
                </div>
              </section>
            )}

            {/* Completed todos */}
            {completedTodos.length > 0 && (
              <section className="todo-section completed">
                <h2>
                  Completed ({completedTodos.length})
                </h2>
                <div className="todo-list">
                  {completedTodos.map((todo) => (
                    <TodoItem
                      key={todo.id}
                      todo={todo}
                      onUpdate={handleUpdate}
                      onDelete={handleDelete}
                      onComplete={handleComplete}
                      onFail={handleFail}
                    />
                  ))}
                </div>
              </section>
            )}

            {/* Failed todos */}
            {failedTodos.length > 0 && (
              <section className="todo-section failed">
                <h2>
                  Failed ({failedTodos.length})
                </h2>
                <div className="todo-list">
                  {failedTodos.map((todo) => (
                    <TodoItem
                      key={todo.id}
                      todo={todo}
                      onUpdate={handleUpdate}
                      onDelete={handleDelete}
                      onComplete={handleComplete}
                      onFail={handleFail}
                    />
                  ))}
                </div>
              </section>
            )}

            {/* Empty state */}
            {todos.length === 0 && (
              <div className="empty-state">
                <p>No tasks yet. Add your first task above!</p>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}
