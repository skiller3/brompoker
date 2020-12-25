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
  <v-app>
    <v-app-bar>
      <v-img :src="require('./assets/logo.svg')"
        contain
        height="50"
        width="50"
        class="logo"
      />
      <v-toolbar-title>Brompoker</v-toolbar-title>
      <v-spacer></v-spacer>
      <router-link to="/games">Games</router-link>
      <span class="bar-sep">|</span>
      <router-link to="/session-history">Ledger</router-link>
      <span class="bar-sep">|</span>
      <v-menu offset-y>
        <template v-slot:activator="{ on, attrs }">
          <!--
          <v-avatar color="rgb(39, 39, 39)"
             v-bind="attrs"
             v-on="on">
            <v-icon x-large dark>
              mdi-account-circle
            </v-icon>
          </v-avatar>
          -->
          <v-app-bar-nav-icon
             v-bind="attrs"
             v-on="on">
          </v-app-bar-nav-icon>
        </template>
        <v-list>
          <v-list-item href="https://github.com/skiller3/brompoker">
            <v-list-item-icon><v-icon>mdi-github</v-icon></v-list-item-icon>
            <v-list-item-title>Source Code</v-list-item-title>
          </v-list-item>
          <v-list-item @click="() => this.showImageUploadDialog = true">
            <v-list-item-icon><v-icon>mdi-image</v-icon></v-list-item-icon>
            <v-list-item-title>Upload Table Image</v-list-item-title>
          </v-list-item>
          <v-list-item @click="() => this.showPasswordChangeDialog = true">
            <v-list-item-icon><v-icon>mdi-lock-reset</v-icon></v-list-item-icon>
            <v-list-item-title>Change Password</v-list-item-title>
          </v-list-item>
          <v-list-item @click="logout">
            <v-list-item-icon><v-icon>mdi-exit-run</v-icon></v-list-item-icon>
            <v-list-item-title>Log Out</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>
    <v-main>
      <ImageUploadDialog v-if="showImageUploadDialog"></ImageUploadDialog>
      <PasswordChangeDialog v-if="showPasswordChangeDialog"></PasswordChangeDialog>
      <LoginDialog v-if="!authenticated"></LoginDialog>
      <router-view v-else></router-view>
    </v-main>
  </v-app>
</template>

<style>
  .v-app-bar { /* Probably not the best way to fix a sizing problem, but worked... */
    position: relative;
    max-height: 65px;
  }
  .v-toolbar__title {
    font-size: 1.5em;
    font-weight: bold;
  }
  .v-overlay__scrim {
    opacity: 0.8 !important;
  }
  .v-dialog--active {
    border: 1px solid #2196f3;
  }
  .v-text-field__slot > label {
    color: rgb(100, 100, 100) !important;
  }
  .logo {
    flex: none !important;
    margin-right: 10px;
  }
  .bar-sep {
    margin-left: 10px;
    margin-right: 10px;
  }
  .router-link-active {
    color: yellow !important;
  }
  /*
  .v-avatar > .v-icon {
    border: 2px solid white;
  }
  */
  button.v-app-bar__nav-icon {
    border: 1px solid white;
    border-radius: 4px;
    margin-right: 0.5em !important;
  }

</style>

<script>
import dao from './dao'
import ImageUploadDialog from './components/ImageUploadDialog';
import PasswordChangeDialog from './components/PasswordChangeDialog';
import LoginDialog from './components/LoginDialog';


function removeOverlays() {
  document.getElementsByClassName("v-overlay").forEach(el => el.remove())
}

export default {
  name: 'App',

  components: {
    ImageUploadDialog,
    PasswordChangeDialog,
    LoginDialog
  },

  data: () => ({
    showImageUploadDialog: false,
    showPasswordChangeDialog: false
  }),

  computed: {
    authenticated() {
      return this.$root.authenticated
    }
  },

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
    // Dirty hacks to remove dialog overlay masks to work around a Vuetify bug
    authenticated: (v) => {if (v) removeOverlays()},
    showImageUploadDialog: (v) => {if (!v) removeOverlays()},
    showChangePasswordDialog: (v) => {if (!v) removeOverlays()}
  }

};
</script>

