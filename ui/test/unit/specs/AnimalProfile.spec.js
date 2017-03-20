/* global jasmine beforeAll afterAll spyOn */
import Vue from 'vue'
import axios from 'axios'
import moxios from 'moxios'

import AnimalProfile from '@/components/AnimalProfile'

describe('AnimalProfile.vue', () => {
  var animal, next, matching, vm
  var resp200 = {status: 200, responseText: 'ok'}
  const Constructor = Vue.extend(AnimalProfile)
  const userId = 'userid'

  beforeAll(() => {
    moxios.install()
    axios.defaults.baseURL = '/'
  })

  afterAll(() => {
    moxios.uninstall()
  })

  beforeEach(() => {
    next = null
    matching = []
    animal = {id: 'some-id', name: 'Doggy', age: 10, description: ['line1', 'line2'], place: 'City', photos: ['http://example.com/photo1', 'http://example.com/photo2']}
    vm = new Constructor({
      data: () => {
        return {animal: animal, next: next, matching: matching}
      },
      propsData: {userId: userId}
    })
  })

  it('should fetch matching and show first animal on mounted', (done) => {
    moxios.stubRequest('/animal/matching/userid/', resp200)
    spyOn(vm, '_fetchMatching').and.callThrough()
    spyOn(vm, 'seeNext')
    spyOn(axios, 'get').and.callThrough()

    vm.$mount()
    Vue.nextTick(() => {
      moxios.wait(() => {
        expect(axios.get).toHaveBeenCalledWith('animal/matching/userid/')
        expect(vm._fetchMatching).toHaveBeenCalledTimes(1)
        expect(vm.seeNext).toHaveBeenCalledTimes(1)
        done()
      })
    })
  })

  it('should send a like, notify a user and switch to next animal', () => {
    spyOn(vm, 'seeNext')
    spyOn(axios, 'post')
    spyOn(console, 'info')

    vm.like('animal-id')
    vm.userId = 'user-id'
    expect(vm.seeNext).toHaveBeenCalledTimes(1)
    expect(console.info).toHaveBeenCalledTimes(1)
    expect(axios.post).toHaveBeenCalledTimes(1)
    expect(axios.post).toHaveBeenCalledWith('animal/some-id/like/userid/')
  })

  it('should render correct name', done => {
    spyOn(vm, '_fetchMatching')

    vm.$mount()
    Vue.nextTick(() => {
      expect(vm.$el.querySelector('div h4').textContent)
        .toBe(animal.name)
      done()
    })
  })

  it('should _get data', done => {
    moxios.stubRequest('/get-ok/', resp200)

    let onSuccess = jasmine.createSpy('onSuccess')
    spyOn(axios, 'get').and.callThrough()

    vm._get('get-ok', onSuccess)
    moxios.wait(() => {
      expect(onSuccess).toHaveBeenCalledTimes(1)
      expect(axios.get).toHaveBeenCalledTimes(1)
      expect(axios.get).toHaveBeenCalledWith('get-ok/')
      let resp = onSuccess.calls.argsFor(0)[0]
      expect(resp.data).toBe('ok')
      expect(resp.status).toBe(200)
      done()
    })
  })

  it("should notify user when can't _get data", (done) => {
    moxios.stubRequest('/get-err/', {status: 500})
    spyOn(console, 'warn')
    spyOn(axios, 'get').and.callThrough()

    let onSuccess = jasmine.createSpy('onSuccess')
    vm._get('get-err', onSuccess)
    moxios.wait(() => {
      expect(onSuccess).toHaveBeenCalledTimes(0)
      expect(axios.get).toHaveBeenCalledTimes(1)
      expect(console.warn).toHaveBeenCalledTimes(1)
      done()
    })
  })

  describe('fetchNext', () => {
    it('should return if there already is next', () => {
      next = {some: 'object'}
      spyOn(matching, 'shift').and.callThrough()
      let vm = new Constructor({
        data: () => {
          return {next: next, animal: animal, matching: matching}
        },
        propsData: {userId: userId}
      })

      Vue.nextTick(() => {
        vm.fetchNext()
        expect(matching.shift).toHaveBeenCalledTimes(0)
      })
    })

    it('should return if no next and no matching', (done) => {
      spyOn(matching, 'shift').and.callThrough()
      spyOn(axios, 'get').and.callThrough()

      vm.fetchNext()
      expect(matching.shift).toHaveBeenCalledTimes(1)
      expect(axios.get).toHaveBeenCalledTimes(0)
      done()
    })

    it('should fetch if no next but matching with callback', (done) => {
      matching = ['some-uid']
      moxios.stubRequest('/animal/some-uid/', resp200)
      let onSuccess = jasmine.createSpy('onSuccess')
      let vm = new Constructor({
        data: () => {
          return {next: next, animal: animal, matching: matching}
        },
        propsData: {userId: userId}
      })
      spyOn(matching, 'shift').and.callThrough()
      spyOn(axios, 'get').and.callThrough()

      Vue.nextTick(() => {
        vm.fetchNext(onSuccess)
        moxios.wait(() => {
          expect(matching.shift).toHaveBeenCalledTimes(1)
          expect(axios.get).toHaveBeenCalledWith('animal/some-uid/')
          expect(onSuccess).toHaveBeenCalledTimes(1)
          done()
        })
      })
    })

    it('should fetch if no next but matching without callback', (done) => {
      matching = ['some-uid']
      moxios.stubRequest('/animal/some-uid/', resp200)
      let vm = new Constructor({
        data: () => {
          return {next: next, animal: animal, matching: matching}
        },
        propsData: {userId: userId}
      })
      spyOn(matching, 'shift').and.callThrough()
      spyOn(axios, 'get').and.callThrough()

      Vue.nextTick(() => {
        vm.fetchNext()
        moxios.wait(() => {
          expect(matching.shift).toHaveBeenCalledTimes(1)
          expect(axios.get).toHaveBeenCalledWith('animal/some-uid/')
          done()
        })
      })
    })
  })

  describe('_fetchMatching', () => {
    beforeEach(() => {
      spyOn(axios, 'get').and.callThrough()
    })

    it('should fetch without callback', (done) => {
      moxios.stubRequest('/animal/matching/userid/', resp200)

      Vue.nextTick(() => {
        vm._fetchMatching()
        moxios.wait(() => {
          expect(axios.get).toHaveBeenCalledTimes(1)
          expect(axios.get).toHaveBeenCalledWith('animal/matching/userid/')
          done()
        })
      })
    })

    it('should fetch with callback', (done) => {
      moxios.stubRequest('/animal/matching/userid/', resp200)
      let onSuccess = jasmine.createSpy('onSuccess')

      Vue.nextTick(() => {
        vm._fetchMatching(onSuccess)
        moxios.wait(() => {
          expect(axios.get).toHaveBeenCalledTimes(1)
          expect(axios.get).toHaveBeenCalledWith('animal/matching/userid/')
          expect(onSuccess).toHaveBeenCalledTimes(1)
          done()
        })
      })
    })
  })

  describe('seeNext', () => {
    it('should mark current animal as seen', (done) => {
      moxios.stubRequest('/animal/some-id/skip/userid/', resp200)
      spyOn(axios, 'post')

      Vue.nextTick(() => {
        vm.seeNext()
        moxios.wait(() => {
          expect(axios.post).toHaveBeenCalledTimes(1)
          expect(axios.post).toHaveBeenCalledWith('animal/some-id/skip/userid/')
          done()
        })
      })
    })

    it('should fetch next and then switch', (done) => {
      moxios.stubRequest('/animal/animal-id/', {status: 200, responseText: animal})
      matching = ['animal-id']
      let vm = new Constructor({
        data: () => {
          return {next: next, animal: {}, matching: matching}
        },
        propsData: {userId: userId}
      })

      spyOn(vm, 'fetchNext').and.callThrough()
      spyOn(axios, 'get').and.callThrough()

      Vue.nextTick(() => {
        vm.seeNext()
        moxios.wait(() => {
          expect(vm.fetchNext).toHaveBeenCalledTimes(1)
          expect(axios.get).toHaveBeenCalledTimes(1)
          expect(axios.get).toHaveBeenCalledWith('animal/animal-id/')
          expect(vm.$data.animal).toBe(animal)
          done()
        })
      })
    })

    it('should switch to next', (done) => {
      next = animal
      let vm = new Constructor({
        data: () => {
          return {next: next, animal: {}, matching: matching}
        },
        propsData: {userId: userId}
      })

      spyOn(axios, 'get').and.callThrough()

      Vue.nextTick(() => {
        vm.seeNext()
        moxios.wait(() => {
          expect(axios.get).toHaveBeenCalledTimes(0)
          expect(vm.$data.animal).toBe(animal)
          done()
        })
      })
    })
  })
})
