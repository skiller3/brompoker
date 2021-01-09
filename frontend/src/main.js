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


window.initClubListSubscription = function() {
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
}

window.initGameListSubscription = function(clubId) {
  window.gameSocket = dao.subscribeToGameList(clubId)
  window.gameSocket.onmessage = function(event) {
    console.log(`Game socket message received: ${event}`)
  }
  window.gameSocket.onclose = function() {
    console.error('Game socket closed')
  }
  window.gameSocket.onerror = function() {
    console.error('Game socket received error')
  }
  window.gameSocket.onopen = function(){
    console.log('Game socket opened')
  }
}

window.initSessionListSubscription = function(clubId) {
  window.sessionSocket = dao.subscribeToSessionList(clubId)
  window.sessionSocket.onmessage = function(event) {
    console.log(`Session socket message received: ${event}`)
  }
  window.sessionSocket.onclose = function() {
    console.error('Session socket closed')
  }
  window.sessionSocket.onerror = function() {
    console.error('Session socket received error')
  }
  window.sessionSocket.onopen = function(){
    console.log('Session socket opened')
  }
}

window.tryCloseSocket = function(ws) {
  if (ws === undefined || ws.readyState === WebSocket.CLOSING || ws.readyState === WebSocket.CLOSED) {
    return
  }
  try {
    ws.close()
  }
  catch (e) {
    console.error(`Failed to close web socket: ${e.message}`)
  }
}

dao.isAuthenticated(
  function(authenticated) {
    window.vue = new Vue({
      router,
      vuetify,
      data: function() {
        return { 
          authenticated,
          selectedClub: null,
          selectedTab: null,

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
      },
      watch: {
        clubs(val) {
          if (val.length) {
            if (localStorage.lastSelectedClubId !== undefined && this.clubs.map(c => c.id).includes(localStorage.lastSelectedClubId)) {
              this.$router.push(`/club/${localStorage.lastSelectedClubId}/games`)
            }
            else {
              this.$router.push(`/club/${this.clubs[0].id}/games`)
            }
          }
        },
        selectedClub(newclub) {
          window.tryCloseSocket(window.gameSocket)
          window.tryCloseSocket(window.sessionSocket)
          this.games.splice(0, this.games.length)
          this.sessions.splice(0, this.sessions.length)
          if (this.selectedTab === 'games') {
            window.initGameListSubscription(newclub.id);
          }
          if (this.selectedTab === 'sessions') {
            window.initSessionListSubscription(newclub.id);
          }
        },
        selectedTab(newtab) {
          window.tryCloseSocket(window.gameSocket)
          window.tryCloseSocket(window.sessionSocket)
          if (newtab === 'games') {
            this.games.splice(0, this.games.length)
            this.sessions.splice(0, this.sessions.length)
            window.initGameListSubscription(this.selectedClub.id);
          }
          if (newtab === 'sessions') {
            this.games.splice(0, this.games.length)
            this.sessions.splice(0, this.sessions.length)
            window.initSessionListSubscription(this.selectedClub.id);
          }
        }
      }
    })
    window.vue.$mount('#app')
    window.initClubListSubscription()
  }, 
  function() {
    document.write("Failed to check current authentication status and mount application!")
  }
)
