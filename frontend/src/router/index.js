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
import Games from '../views/Games'
import SessionHistory from '../views/SessionHistory'

// import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [
  /*
  {
    path: '/',
    redirect: '/home'
  },
  {
    path: '/home',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
  */
  //  component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  /*
  }
  */
  {
    path: '/',
    redirect: '/games'
  },
  {
    path: '/games',
    name: 'Games',
    component: Games
  },
  {
    path: '/session-history',
    name: 'Session History',
    component: SessionHistory
  }
]

const router = new VueRouter({
  routes
})

export default router
