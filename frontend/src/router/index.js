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
import VueRouter from 'vue-router'
import Games from '../components/Games'
import Ledger from '../components/Ledger'

Vue.use(VueRouter)

const routes = [
  {
    path: '*',
    redirect: '/club'
  },
  {
    path: '/club/:clubid/games',
    name: 'Games',
    component: Games,
    beforeEnter(to, from, next) {
      if (window.vue === undefined) {
        // The vue instance may not be defined on initial page load or
        // refresh...
        next('/club')
      }
      else {
        window.vue.selectedClub = window.vue.clubs.filter(c => c.id == to.params.clubid)[0]
        localStorage.lastSelectedClubId = to.params.clubid
        window.vue.selectedTab = 'games'
        next()
      }
    }
  },
  {
    path: '/club/:clubid/ledger',
    name: 'Ledger',
    component: Ledger,
    beforeEnter(to, from, next) {
      if (window.vue === undefined) {
        // The vue instance may not be defined on initial page load or
        // refresh...
        next('/club')
      }
      else {
        window.vue.selectedClub = window.vue.clubs.filter(c => c.id == to.params.clubid)[0]
        localStorage.lastSelectedClubId = to.params.clubid
        window.vue.selectedTab = 'ledger'
        next()
      }
    }
  }
]

const router = new VueRouter({
  routes
})

export default router
