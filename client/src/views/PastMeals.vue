<template>
  <div class="past_meals">
    <div v-if="!isLoggedIn">
      <h4>You can filter your past meals here.</h4>
      <h5 class="mt-5">But first please sign up/ log in first, to access the application.</h5>
      <div><button class="btn-lg btn-warning mt-5" @click="login()">Login</button></div>
      <div><button class="btn-lg btn-success mt-3" @click="signup()">Sign Up!</button></div>
    </div>
    <div v-if="isLoggedIn">
      <h4 class="mb-3"> Hi {{ thisUser.name.split(" ")[0] }}, you can filter and edit your past meals here.</h4>
    <button class="btn-lg btn-primary mb-5" @click="showFilters(filteredStatus)">Filter The Meals</button>
    <form class="form-horizontal">
    <div v-if="filteredStatus" class="form-group">
        <div class="input-group col-md-4 offset-md-4">
            <input class="form-control border h3 ml-3 "  type="text" v-model="date_from" placeholder="Date From" >
          <input class="form-control border h3 ml-3" type="text" v-model="date_to" placeholder="Date To" >
        </div>
          <div class="input-group col-md-4 offset-md-4">
          <input class="form-control border h3 ml-3 mt-3" type="text" v-model="time_from" placeholder="Time From" >
          <input class="form-control border h3 ml-3 mt-3" type="text" v-model="time_to" placeholder="Time To" >
        </div>
        <button @click="filterMeals()" class="btn-success btn mt-3" type="button">
            <b>Submit</b>
        </button>
    </div>
    </form>
    <h4 v-if="!filteredStatus">All your past meals are:</h4>
    <h4 v-if="filteredStatus">Your filtered meals are:</h4>
    <div v-if="!filteredStatus" v-for="(meal,index) in allPastMeals">
       <div class="mt-2" v-if="currentlyEditingStatus===false || meal.id!=currentlyEditingId">
        <span style="color:green;" v-if="meal.status==='within_limit'">{{ index+1 }}. {{ meal.text }} with {{ meal.num_calories}} calories at {{ meal.datetime | formatDate}}</span>
        <span style="color:red;" v-if="meal.status==='exceeded_limit'">{{ index+1 }}. {{ meal.text }} with {{ meal.num_calories}} calories at {{ meal.datetime | formatDate}}</span>
          <button class="btn-sm btn-info ml-3" @click="updateCurrentlyEditing(meal.id, true)">Edit</button>  <button class="btn-sm btn-danger ml-1" @click="deleteCurrentMeal(meal.id)">Delete</button>
        </div>
        <div class="mt-2" v-else-if="meal.id===currentlyEditingId && currentlyEditingStatus===true">
          <div class="form-group row">
            <p class="offset-md-4">{{ index + 1}}. </p>
          <input class="input-sm form-control border h3 col-md-2 ml-2"  type="text" v-model="currentlyEditingRecord.text">
          <input class="input-sm form-control border h3 col-md-2 ml-2"  type="text" v-model="currentlyEditingRecord.numCalories">
           <button class="btn btn-xs btn-success ml-3" @click="updateCurrentlyEditing(meal.id, false)">Save</button>
          </div>
        </div>
    </div>
    <div v-if="filteredStatus" v-for="(meal,index) in filteredMeals">
       <div class="mt-2" v-if="currentlyEditingStatus===false || meal.id!=currentlyEditingId">
        {{ index+1 }}. {{ meal.text }} with {{ meal.num_calories}} calories at {{ meal.datetime | formatDate}} <button class="btn-sm btn-info ml-3" @click="updateCurrentlyEditing(meal.id, true)">Edit</button>  <button class="btn-sm btn-danger ml-1" @click="deleteCurrentMeal(meal.id)">Delete</button>
        </div>
        <div class="mt-2" v-else-if="meal.id===currentlyEditingId && currentlyEditingStatus===true">
          <div class="form-group row">
            <p class="offset-md-4">{{ index + 1}}. </p>
          <input class="input-sm form-control border h3 col-md-2 ml-2"  type="text" v-model="currentlyEditingRecord.text">
          <input class="input-sm form-control border h3 col-md-2 ml-2"  type="text" v-model="currentlyEditingRecord.numCalories">
           <button class="btn btn-xs btn-success ml-3" @click="updateCurrentlyEditing(meal.id, false)">Save</button>
          </div>
        </div>
    </div>
  </div>
    <!-- <home-component></home-component> -->
    <!-- Reuse information by using components from other pages -->
  </div>
