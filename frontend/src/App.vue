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
    <AppBar></AppBar>
    <v-main>
      <!-- <ImageUploadDialog></ImageUploadDialog> -->
      <PasswordChangeDialog></PasswordChangeDialog>
      <LoginDialog></LoginDialog>
      <v-tabs centered>
        <v-tab>Games</v-tab>
        <v-tab>Ledger</v-tab>
      </v-tabs>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<style>
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
</style>

<script>
import AppBar from './components/AppBar'
// import ImageUploadDialog from './components/ImageUploadDialog'
import PasswordChangeDialog from './components/PasswordChangeDialog'
import LoginDialog from './components/LoginDialog'

export default {
  name: 'App',

  components: {
    AppBar,
    // ImageUploadDialog,
    PasswordChangeDialog,
    LoginDialog
  }
};
</script>

