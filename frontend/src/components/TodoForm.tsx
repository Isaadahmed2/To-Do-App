/** Form component for creating new To-Do items. */
import { useState } from "react";
import { TodoCreate, Todo } from "../types";

interface TodoFormProps {
  /** Callback when a new To-Do is created */
  onCreate: (data: TodoCreate) => Promise<Todo>;
}

/**
 * Form component for creating new To-Do items.
 * Includes title, optional description, and priority selection.
 */
export function TodoForm({ onCreate }: TodoFormProps) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priority, setPriority] = useState<TodoCreate["priority"]>("medium");
  const [isExpanded, setIsExpanded] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  /**
   * Handle form submission.
   */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    setIsSubmitting(true);
    try {
      await onCreate({
        title: title.trim(),
        description: description.trim() || null,
        priority,
      });
      // Reset form
      setTitle("");
      setDescription("");
      setPriority("medium");
      setIsExpanded(false);
    } finally {
      setIsSubmitting(false);
    }
  };

  /**
   * Handle cancel action.
   */
  const handleCancel = () => {
    setTitle("");
    setDescription("");
    setPriority("medium");
    setIsExpanded(false);
  };

  /**
   * Handle keyboard shortcut for submission.
   */
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey && !e.ctrlKey) {
      // Only submit if title is not empty and form is expanded
      if (title.trim() && isExpanded) {
        e.preventDefault();
        handleSubmit(e);
      }
    }
    if (e.key === "Escape") {
      handleCancel();
    }
  };

  return (
    <form className="todo-form" onSubmit={handleSubmit}>
      {!isExpanded ? (
        /* Collapsed state - just show title input */
        <input
          type="text"
          className="form-title-input"
          placeholder="Add a new task..."
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          onFocus={() => setIsExpanded(true)}
          onKeyDown={handleKeyDown}
          disabled={isSubmitting}
        />
      ) : (
        /* Expanded state - show full form */
        <div className="form-expanded">
          <input
            type="text"
            className="form-title-input"
            placeholder="What needs to be done?"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            onKeyDown={handleKeyDown}
            autoFocus
            disabled={isSubmitting}
          />
          <textarea
            className="form-description-input"
            placeholder="Add a description (optional)..."
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={3}
            disabled={isSubmitting}
          />
          <div className="form-footer">
            <div className="form-priority">
              <label htmlFor="priority-select">Priority:</label>
              <select
                id="priority-select"
                className="form-priority-select"
                value={priority}
                onChange={(e) =>
                  setPriority(e.target.value as TodoCreate["priority"])
                }
                disabled={isSubmitting}
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>
            <div className="form-actions">
              <button
                type="button"
                className="btn-cancel"
                onClick={handleCancel}
                disabled={isSubmitting}
              >
                Cancel
              </button>
              <button
                type="submit"
                className="btn-submit"
                disabled={!title.trim() || isSubmitting}
              >
                {isSubmitting ? "Adding..." : "Add Task"}
              </button>
            </div>
          </div>
        </div>
      )}
    </form>
  );
}
