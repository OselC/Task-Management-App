<template>
  <div class="page-bg">

  <div class="login-container">
    <div class="login-card">
      <h2>Task Manager Login</h2>

      <input
        v-model="username"
        @blur="touchedUsername = true"
        placeholder="Username"
        class="input"
      />

      <div v-if="usernameError" class="error">{{ usernameError }}</div>

      <input
        v-model="password"
        @blur="touchedPassword = true"
        type="password"
        placeholder="Password"
        class="input"
      />

      <div v-if="passwordError" class="error">{{ passwordError }}</div>

      <button @click="login" class="btn">
        Login
      </button>
    </div>
  </div>
  
</div>
</template>

<script>
import api from "../services/api";
import "../assets/styles/login.css";

export default {
  name: "Login",
  data() {
    return {
      username: "",
      password: ""
      ,touchedUsername: false,
      touchedPassword: false,
      submitAttempted: false
    };
  },
  computed: {
    usernameError() {
      if (!this.touchedUsername && !this.submitAttempted) return "";
      if (!this.username) return "Username is required";
      if (this.username.length < 3) return "Username must be at least 3 characters";
      return "";
    },
    passwordError() {
      if (!this.touchedPassword && !this.submitAttempted) return "";
      if (!this.password) return "Password is required";
      if (this.password.length < 6) return "Password must be at least 6 characters";
      return "";
    },
    isValid() {
      // validation independent of touched state
      if (!this.username || this.username.length < 3) return false;
      if (!this.password || this.password.length < 6) return false;
      return true;
    }
  },
  methods: {
    async login() {
      this.submitAttempted = true;
      this.touchedUsername = true;
      this.touchedPassword = true;

      if (!this.isValid) return;

      try {
        const res = await api.post(
          "/auth/login",
          {
            username: this.username,
            password: this.password
          },
          {
            headers: {
              "Content-Type": "application/json"
            }
          }
        );

        // Save JWT token
        localStorage.setItem("token", res.data.access_token);

        // Redirect to dashboard
        this.$router.push("/dashboard");
      } catch (error) {
        console.error(error);
        alert("Invalid username or password");
      }
    }
  }
};
</script>