</template>

<script>

import axios from "axios";
// import Home from "./Home.vue"; // To reuse components
import { store } from "../store.js";

export default {
  // components: {
  //   'home-component': Home
  // },
  /* eslint-disable */
  name: "pastMeals",
  data() {
    return {
      allPastMeals: [],
      filteredMeals: [],
      currentlyEditingId: null,
      currentlyEditingStatus: false,
      currentlyEditingRecord: {"text": "", "numCalories": null},
      filteredStatus: false,
      date_from: "5 Sep 2019",
      date_to: "8 Sep 2019",
      time_from: "12 pm",
      time_to: "6 pm",
      isLoggedIn: store.isLoggedIn,
      thisUser: store.thisUser
        };
  },
  methods: {
    login() {
      this.$router.push('/login')
    },
    signup() {
      this.$router.push('/signup')
    },
    showFilters(current){
      this.filteredStatus = !current
    },
    filterMeals(){
      const path = "http://localhost:5000/filter-meals/"+ store.thisUser.id + "/"+ this.date_from +"/"+ this.date_to +"/"+ this.time_from +"/"+ this.time_to;
      axios.get(path)
        .then(res => {
          this.filteredMeals = res.data["meals"];
          this.filteredMeals.sort(function(a, b){
            var dateA=new Date(a.datetime), dateB=new Date(b.datetime)
            return dateA-dateB //sort by date ascending
      })
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    updateCurrentlyEditing(id, status) {
      this.currentlyEditingId = id
      // console.log("Currently editing", this.currentlyEditingIndex)
      this.currentlyEditingStatus = status
      if (status == true){
        // update currently editing record if the person presses Edit or Delete buttons
        for (var i=0; i < this.allPastMeals.length; i++) {
          if (this.allPastMeals[i].id == id) {
            this.currentlyEditingRecord.text = this.allPastMeals[i].text
            this.currentlyEditingRecord.numCalories = this.allPastMeals[i].num_calories
            this.currentlyEditingRecord.id = id
          }
        }
      } else {
        // make a post request to save the newly edited record
          var payload = {"id": this.currentlyEditingRecord.id,
                         "text":this.currentlyEditingRecord.text,
                         "user_id": store.thisUser.id,
                         "num_calories": this.currentlyEditingRecord.numCalories}
          // console.log(payload)
          const path = 'http://localhost:5000/add-meal';
          axios.put(path, payload)
            .then((res) => {
              console.log(res.data)
              return axios.get("http://localhost:5000/get-meals/" + store.thisUser.id) // Chain requests
            }).then((res) =>  {
              this.allPastMeals = res.data["meals"];
              this.allPastMeals.sort(function(a, b){
                var dateA=new Date(a.datetime), dateB=new Date(b.datetime)
                return dateA-dateB //sort by date ascending
              })
              this.filterMeals()
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
            return axios.get("http://localhost:5000/get-meals/" + store.thisUser.id) // Chain requests
          }).then((res) =>  {
            this.allPastMeals = res.data["meals"];
            this.allPastMeals.sort(function(a, b){
              var dateA=new Date(a.datetime), dateB=new Date(b.datetime)
              return dateA-dateB //sort by date ascending
        })
          this.filterMeals()
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.log(error);
          });
    },
    getMeals() {
      const path = "http://localhost:5000/get-meals/" + store.thisUser.id;
      axios.get(path)
        .then(res => {
          this.allPastMeals = res.data["meals"];
          this.allPastMeals.sort(function(a, b){
            var dateA=new Date(a.datetime), dateB=new Date(b.datetime)
            return dateA-dateB //sort by date ascending
      })
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
    }
  },
  created() {
  if (store.thisUser){
    this.getMeals();
  }
}
};
</script>
