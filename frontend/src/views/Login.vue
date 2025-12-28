<template>
  <div>
    <h2>Login</h2>

    <input v-model="username" placeholder="Username" />
    <input v-model="password" type="password" placeholder="Password" />

    <button @click="login">Login</button>
  </div>
</template>

<script>
import api from "../services/api";

export default {
  data() {
    return {
      username: "",
      password: ""
    };
  },
  methods: {
    async login() {
      const res = await api.post("/auth/login", {
        username: this.username,
        password: this.password
      });
      localStorage.setItem("token", res.data.access_token);
      this.$router.push("/dashboard");
    }
  }
};
</script>
