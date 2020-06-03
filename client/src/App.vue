<template>
  <div id="app">
    <div id="nav">
      <!-- <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link> -->
      <!--Navigation Bar-->
      <nav class="navbar navbar-expand-sm navbar-dark">
        <div class="container">
            <a class="navbar-text h3" style="color:black;text-decoration:none;" href="/">
                Cal Track
            </a>
            <div class="navbar-nav">
                <router-link class="nav-text nav-link h5" to="/">Home</router-link>
                <router-link class="nav-text nav-link h5" to="/past-meals">Past Meals</router-link>
                <router-link class="nav-text nav-link h5" to="/settings">Settings</router-link>
                <router-link class="nav-text nav-link h5" to="/about">About</router-link>
            </div>
        </div>
      </nav>
    </div>
    <router-view />
  </div>
</template>

<script>
import { store } from "./store.js";

export default {
  // data() {
  //   return {
  //     isLoggedIn: false
  //   };
  // },
  methods: {
    logout() {
      store.isLoggedIn = false
      store.thisUser = null
      this.$router.push('/')
    }
  }
  // watch: {
  //   isLoggedIn: function() {
  //     this.isLoggedIn = store.isLoggedIn
  //   }
  // }
}
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  /* margin-top: 60px; */
}
#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
