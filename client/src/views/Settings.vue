<template>
  <div class="settings">
    <!-- <h3>Change your settings here!</h3> -->
    <div v-if="!isLoggedIn">
      <h4>You can edit your expected calories here and logout.</h4>
      <h5 class="mt-5">But first please sign up/ log in first, to access the application.</h5>
      <div><button class="btn-lg btn-warning mt-5" @click="login()">Login</button></div>
      <div><button class="btn-lg btn-success mt-3" @click="signup()">Sign Up!</button></div>
    </div>
    <div v-if="isLoggedIn">
      <h4 v-if="thisUser.role_id===3">Hi {{ thisUser.name.split(" ")[0] }}, you are an admin, and you can add, access and edit all records and users!</h4>
      <h4 v-if="thisUser.role_id===2">You are a user manager, you can add, access and edit all users!</h4>
      <button v-if="thisUser.role_id===3" class="btn btn-warning mb-1" @click="showMeals(showMealsStatus)">See All Meals</button>
      <button v-if="thisUser.role_id===2 || thisUser.role_id===3" class="btn btn-warning mb-1 ml-5" @click="showUsers(showUsersStatus)">See All Users</button>
      <button v-if="thisUser.role_id===2 || thisUser.role_id===3" class="btn btn-warning mb-1 ml-5" @click="addingUserStatusToggle(addingUserStatus)">Add New User</button>
       <h5 v-if="showMealsStatus" class="mt-3">All users' past meals are:</h5>
      <div v-if="showMealsStatus" v-for="(meal,index) in allUsersMeals">
         <div class="mt-2" v-if="currentlyEditingMealStatus===false || meal.id!=currentlyEditingMealId">
           {{ index+1 }}. {{ meal.text }} with {{ meal.num_calories}} calories at {{ meal.datetime | formatDate}} for user {{ meal.user_id}}
            <button class="btn-sm btn-info ml-3" @click="updateCurrentlyEditing(meal.id, true)">Edit</button>  <button class="btn-sm btn-danger ml-1" @click="deleteCurrentMeal(meal.id)">Delete</button>
          </div>
          <div class="mt-2" v-else-if="meal.id===currentlyEditingMealId && currentlyEditingMealStatus===true">
            <div class="form-group row">
              <p class="offset-md-4">{{ index + 1}}. </p>
            <input class="input-sm form-control border h3 col-md-2 ml-2"  type="text" v-model="currentlyEditingRecord.text">
            <input class="input-sm form-control border h3 col-md-2 ml-2"  type="text" v-model="currentlyEditingRecord.numCalories">
             <button class="btn btn-xs btn-success ml-3" @click="updateCurrentlyEditing(meal.id, false)">Save</button>
            </div>
          </div>
      </div>
      <h5 v-if="showUsersStatus" class="mt-3">All users are:</h5>
     <div v-if="showUsersStatus" v-for="(user,index) in allUsers">
        <div class="mt-2" v-if="(currentlyEditingUserStatus===false || user.id!=currentlyEditingUserId)">
          {{ index+1 }}. {{ user.name }} with expected {{ user.expected_calories}} calories with e-mail {{ user.email }} and role_id {{ user.role_id }}, and user_id {{ user.id }}
           <button class="btn-sm btn-info ml-3" @click="updateCurrentlyEditingUser(user.id, true)">Edit</button>  <button class="btn-sm btn-danger ml-1" @click="deleteCurrentUser(user.id)">Delete</button>
         </div>
         <div class="mt-2" v-else-if="user.id===currentlyEditingUserId && currentlyEditingUserStatus===true">
           <div class="form-group row">
             <p class="offset-md-2">{{ index + 1}}. </p>
           <input class="input-sm form-control border h3 col-md-2 ml-2"  type="text" v-model="currentlyEditingUser.name">
           <input class="input-sm form-control border h3 col-md-2 ml-2"  type="text" v-model="currentlyEditingUser.email">
           <input class="input-sm form-control border h3 col-md-2 ml-2"  type="text" v-model="currentlyEditingUser.expected_calories">
           <input class="input-sm form-control border h3 col-md-1 ml-2"  type="text" v-model="currentlyEditingUser.role_id">
            <button class="btn btn-xs btn-success ml-3" @click="updateCurrentlyEditingUser(user.id, false)">Save</button>
           </div>
         </div>
     </div>
     <h5 v-if="addingUserStatus" class="mt-3">Add new user below:</h5>
     <div v-if="addingUserStatus" class="container mt-2">
     <form class="form-horizontal">
     <div class="form-group">
         <div class="input-group col-md-4 offset-md-4">
             <input class="form-control border h3"  type="text" v-model="currentNewUser.name" placeholder="Enter the name" >
         </div>
         <div class="input-group col-md-4 offset-md-4 mt-2">
           <input class="form-control border h3" type="text" v-model="currentNewUser.email" placeholder="Enter the email" >
         </div>
         <div class="input-group col-md-4 offset-md-4 mt-2">
           <input class="form-control border h3" type="text" v-model="currentNewUser.expected_calories" placeholder="Enter Expected Calories" >
         </div>
         <div class="input-group col-md-4 offset-md-4 mt-2">
           <input class="form-control border h3" type="text" v-model="currentNewUser.role_id" placeholder="Role ID:1, 2 or 3 (user, manager or admin)" >
         </div>
         <div class="input-group col-md-4 offset-md-4 mt-2">
           <input class="form-control border h3" type="password" v-model="currentNewUser.password" placeholder="Password" >
         </div>
         <div v-if="currentNewUser.role_id==2 || currentNewUser.role_id==3" class="input-group col-md-4 offset-md-4 mt-2">
           <input class="form-control border h3" type="text" v-model="currentNewUser.token" placeholder="Token" >
         </div>
         <button @click="addUser()" class="btn-success btn mt-3" type="button">
             <b>Submit</b>
         </button>
     </div>
     </form>
     <!-- <p v-if="currentMeal.text"> You have entered {{ currentMeal.text }}<span v-if="!currentMeal.numCalories">!</span><span v-if="currentMeal.numCalories"> with {{ currentMeal.numCalories }} calories!</span>
     <span v-if="currentMeal.user_id"> For User ID: {{ currentMeal.user_id }}</span></p> -->
     </div>
      <hr v-if="thisUser.role_id===2 || thisUser.role_id===3" style="border: 0.5px solid black;" />

    <h4 class="mb-3 mt-5"> Your current expected no. of calories are: {{ this.thisUser.expected_calories }}</h4>
    <button class="btn btn-info" v-on:click="add(1)"> Add 1 Calorie </button>
    <button class="btn btn-info ml-3" v-on:click="subtract(1)"> Subtract 1 Calorie </button>
    <button class="btn btn-info ml-3" v-on:click="add(100)"> Add 100 Calories </button>
    <button class="btn btn-info ml-3" v-on:click="subtract(100)"> Subtract 100 Calories </button>
    <!-- <div class="mt-3 font-weight-bold">OR</div> -->
    <div class="form-group mt-2">
      <button @click="changeExpectedCalories()" class="btn-success btn mt-3" type="button">
          <b>Save</b>
      </button>
      <div class="mt-3" v-if="saved">The value was saved!</div>
    </div>
    <div v-if="thisUser"><button class="btn btn-danger mt-5" @click="logout()">Logout</button></div>
    <!-- <home-component></home-component> -->
    <!-- Reuse information by using components from other pages -->
  </div>
  </div>
