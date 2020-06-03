<template>
  <div class="home">
    <div v-if="!isLoggedIn">
      <h4> Welcome to Cal Track!</h4>
      <h4> One place to manage your meals and calories status.</h4>
      <h5 class="mt-5">Please sign up/ log in first, to access the application.</h5>
      <div><button class="btn-lg btn-warning mt-5" @click="login()">Login</button></div>
      <div><button class="btn-lg btn-success mt-3" @click="signup()">Sign Up!</button></div>
    </div>
    <div v-if="isLoggedIn">
      <h3>Welcome to Cal Track, {{ thisUser.name.split(" ")[0] }}!</h3>
      <h5> One place to manage your meals and calories status.</h5>
      <div class="container mt-2">
      <form class="form-horizontal">
      <div class="form-group">
          <div class="input-group col-md-4 offset-md-4">
              <input class="form-control border h3" type="text" v-model="currentMeal.text" placeholder="Enter the meal" >
          </div>
          <div class="input-group col-md-4 offset-md-4 mt-2">
            <input class="form-control border h3" type="text" v-model="currentMeal.numCalories" placeholder="Enter the no. of calories" >
          </div>
          <div v-if="thisUser.role_id==3" class="input-group col-md-4 offset-md-4 mt-2">
            <input class="form-control border h3" type="text" v-model="currentMeal.user_id" placeholder="User ID" >
          </div>
          <button @click="addMeal()" class="btn-success btn mt-3" type="button">
              <b>Submit</b>
          </button>
          <p v-if="saved">Saved!</p>
      </div>
      </form>

      <p v-if="currentMeal.text"> You have entered {{ currentMeal.text }}<span v-if="!currentMeal.numCalories">!</span><span v-if="currentMeal.numCalories"> with {{ currentMeal.numCalories }} calories!</span>
      <span v-if="currentMeal.user_id"> For User ID: {{ currentMeal.user_id }}</span></p>
      <div class="mt-2" v-if="error">Error! Please try again.</div>
      <h5 class="mt-4">Based on your per day expected calories of {{ thisUser.expected_calories }}, your current status is {{ status }}:
        <div class="mt-3">
      <button class="btn btn-success" v-if ="status==='Green'">Left with {{ this.caloriesBalance }} calories!</button>
      <button class="btn btn-danger" v-if ="status==='Red'">Exceeded Calories for the day!</button>
      <!-- <button class="float-right" type="button" @click="calculateStatus(thisUser.id)"><img style="width:25px; height:25px;" src="@/assets/refresh_icon.png"></button> -->
        </div>
      </h5>
    </div>
    <!-- <hr class="col-md-12" style="border:0.5px solid black;"/> -->
    <h4 class="mt-5">Your meals in the past day have been:</h4>
    <div v-for="(meal,index) in todayMeals">
       <div class="mt-2" v-if="currentlyEditingStatus===false || index!= currentlyEditingIndex">
        <span style="color:green;" v-if="meal.status==='within_limit'">{{ index+1 }}. {{ meal.text }} with {{ meal.num_calories}} calories at {{ meal.datetime | formatTodayDate}}</span>
        <span style="color:red;" v-if="meal.status==='exceeded_limit'">{{ index+1 }}. {{ meal.text }} with {{ meal.num_calories}} calories at {{ meal.datetime | formatTodayDate}}</span>
        <button class="btn-sm btn-info ml-3" @click="updateCurrentlyEditing(index, true)">Edit</button>  <button class="btn-sm btn-danger ml-1" @click="deleteCurrentMeal(index)">Delete</button>
        </div>
        <div class="mt-2" v-else-if="index===currentlyEditingIndex && currentlyEditingStatus===true">
          <div class="form-group row">
            <p class="offset-md-4">{{ index + 1}}. </p>
          <input class="input-sm form-control border h3 col-md-2 ml-2"  type="text" v-model="currentlyEditingRecord.text">
          <input class="input-sm form-control border h3 col-md-2 ml-2"  type="text" v-model="currentlyEditingRecord.numCalories">
           <button class="btn btn-xs btn-success ml-3" @click="updateCurrentlyEditing(index, false)">Save</button>

          </div>
        </div>
    </div>

    <footer></footer>
    <div class="mt-5"></div>
    </div>
    <!-- <past-meals v-bind:thisUser="thisUser"></past-meals> -->
</div>
</template>

<script>

import axios from "axios";
// import PastMeals from "./PastMeals.vue";
import { store } from "../store.js";

