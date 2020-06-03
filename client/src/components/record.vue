<template>
  <div class="record">
  <p>
    <span class="field-value" v-show="!showField('name')" @click="focusField('name')">{{user.name}}</span>
    <input v-model="user.name" v-show="showField('name')" id="user-name" type="text" class="field-value form-control" @focus="focusField('name')" @blur="blurField">
    </span>
  </p>
  </div>

</template>
