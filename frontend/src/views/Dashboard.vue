<template>
  <div class="dashboard">
    <div class="header">
      <div class="header-left">
        <h1>Dashboard</h1>
        <p class="subtitle">Manage your tasks efficiently</p>
      </div>
      <div class="header-right">
        <button class="logout" @click="logout">Logout</button>
      </div>
    </div>

    <form class="task-form" @submit.prevent="addTask">
      <div class="form-row">
        <input v-model="title" placeholder="Title" required class="input-field" />
        <input v-model="description" placeholder="Description" class="input-field" />
      </div>
      <div class="form-row controls">
        <select v-model="status" class="select-field">
          <option>To Do</option>
          <option>In Progress</option>
          <option>Done</option>
        </select>
        <button type="submit" class="add-btn">Add Task</button>
      </div>
    </form>

    <div class="task-counter">{{ tasks.length }} tasks</div>

    <div class="task-list">
        <div v-if="tasks.length === 0" class="empty">
          <p>No tasks yet — add your first task with the form above.</p>
        </div>
        <div v-for="task in tasks" :key="task.id" class="task-card">
          <!-- action icons top-right -->
          <div class="task-actions-top">
            <button class="icon-btn delete-icon" @click="deleteTask(task.id)" aria-label="Delete task">
              <!-- trash SVG -->
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M9 3v1H4v2h16V4h-5V3H9z" fill="currentColor"/>
                <path d="M6 7l1 14a2 2 0 002 2h6a2 2 0 002-2l1-14H6z" fill="currentColor"/>
              </svg>
            </button>
          </div>

          <template v-if="editingId !== task.id">
            <h3 class="task-title">{{ task.title }}</h3>
            <p class="task-desc">{{ task.description }}</p>
            <span :class="['badge', task.status.replace(/\s+/g,'-').toLowerCase()]">{{ task.status }}</span>
            <!-- edit icon bottom-right -->
            <button class="icon-btn edit-icon-bottom" @click="startEdit(task)" aria-label="Edit task">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25z" fill="currentColor"/>
                <path d="M20.71 7.04a1 1 0 000-1.41l-2.34-2.34a1 1 0 00-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z" fill="currentColor"/>
              </svg>
            </button>
          </template>

          <template v-else>
            <input v-model="editTitle" />
            <input v-model="editDescription" />
            <select v-model="editStatus">
              <option>To Do</option>
              <option>In Progress</option>
              <option>Done</option>
            </select>
            <div class="task-actions">
              <button class="save-btn" @click="saveEdit(task.id)">Save</button>
              <button class="cancel-btn" @click="cancelEdit">Cancel</button>
            </div>
          </template>
        </div>
    </div>
  </div>
</template>

<script>
import api from "../services/api";
import "../assets/styles/dashboard.css";

export default {
  name: "Dashboard",
  data() {
    return {
      tasks: [],
      title: "",
      description: "",
      status: "To Do",
      editingId: null,
      editTitle: "",
      editDescription: "",
      editStatus: "To Do"
    };
  },
  async mounted() {
    this.fetchTasks();
  },
  methods: {
    async fetchTasks() {
      try {
        const res = await api.get("/tasks");
        this.tasks = res.data;
      } catch (err) {
        console.error(err);
        this.tasks = [];
      }
    },
    async addTask() {
      try {
        await api.post("/tasks", {
          title: this.title,
          description: this.description,
          status: this.status
        });
        this.title = "";
        this.description = "";
        this.status = "To Do";
        this.fetchTasks();
      } catch (err) {
        console.error(err);
        alert('Failed to add task');
      }
    },
    startEdit(task) {
      this.editingId = task.id;
      this.editTitle = task.title || "";
      this.editDescription = task.description || "";
      this.editStatus = task.status || "To Do";
    },
    async saveEdit(id) {
      try {
        await api.put(`/tasks/${id}`, {
          title: this.editTitle,
          description: this.editDescription,
          status: this.editStatus
        });
        this.editingId = null;
        this.fetchTasks();
      } catch (err) {
        console.error(err);
        alert('Failed to save task');
      }
    },
    cancelEdit() {
      this.editingId = null;
    },
    async deleteTask(id) {
      if (!confirm('Delete this task?')) return;
      try {
        await api.delete(`/tasks/${id}`);
        this.fetchTasks();
      } catch (err) {
        console.error(err);
        alert('Failed to delete task');
      }
    },
    logout() {
      localStorage.removeItem("token");
      this.$router.push("/");
    }
  }
};
</script>

