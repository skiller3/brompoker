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
  <div>
    <v-card class="games-card">
      <v-card-title>
        Available Games
        <v-spacer></v-spacer>
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Search"
          single-line
          hide-details
        ></v-text-field>
      </v-card-title>
      <v-data-table
        :headers="headers"
        :items="games"
        :search="search"
        :loading="loading"
        loading-text="Loading games from server..."
      ></v-data-table>
    </v-card>
  </div>
</template>

<style scoped>
  .games-card {
    margin-top: 4em;
    margin-left: auto;
    margin-right: auto;
    padding-left: 4em;
    padding-right: 4em;
    max-width: 90em;
    border: 1px solid #2196f3;
  }
</style>

<script>
export default {
  name: 'Games',
  components: {
    
  },
  data() {
    return {
      search: '',
      headers: [
        {
          text: 'Name',
          align: 'start',
          sortable: true,
          value: 'name'
        },
        {
          text: 'Blinds & Antes',
          align: 'start',
          sortable: true,
          value: 'blinds_and_antes'
        },
        {
          text: 'Max Buy-in',
          align: 'start',
          sortable: true,
          value: 'max_buy_in'
        },
        {
          text: 'Min Buy-in',
          align: 'start',
          sortable: true,
          value: 'min_buy_in'
        },        
        {
          text: 'Seats',
          align: 'center',
          sortable: true,
          value: 'filled_seats'
        },
        {
          text: 'Description',
          align: 'start',
          sortable: true,
          value: 'description'
        }
      ],
      games: [
        {
          name: "Weekly NLHE Cash Game",
          blinds_and_antes: "100/200, 50",
          max_buy_in: 40000,
          min_buy_in: 30000,
          filled_seats: "5/9",
          description: "NLHE + 2/7 3/8 4/9 Bonus + 2/7 Street Rules"
        },
        {
          name: "Weekly Omaha Cash Game",
          blinds_and_antes: "100/200, 50",
          max_buy_in: 50000,
          min_buy_in: 25000,
          filled_seats: "4/9",
          description: "PLO + Trip Hole Card Bonus"
        }
      ]
    }
  },
  computed: {
    loading() {
      return this.games.length < 1
    }
  }
}
</script>
