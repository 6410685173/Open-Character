<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, toRefs } from 'vue';
import { useRoute } from 'vue-router';
import AIMessage from "../components/AIMessage.vue";
import BoxMessage from "../components/BoxMessage.vue";
import UserMessage from "../components/UserMessage.vue";

// Create a reactive reference for the WebSocket connection
const socket = ref<WebSocket | null>();
const connectionStatus = ref('closed');

const conversation_id = useRoute().params.id;


interface Response {
  id: string | null;
  role: 'assistant' | 'user' | 'system';
  text: string;
  background:string | null;
  mood:string | null;
  voice: HTMLAudioElement | Blob | null; // Optional for non-assistant roles, but can be null for all
}

// Reactive state for chat history
const history = ref<Response[]>([]); // 
const items = history
const stream = false
const is_voice_playing = ref(false);
let pendingVoiceId: string | null = null;
const wait_status = ref(false);

// Function to send a message
const send_message = async (content: string, resend: Boolean) => {
  if (!socket.value || socket.value.readyState !== WebSocket.OPEN) {
    // Only attempt to connect if the socket is closed or uninitialized
    await connect_socket(true);
  }

  if (socket.value && socket.value.readyState === WebSocket.OPEN) {
    // Push the user's message to the history
    history.value.push({
      id: null,
      role: "user", 
      text: content,
      background: null,  
      mood: null,
      voice:null         
    });

    // Create the message to send
    const messageToSend = {
      message: content,
      stream: stream, // Assuming you're using streaming
    };

    // Send the message over WebSocket
    socket.value.send(JSON.stringify(messageToSend));
    
    if (stream){ // if user set stream it will concat text as soon as it recieve from backend
      history.value.push({ 
        id: null,
        role: 'assistant',
        text: "", 
        background: null,  
        mood: null,
        voice:null,        
      });
    }else{
      wait_status.value = true
    }

  }
};
const get_voice = async (id: string) => {
  if (!socket.value || socket.value.readyState !== WebSocket.OPEN) {
    // Only attempt to connect if the socket is closed or uninitialized
    await connect_socket(true);
  }

  if (socket.value && socket.value.readyState === WebSocket.OPEN) {
    pendingVoiceId = id
    socket.value.send(JSON.stringify({ action: 'get_voice', id:id  }));
  }
}

// Function to handle incoming messages
const handleIncomingMessage = (event: MessageEvent) => {
  
  if (typeof event.data === 'string') {
    
    try {
      const data = JSON.parse(event.data); // Try to parse the JSON string
      
      if (data.history && Array.isArray(data.history)) { // Check if the data has a 'history' property(fetch hsitory conversation) for handle fetch data
        
      // Update the history array with memmory conversation
        history.value.push(...data.history.map((item: { id:string, role: string; content: string; background:string; mood:String;}) => ({
          id: item.id,
          role: item.role,
          text: item.content, 
          background: item.background,
          mood: item.mood,
          voice: null 
        })));

      }else{
        pendingVoiceId =  data.id
        history.value.push({ 
          id: data.id,
          role: 'assistant',
          text: data.content, 
          background: data.background,  
          mood: data.mood,  
          voice: null
        });
        wait_status.value = false
        console.log(history)
      }

    } catch (error) {
      // it's a plain string message for streaming
      if (stream){
        const lastAssistantMessage = history.value.slice().reverse().find(msg => msg.role === "assistant");
        if (lastAssistantMessage) {
          lastAssistantMessage.text += event.data;
        }
      }

    }
  } else if (event.data instanceof Blob) { // for recieving blob (audio)
    console.log("Blob received");
    
    const audioUrl = URL.createObjectURL(event.data);
    const audio = new Audio(audioUrl);
    
    // Find the last assistant message
    const lastAssistantMessage = history.value.slice().reverse().find(msg => msg.id === pendingVoiceId);
    if (lastAssistantMessage) {
      lastAssistantMessage.voice = audio; 
      pendingVoiceId = null; // Clear the pending ID after handling
    }

  }  
  // } else if (event.data instanceof ArrayBuffer) {
  //   console.log("ArrayBuffer")
  //   // Handle ArrayBuffer voice (binary data) 
  //   const audioBlob = new Blob([event.data], { type: 'audio/mpeg' });
  //   const audioUrl = URL.createObjectURL(audioBlob);

  //   const lastAssistantMessage = history.value.slice().reverse().find(msg => msg.role === "assistant");
  //   if (lastAssistantMessage) {
  //     lastAssistantMessage.voice = audioBlob;
  //   }

  //   // Play the audio
  //   const audio = new Audio(audioUrl);
  //   audio.play();
  //}
};



// Function to fetch history from the server
const fetchHistory = () => {
  if (socket.value && socket.value.readyState === WebSocket.OPEN) {
    socket.value.send(JSON.stringify({ action: 'fetch_history'}));
  }
  
};


