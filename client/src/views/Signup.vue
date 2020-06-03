<template>
  <div class="login">
    <div class="container mt-2">
      <h3>Sign Up Here!</h3>
    <form class="form-horizontal">
    <div class="form-group">
      <div class="input-group col-md-4 offset-md-4">
          <input class="form-control border h3"  type="text" v-model="currentUser.name" placeholder="Name" >
      </div>
        <div class="input-group col-md-4 offset-md-4 mt-2">
            <input class="form-control border h3"  type="text" v-model="currentUser.email" placeholder="Email" >
        </div>
        <div class="input-group col-md-4 offset-md-4 mt-2">
          <input class="form-control border h3" type="text" v-model="currentUser.expected_calories" placeholder="Expected Calories" >
        </div>
        <div class="input-group col-md-4 offset-md-4 mt-2">
          <input class="form-control border h3" type="password" v-model="currentUser.password" placeholder="Password" >
        </div>
        <div v-if="signedUp">Signed up successfully! Please use the app.</div>
        <div><label><input type="checkbox" class="mt-4" v-model="isUserManagerChecked"> User Manager</input></label>
          <label><input type="checkbox" class="ml-4" v-model="isAdminChecked"> Admin</input></label>
          <div v-if="isUserManagerChecked || isAdminChecked" class="input-group col-md-4 offset-md-4 mt-3">
            <input class="form-control border h3" type="text" v-model="currentUser.token" placeholder="Please enter the token!" >
          </div>
        </div>
        <button @click="signUp()" class="btn-success btn mt-3" type="button">
            <b>Submit</b>
        </button>
        <div class="mt-2" v-if="error">Error! Please try again.</div>
    </div>
    <button @click="login()" class="btn-info btn mt-5" type="button">
        <b>Or Login!</b>
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
  name: "signup",
  data() {
    return {
      currentUser: {"email": "", "password": "", "name":"", "expected_calories": "", "token": ""},
      signedUp: false,
      isUserManagerChecked: false,
      isAdminChecked: false,
      error: false
    };
},
methods: {
  login() {
    this.$router.push('/login')
  },
  signUp() {
    var payload = this.currentUser
    if (this.isAdminChecked) {
      payload["role_id"] = 3
    } else if (this.isUserManagerChecked) {
      payload["role_id"] = 2
    } else {
      payload["role_id"] = 1
    }
    const path = 'http://localhost:5000/signup';
    axios.post(path, payload)
      .then((res) => {
        if (res.data["status"] == "success"){
        store.thisUser = res.data["user"]
        store.isLoggedIn = true
        this.signedUp = true
        this.$router.push('/')
      } else {
        this.error = true
      }
      })
      .catch((error) => {
        // eslint-disable-next-line
        console.log(error);
      });
  }
}
}
</script>
