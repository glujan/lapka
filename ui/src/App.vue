<template>
  <div id="app" class="container">
    <status-header class="row" :userId="userId"></status-header>
    <img src="./assets/logo.png">
    <div class="row">
      <router-view :userId="userId"></router-view>
    </div>
    <footer class="row">
      <div class="six columns">
        Left column
      </div>
      <div class="six columns">
        Right column
      </div>
    </footer>
  </div>
</template>

<script>
import StatusHeader from '@/components/StatusHeader'

export default {
  name: 'app',
  components: {
    'status-header': StatusHeader
  },
  data: () => {
    return {userId: 'user-id'}  // TODO Use real user id
  }
}
</script>

<style>
@import './assets/css/normalize.css';
@import './assets/css/skeleton.css';

#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
}
</style>