const connect_socket = async (reconnect: boolean) => {
  // If already connected and no need for force reconnect, resolve immediately
  if (socket.value && socket.value.readyState === WebSocket.OPEN && !reconnect) {
      return Promise.resolve();
    }

    // Return a new promise that resolves when the connection is open
    return new Promise<void>((resolve) => {
      connectionStatus.value = 'reconnecting';
      
      socket.value = new WebSocket('ws://localhost:8001/front_ws');

      socket.value.onopen = () => {
        console.log('WebSocket connection established.');
        socket.value?.send(JSON.stringify({ id:conversation_id}));

        connectionStatus.value = 'open';
        resolve(); // Resolve the promise here, indicating connection is ready
        if (!reconnect){
          fetchHistory();
          console.log("fetchHistory")
        }
        
      };

      socket.value.onmessage = handleIncomingMessage; // Handle incoming messages

      socket.value.onerror = (error: Event) => {
        console.error('WebSocket Error:', error);
      };

      socket.value.onclose = () => {
        connectionStatus.value = 'closed';
        console.log('WebSocket connection closed.');
      };
    });
};

// Lifecycle hook to connect to WebSocket when the component is mounted
onMounted(connect_socket)

//Lifecycle hook to clean up the WebSocket connection when the component is unmounted
onBeforeUnmount(() => {
  if (socket.value) {
    socket.value.close();
    socket.value = null; // Clear the reference
  }
}); 


</script>



<template>

  <v-container class="status_server d-flex justify-end align-end">
    <v-row class="d-flex justify-end align-end">
      <div v-if="connectionStatus === 'open'" class="d-flex justify-end align-end">
        <v-icon
          color="green"
          icon="mdi-circle"
          size="x-small"
          style="margin-bottom: 2px; margin-right: 2px;"
        ></v-icon>
        <v-card variant="text" style="font-size: 13px">
          connect to server
        </v-card>
      </div>
      <div v-if="connectionStatus === 'closed'" class="d-flex justify-end align-end">
        <v-icon
          color="red"
          icon="mdi-circle"
          size="x-small"
          style="margin-bottom: 2px; margin-right: 2px;"
        ></v-icon>
        <v-card variant="text" style="font-size: 13px">
          disconect
        </v-card>
      </div>
      <div v-if="connectionStatus === 'reconnecting'" class="d-flex justify-end align-end">
        <v-icon
          color="yellow"
          icon="mdi-circle"
          size="x-small"
          style="margin-bottom: 2px; margin-right: 2px;"
        ></v-icon>
        <v-card variant="text" style="font-size: 13px">
          reconnecting
        </v-card>
      </div>
    </v-row>
  </v-container>
  
  <v-container style="margin-bottom: 4rem; margin-top: 2rem;">
    <v-virtual-scroll :items="items">
      <template v-slot:default="{ item }">
        <!-- AI Message -->
        <div v-if="item.role === 'assistant'" class="message-wrapper">
          <AIMessage :id ="item.id" 
                     :text="item.text" 
                     :is_voice_playing ="is_voice_playing" 
                     :mood = "item.mood"   
                     :background = "item.background" 
                     :voice ="item.voice" 
                     :get_voice="get_voice"
                     class="ai-message"/>
        </div>

        <!-- User Message -->
        <div v-if="item.role === 'user'" class="message-wrapper">
          <UserMessage :text="item.text" 
                       class="user-message" 
                       :onSend="send_message"/>
        </div>
      </template>
      
    </v-virtual-scroll>
      <div v-if="wait_status === true" class="message-wrapper">
          <AIMessage 
            :id="null" 
            text="Thinking..." 
            :is_voice_playing="false" 
            :mood="null" 
            :background="null" 
            :voice="null" 
            :get_voice="get_voice" 
            class="ai-message"
          />
      </div>

    <!-- Text box at the bottom -->
    <v-container class="fixed-box d-flex justify-center align-center">
      <BoxMessage :onSend="send_message" />
    </v-container>
  </v-container>
</template>



<style >
.fixed-box {
  bottom: 0;
  position: fixed;
  width: 100%;
  padding: 15px 0; /* Add padding for height */
  z-index: 10; /* Ensure it stays on top */
}

.status_server {
  position: fixed;
  top: 0; /* Aligns to the top */
  right: 0; /* Aligns to the right */
  z-index: 10;
  margin-right: 3rem; 
  margin-top: 1rem; 
}

.message-wrapper {
  max-width: 800px; /* Limit the width of the message container */
  width: 100%;
  margin: auto; /* Center the message container */
  display: flex; /* Flex container for alignment */
  
}

.ai-message {
  text-align: left; /* Align AI messages to the left */
  padding-bottom: 0;
}

.user-message {
  margin-left: auto; /* Push the user message to the right within the container */
  text-align: right; /* Align text within user message to the right */
}
</style>
