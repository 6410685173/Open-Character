<script setup lang="ts">
import { defineProps, ref, computed} from 'vue';


// Define the Props interface
interface Props {
  text: string;
  onSend: Function
}

// Use defineProps with the Props interface
const props = defineProps<Props>();
const text = ref(props.text);

function ReSendMessage() {
  if (text.value.trim() !== '') {
    props.onSend(text.value,true);  // Call the passed function
  }
}

</script>

<template>
  <v-container class="hover-container">
    <v-row  class="d-flex justify-end align-end">
      <!-- <v-btn
          size="small"
          variant="text"
          icon='mdi-refresh'
          @click="ReSendMessage"
          class="hover-button"
          >
      </v-btn> -->
      <v-card class="user-box-message d-flex justify-end">
        <v-card-text  variant="tonal" style="font-size: 16px; padding: 15px;">
          {{ text }}
        </v-card-text>
      </v-card>
    </v-row>
  </v-container>
</template>

<style >
.user-box-message {
  margin-bottom: 5px; /* Space below the card */
  max-width: 50%; /* Set a maximum width */
  display: inline-block; /* Allows the card to fit content */
  word-break: break-word; /* Break long words */
  background-color: #424242; /* Add background color */
  border-radius: 1rem; /* Rounded corners */
  overflow-wrap: break-word; /* Allow breaking of long words */
}

.hover-container .hover-button {
  opacity: 0; /* Initially hidden */
  transition: opacity 0.3s ease; /* Smooth transition */
}

.hover-container:hover .hover-button,
.hover-button:hover {
  opacity: 1; /* Show the button on hover */
}
</style>
