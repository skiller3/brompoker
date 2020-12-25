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
          authenticated
        }
      },
      render: h => h(App)
    }).$mount('#app')
  }, 
  function() {
    document.write("Failed to check current authentication status and mount application!")
  }
)
