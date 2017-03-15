import Vue from 'vue'
import Router from 'vue-router'
import AnimalProfile from '@/components/AnimalProfile'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'AnimalProfile',
      component: AnimalProfile
    }
  ]
})
