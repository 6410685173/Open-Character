<script setup lang="ts">
import { ref } from 'vue';
import { defineProps } from 'vue';


// Define the Props interface
interface Props {
  onSend: Function

}

// Define props
const props = defineProps<Props>();

// Create a ref for the message
const message = ref('');

// Function to send the message and clear the input
function sendMessage() {
  if (message.value.trim() !== '') {
    props.onSend(message.value);  // Call the passed function
    message.value = '';           // Clear the text area after sending
  }
}
</script>



<template>
    <v-row class="d-flex justify-center align-center row-container" >
      <v-col cols="11" md="6" style="padding: 0;">

        <v-textarea
        v-model="message"
        rows="1"  
        auto-grow
        placeholder="message"
        class="text-area"
        hide-details="auto"
        @keyup.enter="sendMessage"
        ></v-textarea>
      </v-col>
      <v-btn
         
            density="compact"
            
            size="large"
            class="icon-volume"
            icon='mdi-send'
            style="margin: 0 0 0 7px;"
            @click="sendMessage"
            >
          </v-btn>
    </v-row>
    
</template>

<style>
.text-area {
  max-height: 200px; /* Set the max height for scrolling */
  overflow-y: auto;  /* Allow vertical scrolling */
  border-radius: 25px;
  margin-bottom: 5px;
  background-color: #383838;
}

.row-container {
  border-radius: 25px;
}
</style>