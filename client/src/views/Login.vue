<template>
  <div class="login">
    <div class="container mt-2">
      <h3>Login Here!</h3>
    <form class="form-horizontal">
    <div class="form-group">
        <div class="input-group col-md-4 offset-md-4 mt-2">
            <input class="form-control border h3"  type="text" v-model="currentUser.email" placeholder="Email" >
        </div>
        <div class="input-group col-md-4 offset-md-4 mt-2">
          <input class="form-control border h3" type="password" v-model="currentUser.password" placeholder="Password" >
        </div>

        <button @click="login()" class="btn-success btn mt-3" type="button">
            <b>Submit</b>
        </button>
        <div class="mt-2" v-if="error">Error! Please try again.</div>
    </div>
    <button @click="signup()" class="btn-info btn mt-3" type="button">
        <b>Or Sign Up!</b>
    </button>
    </form>
  </div>
</div>
</template>

<script>
// import home from "@/views/Home.vue";
import axios from "axios";
import { store } from "../store.js";

export default {
  name: "login",
  data() {
    return {
      currentUser: {"email": "", "password": ""},
      loggedIn: false,
      error: false
    };
},
methods: {
  signup() {
    this.$router.push('/signup')
  },
  login() {
    var payload = this.currentUser
    const path = 'http://localhost:5000/login';
    axios.post(path, payload)
      .then((res) => {
        if (res.data["status"] == "success"){
          store.thisUser = res.data["user"]
          store.isLoggedIn = true
          this.loggedIn = true
          this.error = false
          this.$router.push('/')
      } else {
        this.error = true
      }})
      .catch((error) => {
        // eslint-disable-next-line
        console.log(error);
      });
  }
}
}
</script>
