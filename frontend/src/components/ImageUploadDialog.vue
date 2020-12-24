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
  <v-dialog v-model="visible" width="50vw">
    <v-card>
      <v-card-title class="headline">Table Image</v-card-title>
      <v-card-text>
        <image-uploader
          :debug="1"
          :maxWidth="512"
          :quality="0.7"
          :autoRotate=true
          outputFormat="verbose"
          :preview=false
          :className="['fileinput', { 'fileinput--loaded' : hasImage }]"
          :capture="false"
          accept="video/*,image/*"
          doNotResize="['gif', 'svg']"
          @input="setImage"
          @onUpload="startImageResize"
          @onComplete="endImageResize"
        ></image-uploader>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<style>
</style>

<script>
// import dao from '../dao'
import ImageUploader from 'vue-image-upload-resize'

export default {

  computed: {
    visible() {
      return this.$root.showImageUpload
    }
  },
  components: {
    ImageUploader
  },
  

}
</script>