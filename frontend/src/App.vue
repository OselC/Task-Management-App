<script setup>
import { useRoute } from 'vue-router'
const route = useRoute()
</script>

<template>
  <nav v-if="!(route.path === '/' || route.path === '/dashboard')">
    <router-link to="/">Login</router-link> |
    <router-link to="/dashboard">Dashboard</router-link>
  </nav>

  <main>
    <router-view />
  </main>
</template>

<style scoped>
nav {
  padding: 30px;
  text-align: center;
}
main {
  padding: 20px;
}
</style>
