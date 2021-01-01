/*
 Copyright 2020 Skye Isard

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
*/
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
import VueCookies from 'vue-cookies'
import ImageUploader from 'vue-image-upload-resize'
import dao from './dao'


Vue.config.devtools = true
Vue.config.productionTip = true

Vue.use(VueCookies)
Vue.use(ImageUploader)


dao.isAuthenticated(
  function(authenticated) {
    window.vue = new Vue({
      router,
      vuetify,
      data: function() {
        return { 
          authenticated,
          selectedClub: null,

          showImageUploadDialog: false,
          showPasswordChangeDialog: false,

          clubs: [],
          games: [],
          sessions: []
        }
      },
      computed: {
        showLoginDialog() {
          return !this.authenticated
        }
      },
      render: h => h(App),
      methods: {
        logout() {
          dao.logout(
            () => {
              console.log("Successfully logged out via server!")
              this.$root.authenticated = false          
            },
            () => {
              console.log("Failed to log out via server!") 
            }
          )
        }
      }
    })

    window.vue.$mount('#app')

    window.clubSocket = dao.subscribeToClubList()
    window.clubSocket.onmessage = function(event) {
      const payload = JSON.parse(event.data)
      if (payload.type === 'CREATE_CLUBS') {
        payload.data.forEach((club) => {
          if (!window.vue.clubs.map(c => c.id).includes(club.id)) {
            window.vue.clubs.push(club)
          }
        })
      }
      if (payload.type === 'UPDATE_CLUBS') {
        payload.data.forEach((club) => {
          for (var i = 0; i < window.vue.clubs.length; i++) {
            if (window.vue.clubs[i].id === club.id) {
              window.vue.clubs[i] = club
            }
          }
        })
      }
      if (payload.type === 'DELETE_CLUBS') {
        payload.data.forEach((club) => {
          window.vue.clubs = window.vue.clubs.filter(c => c.id !== club.id)
        })
      }
    }
    window.clubSocket.onclose = function() {
      console.error('Club socket closed')
    }
    window.clubSocket.onerror = function() {
      console.error('Club socket received error')
    }
    window.clubSocket.onopen = function(){
      console.log('Club socket opened')
    }
  }, 
  function() {
    document.write("Failed to check current authentication status and mount application!")
  }
)