</template>

<script>

// import home from "@/views/Home.vue";
import axios from "axios";
import { store } from "../store.js";

export default {
  name: "settings",
  data() {
    return {
      thisUser: store.thisUser,
      isLoggedIn: store.isLoggedIn,
      saved: false,
      showMealsStatus: false,
      currentlyEditingMealId: null,
      currentlyEditingMealStatus: false,
      currentlyEditingRecord: {"text": "", "numCalories": null, "id": null, "user_id": null},
      allUsersMeals: [],
      showUsersStatus: false,
      currentlyEditingUserId: null,
      currentlyEditingUserStatus: false,
      currentlyEditingUser: {"name": "", "email": "", "expected_calories": null, "role_id": null},
      allUsers: [],
      addingUserStatus: false,
      currentNewUser: {"name": "", "email": "", "expected_calories": null, "role_id": null}
    };
},
methods: {
  login() {
    this.$router.push('/login')
  },
  signup() {
    this.$router.push('/signup')
  },
changeExpectedCalories() {
  var payload = this.thisUser
  const path = 'http://localhost:5000/add-user';
  this.saved = true
  axios.put(path, payload)
    .then((res) => {
      console.log(res.data)
    })
    .catch((error) => {
      // eslint-disable-next-line
      console.log(error);
    });
},
add(inc){
  this.thisUser.expected_calories += inc;
  this.saved = false;
},
subtract(dec){
  this.thisUser.expected_calories -= dec;
  this.saved = false;
},
logout() {
  store.isLoggedIn = false
  store.thisUser = null
  this.$router.push('/')
},
showMeals(current){
  this.showMealsStatus = !current
  if (this.showMealsStatus) {
    this.getMealsAsAdmin()
  }
},
showUsers(current){
  this.showUsersStatus = !current
  if (this.showUsersStatus) {
    this.getUsers()
  }
},
addingUserStatusToggle(current){
  this.addingUserStatus = !current
  // if (this.addingUserStatus) {
  //   this.getUsers()
  // }
},
getMealsAsAdmin() {
  const path = "http://localhost:5000/get-meals-admin/" + store.thisUser.id;
  axios.get(path)
    .then(res => {
      this.allUsersMeals = res.data["meals"];
      this.showMealsStatus = true;
  //     this.allUsersMeals.sort(function(a, b){
  //       var dateA=new Date(a.datetime), dateB=new Date(b.datetime)
  //       return dateA-dateB //sort by date ascending
  // })
    })
    .catch(error => {
      // eslint-disable-next-line
      console.error(error);
    });
},
getUsers() {
  const path = "http://localhost:5000/get-users-manager/" + store.thisUser.id;
  axios.get(path)
    .then(res => {
      this.allUsers = res.data["users"];
      this.showUsersStatus = true;
  //     this.allUsersMeals.sort(function(a, b){
  //       var dateA=new Date(a.datetime), dateB=new Date(b.datetime)
  //       return dateA-dateB //sort by date ascending
  // })
    })
    .catch(error => {
      // eslint-disable-next-line
      console.error(error);
    });
},
updateCurrentlyEditing(id, status) {
  // console.log("TEST",id,status, this.allUsersMeals)
  this.currentlyEditingMealId = id
  this.currentlyEditingMealStatus = status
  if (status == true){
    // update currently editing record if the person presses Edit or Delete buttons
    for (var i=0; i < this.allUsersMeals.length; i++) {
      if (this.allUsersMeals[i].id == id) {
        this.currentlyEditingRecord.text = this.allUsersMeals[i].text
        this.currentlyEditingRecord.numCalories = this.allUsersMeals[i].num_calories
        this.currentlyEditingRecord.id = id
        this.currentlyEditingRecord.user_id = this.allUsersMeals[i].user_id
      }
    }
  } else {
    // make a post request to save the newly edited record
      var payload = {"id": this.currentlyEditingRecord.id,
                     "text":this.currentlyEditingRecord.text,
                     "user_id": this.currentlyEditingRecord.user_id,
                     "num_calories": this.currentlyEditingRecord.numCalories}
      // console.log("payload", payload)
      const path = 'http://localhost:5000/add-meal';
      axios.put(path, payload)
        .then((res) => {
          console.log(res.data)
          return axios.get("http://localhost:5000/get-meals-admin/" + store.thisUser.id) // Chain requests
        }).then((res) =>  {
          this.allUsersMeals = res.data["meals"];
          this.allUsersMeals.sort(function(a, b){
            var dateA=new Date(a.datetime), dateB=new Date(b.datetime)
            return dateA-dateB //sort by date ascending
          })
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    }
},
deleteCurrentMeal(id){
  // make a delete request to delete this ID
    const path = 'http://localhost:5000/delete-meal/' + id;
    // console.log(path)
    axios.delete(path)
      .then((res) => {
        console.log(res.data)
        return axios.get("http://localhost:5000/get-meals-admin/" + store.thisUser.id) // Chain requests
      }).then((res) =>  {
        this.allUsersMeals = res.data["meals"];
        this.allUsersMeals.sort(function(a, b){
          var dateA=new Date(a.datetime), dateB=new Date(b.datetime)
          return dateA-dateB //sort by date ascending
    })
      })
      .catch((error) => {
        // eslint-disable-next-line
        console.log(error);
      });
},
updateCurrentlyEditingUser(id, status) {
  // console.log("TEST USRE",id,status, this.allUsers)
  this.currentlyEditingUserId = id
  this.currentlyEditingUserStatus = status
  if (status == true){
    // update currently editing record if the person presses Edit or Delete buttons
    for (var i=0; i < this.allUsers.length; i++) {
      if (this.allUsers[i].id == id) {
        this.currentlyEditingUser.name = this.allUsers[i].name
        this.currentlyEditingUser.expected_calories = this.allUsers[i].expected_calories
        this.currentlyEditingUser.email = this.allUsers[i].email
        this.currentlyEditingUser.role_id = this.allUsers[i].role_id
      }
    }
  } else {
    // make a post request to save the newly edited record
      var payload = {"name": this.currentlyEditingUser.name,
                     "expected_calories":this.currentlyEditingUser.expected_calories,
                     "email": this.currentlyEditingUser.email,
                     "role_id": this.currentlyEditingUser.role_id}
      // console.log("payload", payload)
      const path = 'http://localhost:5000/add-user';
      axios.put(path, payload)
        .then((res) => {
          console.log(res.data)
          return axios.get("http://localhost:5000/get-users-manager/" + store.thisUser.id) // Chain requests
        }).then((res) =>  {
          this.allUsers = res.data["users"];
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    }
},
deleteCurrentUser(id){
  // make a delete request to delete this ID
    const path = 'http://localhost:5000/delete-user/' + id;
    // console.log(path)
    axios.delete(path)
      .then((res) => {
        console.log(res.data)
        return axios.get("http://localhost:5000/get-users-manager/" + store.thisUser.id) // Chain requests
      }).then((res) =>  {
        this.allUsers = res.data["users"];
      })
      .catch((error) => {
        // eslint-disable-next-line
        console.log(error);
      });
},
addUser(payload) {
  payload = this.currentNewUser
  const path = 'http://localhost:5000/signup';
  axios.post(path, payload)
    .then((res) => {
      console.log(res)
      this.addingUserStatus=false;
      this.getUsers();
    })
    .catch((error) => {
      // eslint-disable-next-line
      console.log(error);
    });
},
}
};

</script>
