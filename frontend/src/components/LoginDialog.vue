<!--
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
-->
<template>
  <v-dialog v-model="this.$root.showLoginDialog" persistent width="50vw" v-bind:class="{'v-dialog-error': error}">
    <v-card>
      <v-card-title class="headline">Authenticate</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="login">
          <v-row>
            <v-col>
              <v-text-field
                hide-details
                prepend-icon="mdi-account-circle"
                single-line
                label="Username"
                v-model="username"
                :error="error"
              />
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-text-field
                hide-details
                prepend-icon="mdi-lock"
                single-line
                label="Password"
                type="password"
                v-model="password"
                :error="error"
              />
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-btn type="submit">Submit</v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<style>

.v-dialog-error {
    border: 1px solid red;
}

</style>

<script>
import dao from '../dao'

export default {

  data() {
    return {
      username: '',
      password: '',
      error: false
    }
  },
  computed: {
    visible() {
      return !this.$root.authenticated
    }
  },
  watch: {
    error: function(error) {
        if (error) {
            document.querySelector(".v-dialog--active").style.borderColor = "red"
        }
        else{
            document.querySelector(".v-dialog--active").style.borderColor = "#2196f3"
        }
    },
    visible: function(visible) {
      if (!visible) {
        // Force the closing of the overlay masks
        document.getElementsByClassName("v-overlay").forEach(function(el) {el.remove()})
      }
    }
  }, 
  methods: {
    login() {
        const $this = this
        dao.authenticate(
            $this.username,
            $this.password,
            function() {
                $this.error = false
                $this.$root.authenticated = true
            },
            function() {
                $this.error = true
            }
        )
        $this.password = ''
    }
  }
}
</script>