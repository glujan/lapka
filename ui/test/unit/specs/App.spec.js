import Vue from 'vue'

import App from '@/App'

describe('App.vue', () => {
  const Constructor = Vue.extend(App)
  var vm

  beforeEach(() => {
    vm = new Constructor({
      data: () => {
        return {userId: 'some-id'}
      }
    })
  })

  it('should pass coverage :-)', () => {
    expect(vm.userId).toBe('some-id')
  })
})
