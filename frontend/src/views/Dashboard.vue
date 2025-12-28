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

    <div v-if="successMessage" class="success-message">{{ successMessage }}</div>

    <div class="task-counter-wrapper">
      <div class="task-counter">
        {{ filteredTasks.length }} tasks
        <select v-model="filterStatus" class="filter-dropdown">
          <option value="">All</option>
          <option value="To Do">To Do</option>
          <option value="In Progress">In Progress</option>
          <option value="Done">Done</option>
        </select>
      </div>
      <div class="search-bar-wrapper">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search tasks..."
          class="search-bar"
        />
        <span class="search-icon">
          <!-- Magnifying glass SVG -->
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M11 4a7 7 0 100 14 7 7 0 000-14zm0-2a9 9 0 016.32 15.32l4.36 4.36-1.41 1.41-4.36-4.36A9 9 0 1111 2z" fill="currentColor"/>
          </svg>
        </span>
      </div>
    </div>

    <div class="task-list">
        <div v-if="paginatedTasks.length === 0" class="empty">
          <p>No tasks match your search or filter.</p>
        </div>
        <div v-for="task in paginatedTasks" :key="task.id" class="task-card">
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

    <div class="pagination" v-if="totalPages > 1">
      <button
        class="pagination-btn"
        :disabled="currentPage === 1"
        @click="currentPage--"
      >
        Previous
      </button>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <button
        class="pagination-btn"
        :disabled="currentPage === totalPages"
        @click="currentPage++"
      >
        Next
      </button>
    </div>

  </div>
</template>

<script>
import api from "../services/api";
import "../assets/styles/dashboard.css"; // Ensure styles are imported

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
      editStatus: "To Do",
      filterStatus: "",
      searchQuery: "",
      currentPage: 1,
      tasksPerPage: 8,
      successMessage: "", // New state for success message
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.filteredTasks.length / this.tasksPerPage);
    },
    paginatedTasks() {
      const start = (this.currentPage - 1) * this.tasksPerPage;
      const end = start + this.tasksPerPage;
      return this.filteredTasks.slice(start, end);
    },
    filteredTasks() {
      const query = this.searchQuery.toLowerCase();
      return this.tasks.filter(task => {
        const matchesStatus = !this.filterStatus || task.status === this.filterStatus;
        const matchesSearch = task.title.toLowerCase().includes(query);
        return matchesStatus && matchesSearch;
      });
    },
  },
  watch: {
    filteredTasks() {
      if (this.currentPage > this.totalPages) {
        this.currentPage = this.totalPages || 1;
      }
    },
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
        this.successMessage = "Task added successfully!"; // Set success message
        setTimeout(() => {
          this.successMessage = ""; // Clear message after 3 seconds
        }, 3000);
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

