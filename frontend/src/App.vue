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
      <!--
      <router-link to="/games">Games</router-link>
      <span class="bar-sep">|</span>
      <router-link to="/session-history">Ledger</router-link>
      <span class="bar-sep">|</span>
      <v-icon medium>mdi-github</v-icon>
      <a href="https://github.com/skiller3/brompoker">
        Source Code
      </a>
      -->
      <!-- <span style="display: inline"> -->
      <h4 class="poker-club-label">Poker Club:</h4>
      <v-menu offset-y>
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            color="primary"
            v-bind="attrs"
            v-on="on">
            Public Games
            <v-icon medium right>
              mdi-menu-down
            </v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item @click="() => this.showImageUploadDialog = true">
            <v-list-item-icon class="new-club-icon"><v-icon medium>mdi-plus</v-icon></v-list-item-icon>
            <v-list-item-title>New Club</v-list-item-title>
          </v-list-item>
          <v-divider></v-divider>
          <v-list-item @click="() => this.showImageUploadDialog = true">
            <v-list-item-title>Public Games</v-list-item-title>
          </v-list-item>
          <v-list-item @click="() => this.showPasswordChangeDialog = true">
            <v-list-item-title>Skye's Home Game</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
      <!-- </span> -->
      <span class="bar-sep">|</span>
      <!-- <v-spacer></v-spacer> -->
      <v-btn
        color="primary"
        v-bind="attrs"
        v-on="on"
        class="new-club-button">
        <v-icon medium left>mdi-plus-circle</v-icon>
          New Club
      </v-btn>
      <v-btn tile class="github-link" href="https://github.com/skiller3/brompoker">
        <v-icon left>
          mdi-github
        </v-icon>
        GITHUB
      </v-btn>
      <v-menu offset-y>
        <template v-slot:activator="{ on, attrs }">
          <v-avatar color="rgb(39, 39, 39)"
             v-bind="attrs"
             v-on="on"
             class="profile-menu">
              <v-icon x-large dark center>
                mdi-account-circle
              </v-icon>
              <v-icon medium>
                mdi-menu-down
              </v-icon>
          </v-avatar>
        </template>
        <v-list>
          <v-list-item @click="() => this.showImageUploadDialog = true">
            <v-list-item-icon><v-icon>mdi-image-multiple-outline</v-icon></v-list-item-icon>
            <v-list-item-title>Upload Avatar Image</v-list-item-title>
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

      <template v-if="this.$root.authenticated" v-slot:extension>
        <v-tabs centered>
          <v-tab>Games</v-tab>
          <v-tab>Ledger</v-tab>
        </v-tabs>
      </template>

    </v-app-bar>
    <v-main>
      <ImageUploadDialog v-if="showImageUploadDialog"></ImageUploadDialog>
      <PasswordChangeDialog v-if="showPasswordChangeDialog"></PasswordChangeDialog>
      <LoginDialog v-if="!this.$root.authenticated"></LoginDialog>
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
  .v-menu__content {
    border: 1px solid #2196f3;
  }
  .logo {
    flex: none !important;
    margin-right: 10px;
  }
  .bar-sep {
    margin-left: 1em;
    margin-right: 1em;
    font-weight: bold;
  }
  .router-link-active {
    color: yellow !important;
  }
  /*
  .v-avatar > .v-icon {
    border: 2px solid white;
  }
  */
  /*
  button.v-app-bar__nav-icon {
    border: 1px solid white;
    border-radius: 4px;
    margin-right: 0.5em !important;
  }
  */
  .profile-menu {
    width: 4em !important;
    min-width: 4em !important;
  }
  a.github-link {
    border: 1px solid white;
    border-radius: 4px;
    margin-right: 1em;
  }
  .poker-club-label {
    margin-right: 1em;
  }
  .new-club-button {
    margin-right: 1em;
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

