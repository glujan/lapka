<template>
    <div class="twelve columns">
        <h4>{{ animal.name }}</h4>
        <img v-if="animal.photos.length > 0" :src="animal.photos[0]"/>
        <p>{{ animal.name }} is here since {{ animal.since }} and can be adopted in {{ animal.place }}.</p>
        <p v-for="(par, index) in animal.description">{{ par }}</p>
        <ul @mouseover.stop="fetchNext()">
            <li><a href="#like" @click.prevent="like">Like</a></li>
            <li><a href="#skip" @click.prevent="seeNext">Skip</a></li>
        </ul>
    </div>
</template>

<script>
function httpError (url) {
  return function (error) {
    console.warn('Could not fetch data from', url, ':', error)
  }
}
var animalData = {
  id: '',
  name: '',
  age: 0,
  place: '',
  description: [],
  photos: []
}

import axios from 'axios'

export default {
  name: 'animal-profile',
  data () {
    return {
      animal: animalData,
      next: null,
      matching: []  // list of animals ids
      // lru: {}
    }
  },
  props: {
    userId: {type: String, required: true}
  },
  methods: {
    _get: function (url, success) {
      var queryUrl = url + '/'
      axios.get(queryUrl)
        .then(success)
        .catch(httpError(queryUrl))
    },
    _fetchMatching: function (success) {
      var $this = this
      var url = 'animal/matching/' + this.userId
      this._get(url, function (resp) {
        $this.matching = resp.data
        if (typeof success === 'function') {
          success(resp)
        }
      })
    },
    like: function () {
      var uid = this.animal.id
      axios.post('animal/' + uid + '/like/' + this.userId + '/')
      console.info('Liked ' + uid)  // TODO Implement notyfing user
      this.seeNext()
    },
    seeNext: function () {
      var $this = this

      function switchAnimals () {
        $this.animal = $this.next
        $this.next = null
      }

      if (this.animal.id) {
        axios.post('animal/' + this.animal.id + '/skip/' + this.userId + '/')
      }

      if (this.next === null) {
        this.fetchNext(switchAnimals)
      } else {
        switchAnimals()
      }
    },
    fetchNext: function (success) {
      if (this.next !== null) {
        return
      }

      var $this = this
      var uid = this.matching.shift()

      if (uid === undefined) {
        return
      }
      this._get('animal/' + uid, function (resp) {
        $this.next = resp.data
        if (typeof success === 'function') {
          success(resp)
        }
      })
    }
  },
  mounted: function () {
    let $this = this
    this._fetchMatching(() => {
      $this.seeNext()
    })
  }
}
</script>

<style>
</style>
