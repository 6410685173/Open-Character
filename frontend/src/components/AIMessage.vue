<script lang="ts" setup>
import { defineProps, ref, watch, computed, onMounted   } from 'vue';
import img from '../assets/avatar/general.png';
import avatar_general from '../assets/avatar/general.png';
import avatar_curious_or_thinking from '../assets/avatar/curious_or_thinking.png';
import avatar_excited from '../assets/avatar/excited.png';
import avatar_glad_or_thankyou from '../assets/avatar/glad_or_thankyou.png';
import avatar_happy from '../assets/avatar/happy.png';
import avatar_sad_or_angry from '../assets/avatar/sad_or_angry.png';
import otrafford from '../assets/background/otrafford.jpg';
import university from '../assets/background/university.jpg';
import general from '../assets/background/general.jpg';
import dormitory from '../assets/background/dormitory.jpg';
import hometown from '../assets/background/hometown.jpg';

// Define the Props interface
interface Props {
  id:string | null;
  text: string ;
  is_voice_playing: boolean | null;
  mood:string | null;
  background:string | null;
  voice: HTMLAudioElement  | Blob | null;
  get_voice: Function ;
}

// Use defineProps with the Props interface
const props = defineProps<Props>();
const text = ref(props.text);
const id = props.id
const voice = ref(props.voice);
const isPlaying = ref(props.is_voice_playing);
const isImageOpened = ref(false);
const mood = ref();
const background = ref();


// Watch for changes in the props and update the reactive ref accordingly
watch(() => props.text, (newText) => {
  text.value = newText;
});

const play_audio = () => {
  if (voice.value instanceof HTMLAudioElement) {
    isPlaying.value = true;
    voice.value.play();
    voice.value.onended = () => {
      isPlaying.value = false;
    };
  } else if (voice.value === null) {
    props.get_voice(id); 
  }
};
const stop_audio = () => {
  if (voice.value instanceof HTMLAudioElement) {
    isPlaying.value = false;
    voice.value.pause();
    voice.value.currentTime = 0;  
  } else if (voice.value === null) {
    props.get_voice(id); 
  }
};


const toggleAudio = () => {
    
  if (isPlaying.value) {
    stop_audio();
  } else {
    play_audio(); 
  }
};

// Function to handle the toggle
const openimage = () => { 
  isImageOpened.value = !isImageOpened.value; // Toggle the state
};


const formattedText = computed(() => {
  // First, replace code blocks using markdown-like syntax
  let formattedText = props.text.replace(/```(.*?)\n([\s\S]*?)```/g, (match, lang, code) => {
    return `<code class="${lang}">${code}</code>`;
  });

  // Then, replace newlines with <br> tags for normal text
  return formattedText.replace(/\n/g, '<br>');
});

// Watch for changes in the props and update the reactive ref accordingly
watch(() => props.voice, (newVoice) => {
    console.log(newVoice)
    voice.value = newVoice;
    play_audio(); // Call play_audio when voice is set
  
});

onMounted(() => {
  if (props.mood === "general"){
    mood.value = avatar_general;
  }else if(props.mood === "happy"){
    mood.value = avatar_happy;
  }else if(props.mood === "sad_or_angry"){
    mood.value = avatar_sad_or_angry;
  }else if(props.mood === "excited"){
    mood.value = avatar_excited;
  }else if(props.mood === "glad_or_thankyou"){
    mood.value = avatar_glad_or_thankyou;
  }else if(props.mood === "curious_or_thinking"){
    mood.value = avatar_curious_or_thinking;
  }else{
    mood.value = avatar_general;
  }

  if (props.background === "general"){
    background.value = general;
  }else if(props.background === "football field"){
    background.value = otrafford;
  }else if(props.background === "chiang rak"){
    background.value = dormitory;
  }else if(props.background === "hometown"){
    background.value = hometown;
  }else if(props.background === "university"){
    background.value = university;
  }else{
    background.value = general;
  }
})
</script>


<template>
  <v-container class="ai-box-message">
    <v-row class="d-flex" style=" flex-wrap: nowrap;">
      <!-- Avatar on the left -->
      <v-avatar
        size="30"
        style="margin-right: 0px;"
        :image="img"
      />
      
      <!-- Text on the same row -->
      <v-card-text v-html="formattedText" style="font-size: 16px; padding-left: 15px; padding-top: 5px;"></v-card-text>
    </v-row>
    <v-row class="d-flex mx-0">
        
          
      <v-btn
        v-if="id !== null"
        density="compact"
        variant="text"
        size="small"
        class="icon-volume"
        :icon="isPlaying ? 'mdi-pause-circle' : 'mdi-volume-high'"
        @click="toggleAudio"
        style="margin: 0 0 0 2rem"
        >
        
      </v-btn>
    
    
      <v-btn
        v-if="id !== null"
        density="compact"
        variant="text"
        size="small"
        class="icon-image"
        :icon="isImageOpened ? 'mdi-image' : 'mdi-image-off'"
        @click="openimage"
        style="margin: 0 0 0 10px"
        >
      </v-btn>
        

    </v-row>
    <div class="d-flex justify-center" style="margin-top: 2rem; ">
      <div class="image-container" v-if="isImageOpened">
        <img :src="background" class="background-image" />
        <img :src="mood" class="avatar-image" />
      </div>

      
        
      
    </div>
    
  </v-container>
</template>



<style >
.ai-box-message {
    
    width: 80%;
    
}
.v-btn {
  
  margin-top: 17px;
  margin-left: 10px;
}
/* Optional: Add some styles for code blocks */
code {
  background-color: #6e6e6e;
  padding: 0.5em;
  display: block;
  border-radius: 5px;
  white-space: pre-wrap; /* Preserve formatting inside the code block */
}

.icon-volume .v-icon {
  font-size: 20px; /* Adjust size here */
  color: #757575; /* Custom color */

}

.icon-image .v-icon {
  font-size: 20px; /* Adjust size here */
  color: #757575; /* Custom color */

}

.image-container {
  position: relative;
  width: 80%;  /* Fixed width */
  height: 100%; /* Fixed height */
  margin: 0 auto; /* Center container */
}

.background-image {
  width: 100%;
  height: 100%;
  object-fit: cover; /* Ensures background covers area */
  display: block;
  opacity: 1;
}

.avatar-image {
  position: absolute;
  bottom: 0;
  opacity: 1;
  
  width: 300px;  /* More reasonable size */
  height: 350px;
  object-fit: contain; /* Maintains PNG aspect ratio */
}



</style>