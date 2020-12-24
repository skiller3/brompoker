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
