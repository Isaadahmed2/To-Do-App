/** TypeScript type definitions for To-Do app. */

/**
 * Priority levels for To-Do items.
 */
export type Priority = "low" | "medium" | "high";

/**
 * Status options for To-Do items.
 */
export type TodoStatus = "pending" | "completed" | "failed";

/**
 * Data model for a To-Do item.
 */
export interface Todo {
  id: string;
  title: string;
  description: string | null;
  priority: Priority;
  status: TodoStatus;
  created_at: string;
  updated_at: string;
}

/**
 * Data for creating a new To-Do item.
 */
export interface TodoCreate {
  title: string;
  description?: string | null;
  priority: Priority;
}

/**
 * Data for updating an existing To-Do item.
 */
export interface TodoUpdate {
  title?: string;
  description?: string | null;
  priority?: Priority;
  status?: TodoStatus;
}

/**
 * Priority badge color mapping for UI display.
 */
export const priorityColors: Record<Priority, string> = {
  low: "#22c55e",
  medium: "#f59e0b",
  high: "#ef4444",
};

/**
 * Status badge color mapping for UI display.
 */
export const statusColors: Record<TodoStatus, string> = {
  pending: "#6b7280",
  completed: "#22c55e",
  failed: "#ef4444",
};
