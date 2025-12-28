<template>
  <div>
    <h2>Dashboard</h2>

    <input v-model="title" placeholder="Title" />
    <input v-model="description" placeholder="Description" />
    <input v-model="status" placeholder="Status" />

    <button @click="addTask">Add Task</button>

    <ul>
      <li v-for="task in tasks" :key="task.id">
        {{ task.title }} - {{ task.status }}
      </li>
    </ul>
  </div>
</template>

<script>
import api from "../services/api";

export default {
  data() {
    return {
      tasks: [],
      title: "",
      description: "",
      status: ""
    };
  },
  async mounted() {
    const res = await api.get("/tasks");
    this.tasks = res.data;
  },
  methods: {
    async addTask() {
      await api.post("/tasks", {
        title: this.title,
        description: this.description,
        status: this.status
      });
      const res = await api.get("/tasks");
      this.tasks = res.data;
    }
  }
};
</script>
