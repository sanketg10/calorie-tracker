<template>
  <div class="test">
    <p>{{ msg }}</p>
  </div>
</template>

<script>

import axios from "axios";

export default {
  /* eslint-disable */
  name: "test",
  data() {
    return {
      msg: "",
    };
  },
  methods: {
    getMessage() {
      const path = "http://localhost:5000/test";
      axios.get(path)
        .then(res => {
          this.msg = res.data;
          console.log(this.msg)
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
    }
  },
  created() {
    this.getMessage();
  }
};
</script>
