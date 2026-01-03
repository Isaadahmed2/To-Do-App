/** API service for To-Do app backend communication. */
import { Todo, TodoCreate, TodoUpdate } from "../types";

const API_BASE = "/api";

/**
 * Custom error class for API operations.
 */
export class ApiError extends Error {
  constructor(message: string, public status?: number) {
    super(message);
    this.name = "ApiError";
  }
}

/**
 * Fetch wrapper that handles common API errors.
 */
async function fetchApi<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  });

  if (!response.ok) {
    const message = await response.text().catch(() => "Unknown error");
    throw new ApiError(message, response.status);
  }

  // Handle 204 No Content
  if (response.status === 204) {
    return undefined as T;
  }

  return response.json();
}

/**
 * API service class for To-Do operations.
 * Provides methods for all CRUD operations on To-Do items.
 */
export class TodoApiService {
  /**
   * Get all To-Do items from the server.
   * @returns Promise resolving to array of To-Do items
   */
  static async getAllTodos(): Promise<Todo[]> {
    return fetchApi<Todo[]>(`${API_BASE}/todos`);
  }

  /**
   * Get a specific To-Do item by ID.
   * @param id - The To-Do item ID
   * @returns Promise resolving to the To-Do item
   */
  static async getTodo(id: string): Promise<Todo> {
    return fetchApi<Todo>(`${API_BASE}/todos/${id}`);
  }

  /**
   * Create a new To-Do item.
   * @param data - The To-Do item data
   * @returns Promise resolving to the created To-Do item
   */
  static async createTodo(data: TodoCreate): Promise<Todo> {
    return fetchApi<Todo>(`${API_BASE}/todos`, {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  /**
   * Update an existing To-Do item.
   * @param id - The To-Do item ID
   * @param data - The update data
   * @returns Promise resolving to the updated To-Do item
   */
  static async updateTodo(id: string, data: TodoUpdate): Promise<Todo> {
    return fetchApi<Todo>(`${API_BASE}/todos/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    });
  }

  /**
   * Delete a To-Do item.
   * @param id - The To-Do item ID
   * @returns Promise resolving when deletion is complete
   */
  static async deleteTodo(id: string): Promise<void> {
    return fetchApi<void>(`${API_BASE}/todos/${id}`, {
      method: "DELETE",
    });
  }

  /**
   * Mark a To-Do item as completed.
   * @param id - The To-Do item ID
   * @returns Promise resolving to the updated To-Do item
   */
  static async markCompleted(id: string): Promise<Todo> {
    return fetchApi<Todo>(`${API_BASE}/todos/${id}/complete`, {
      method: "POST",
    });
  }

  /**
   * Mark a To-Do item as failed.
   * @param id - The To-Do item ID
   * @returns Promise resolving to the updated To-Do item
   */
  static async markFailed(id: string): Promise<Todo> {
    return fetchApi<Todo>(`${API_BASE}/todos/${id}/fail`, {
      method: "POST",
    });
  }

  /**
   * Set the priority of a To-Do item.
   * @param id - The To-Do item ID
   * @param priority - The new priority level
   * @returns Promise resolving to the updated To-Do item
   */
  static async setPriority(id: string, priority: Todo["priority"]): Promise<Todo> {
    return fetchApi<Todo>(`${API_BASE}/todos/${id}/priority?priority=${priority}`, {
      method: "PUT",
    });
  }
}