export default {
  /* eslint-disable */
  name: "home",
  data() {
    return {
      currentMeal: {"text": "", "numCalories": null, "user_id": null},
      allPastMeals: [],
      todayMeals: [],
      status: "",
      caloriesBalance: 0,
      currentlyEditingIndex: null,
      currentlyEditingStatus: false,
      thisUser: store.thisUser,
      isLoggedIn: store.isLoggedIn,
      currentlyEditingRecord: {"text": "", "numCalories": null},
      error:false,
      saved: false
    };
  },
  methods: {
    login() {
      this.$router.push('/login')
    },
    signup() {
      this.$router.push('/signup')
    },
    updateCurrentlyEditing(index, status) {
      this.currentlyEditingIndex = index
      console.log("Currently editing", this.currentlyEditingIndex)
      this.currentlyEditingStatus = status
      if (status == true){
        // update currently editing record if the person presses Edit or Delete buttons
        this.currentlyEditingRecord.text = this.todayMeals[index].text
        this.currentlyEditingRecord.numCalories = this.todayMeals[index].num_calories
        this.currentlyEditingRecord.id = this.todayMeals[index].id
      } else {
        // make a post request to save the newly edited record
          var payload = {"id": this.currentlyEditingRecord.id,
                         "text":this.currentlyEditingRecord.text,
                         "user_id": store.thisUser.id,
                         "num_calories": this.currentlyEditingRecord.numCalories}
          console.log(payload)
          const path = 'http://localhost:5000/add-meal';
          axios.put(path, payload)
            .then((res) => {
              console.log(res.data)
              return axios.get("http://localhost:5000/get-today-meals/" + store.thisUser.id) // Chain requests
            }).then((res) =>  {
              this.todayMeals = res.data["meals"];
          //     this.todayMeals.sort(function(a, b){
          //       var dateA=new Date(a.datetime), dateB=new Date(b.datetime)
          //       return dateA-dateB //sort by date ascending
          // })
              this.calculateStatus(store.thisUser.id)
            })
            .catch((error) => {
              // eslint-disable-next-line
              console.log(error);
            });
        }
    },
    deleteCurrentMeal(index){
      // make a delete request to delete this ID
        const path = 'http://localhost:5000/delete-meal/' + this.todayMeals[index].id;
        console.log(path)
        axios.delete(path)
          .then((res) => {
            console.log(res.data)
            return axios.get("http://localhost:5000/get-today-meals/" + store.thisUser.id) // Chain requests
          }).then((res) =>  {
            this.todayMeals = res.data["meals"];
            this.calculateStatus(store.thisUser.id)
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.log(error);
          });
    },
    getUsers() {
      const path = "http://localhost:5000/get-users";
      axios.get(path)
        .then(res => {
          this.msg = res.data;
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getThisUserInfo(user_id) {
      const path = "http://localhost:5000/get-users/"+user_id;
      axios.get(path)
        .then(res => {
          this.thisUser = res.data["users"][0];
          this.calculateStatus(user_id);
        }).then(() => {
          this.getTodayMeals(user_id);
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getMeals() {
      const path = "http://localhost:5000/get-meals";
      axios.get(path)
        .then(res => {
          this.allPastMeals = res.data["meals"];
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getTodayMeals(user_id) {
      const path = "http://localhost:5000/get-today-meals/"+ user_id;
      axios.get(path)
        .then(res => {
          this.todayMeals = res.data["meals"];
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addMeal() {
      if (this.currentMeal.user_id){
        var payload = {"text":this.currentMeal.text, "user_id": this.currentMeal.user_id, "num_calories": this.currentMeal.numCalories}
      } else {
      var payload = {"text":this.currentMeal.text, "user_id": store.thisUser.id, "num_calories": this.currentMeal.numCalories}
    }
      console.log(payload)
      const path = 'http://localhost:5000/add-meal';
      axios.post(path, payload)
        .then((res) => {
          if (res.data["status"]!="success"){
            console.log("ERRRR")
            this.error=true
          }
          console.log(res.data)
          this.saved = true
          return axios.get("http://localhost:5000/get-today-meals/" + store.thisUser.id) // Chain requests
        }).then((res) =>  {
          this.todayMeals = res.data["meals"];
          this.calculateStatus(store.thisUser.id);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
    onSubmit() {
      alert("YAY")
    },
    calculateStatus(user_id){
    const path = 'http://localhost:5000/calculate-status/'+user_id;
    axios.get(path)
      .then(res => {
        this.status = res.data["status"];
        this.caloriesBalance = res.data["calories_balance"];
      })
      .catch(error => {
        // eslint-disable-next-line
        console.error(error);
      });
    }
      //   var totalToday = 0
      //   for (var i = 0; i < this.todayMeals.length; i++){
      //     totalToday += this.todayMeals[i].num_calories
      //   }
      //   this.totalToday = totalToday
      //   console.log("TOTaltoday", this.totalToday, this.todayMeals)
      //
      //   if (this.totalToday <= this.thisUser.expected_calories) {
      //      this.status = "Green"
      //   } else {
      //     this.status = "Red"
      //   }
      //   console.log(this.totalToday, this.thisUser.expected_calories, this.status)
      // }
  },
  created() {

    if (store.thisUser){
    this.calculateStatus(store.thisUser.id);
    this.getTodayMeals(store.thisUser.id);
  }
}
};
</script>

<style>
.btn-group-xs > .btn, .btn-xs {
  padding: .1rem .4rem;
  font-size: .875rem;
  line-height: .5;
  border-radius: .2rem;
}
</style>
