<script setup>
// You generally don't need to import views here; 
// the router handles that!
</script>

<template>
  <nav>
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
