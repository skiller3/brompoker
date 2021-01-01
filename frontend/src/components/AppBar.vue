<template>
    <v-app-bar>
      <v-img :src="require('../assets/logo.svg')"
        contain
        height="50"
        width="50"
        class="logo"
      />
      <v-toolbar-title>Brompoker</v-toolbar-title>
      <v-spacer></v-spacer>
      <h4 class="poker-club-label">Poker Club:</h4>
      <v-menu offset-y>
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            color="primary"
            v-bind="attrs"
            v-on="on"
            :disabled="$root.clubs.length < 1">
            {{ $root.selectedClub === null ? 'None' : $root.selectedClub.name }}
            <v-icon medium right>
              mdi-menu-down
            </v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item v-for="club in $root.clubs" :key="club.id" @click="() => console.log('club clicked')">
            <v-list-item-title>{{club.name}}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
      <span class="bar-sep">|</span>
      <v-btn
        color="primary"
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
          <v-list-item @click="() => this.$root.showImageUploadDialog = true">
            <v-list-item-icon><v-icon>mdi-image-multiple-outline</v-icon></v-list-item-icon>
            <v-list-item-title>Upload Avatar Image</v-list-item-title>
          </v-list-item>
          <v-list-item @click="() => this.$root.showPasswordChangeDialog = true">
            <v-list-item-icon><v-icon>mdi-lock-reset</v-icon></v-list-item-icon>
            <v-list-item-title>Change Password</v-list-item-title>
          </v-list-item>
          <v-list-item @click="this.$root.logout">
            <v-list-item-icon><v-icon>mdi-exit-run</v-icon></v-list-item-icon>
            <v-list-item-title>Log Out</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>
</template>

<style scoped>
  .v-app-bar { /* Probably not the best way to fix a sizing problem, but worked... */
    position: relative;
    max-height: 65px;
  }
  .v-toolbar__title {
    font-size: 1.5em;
    font-weight: bold;
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
export default {}
</script>