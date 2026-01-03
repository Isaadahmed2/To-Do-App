/** Individual To-Do item component with edit and action buttons. */
import { useState } from "react";
import { Todo, priorityColors, statusColors, TodoUpdate } from "../types";

interface TodoItemProps {
  /** The To-Do item data */
  todo: Todo;
  /** Callback when a To-Do item is updated */
  onUpdate: (id: string, data: TodoUpdate) => Promise<void>;
  /** Callback when a To-Do item is deleted */
  onDelete: (id: string) => Promise<void>;
  /** Callback when a To-Do item is marked completed */
  onComplete: (id: string) => Promise<void>;
  /** Callback when a To-Do item is marked failed */
  onFail: (id: string) => Promise<void>;
}

/**
 * Component for displaying and managing a single To-Do item.
 * Supports inline editing and status/priority actions.
 */
export function TodoItem({
  todo,
  onUpdate,
  onDelete,
  onComplete,
  onFail,
}: TodoItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(todo.title);
  const [editDescription, setEditDescription] = useState(todo.description || "");
  const [editPriority, setEditPriority] = useState(todo.priority);

  /**
   * Handle save action for inline editing.
   */
  const handleSave = async () => {
    if (editTitle.trim()) {
      await onUpdate(todo.id, {
        title: editTitle.trim(),
        description: editDescription.trim() || null,
        priority: editPriority,
      });
      setIsEditing(false);
    }
  };

  /**
   * Handle cancel action for inline editing.
   */
  const handleCancel = () => {
    setEditTitle(todo.title);
    setEditDescription(todo.description || "");
    setEditPriority(todo.priority);
    setIsEditing(false);
  };

  /**
   * Handle keyboard shortcuts for editing.
   */
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSave();
    }
    if (e.key === "Escape") {
      handleCancel();
    }
  };

  return (
    <div className={`todo-item ${todo.status}`}>
      {/* Priority indicator */}
      <div
        className="priority-indicator"
        style={{ backgroundColor: priorityColors[todo.priority] }}
        title={`Priority: ${todo.priority}`}
      />

      <div className="todo-content">
        {isEditing ? (
          /* Edit mode */
          <div className="todo-edit-form">
            <input
              type="text"
              className="edit-title-input"
              value={editTitle}
              onChange={(e) => setEditTitle(e.target.value)}
              onKeyDown={handleKeyDown}
              autoFocus
              placeholder="Title"
            />
            <textarea
              className="edit-description-input"
              value={editDescription}
              onChange={(e) => setEditDescription(e.target.value)}
              placeholder="Description (optional)"
              rows={2}
            />
            <select
              className="edit-priority-select"
              value={editPriority}
              onChange={(e) => setEditPriority(e.target.value as Todo["priority"])}
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
            <div className="edit-actions">
              <button className="btn-save" onClick={handleSave}>
                Save
              </button>
              <button className="btn-cancel" onClick={handleCancel}>
                Cancel
              </button>
            </div>
          </div>
        ) : (
          /* View mode */
          <>
            <div className="todo-header">
              <h3 className="todo-title">{todo.title}</h3>
              <span
                className="status-badge"
                style={{ backgroundColor: statusColors[todo.status] }}
              >
                {todo.status}
              </span>
            </div>
            {todo.description && (
              <p className="todo-description">{todo.description}</p>
            )}
            <div className="todo-meta">
              <span className="todo-priority">
                Priority: <span style={{ color: priorityColors[todo.priority] }}>{todo.priority}</span>
              </span>
              <span className="todo-date">
                {new Date(todo.created_at).toLocaleDateString()}
              </span>
            </div>
          </>
        )}
      </div>

      {/* Action buttons */}
      <div className="todo-actions">
        {todo.status === "pending" && (
          <>
            <button
              className="btn-action btn-complete"
              onClick={() => onComplete(todo.id)}
              title="Mark as completed"
            >
              ✓
            </button>
            <button
              className="btn-action btn-fail"
              onClick={() => onFail(todo.id)}
              title="Mark as failed"
            >
              ✗
            </button>
          </>
        )}
        {isEditing ? null : (
          <>
            <button
              className="btn-action btn-edit"
              onClick={() => setIsEditing(true)}
              title="Edit"
            >
              ✎
            </button>
            <button
              className="btn-action btn-delete"
              onClick={() => onDelete(todo.id)}
              title="Delete"
            >
              🗑
            </button>
          </>
        )}
      </div>
    </div>
  );
}
