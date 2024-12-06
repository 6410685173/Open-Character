<script setup lang="ts">
import { RouterLink, RouterView, useRouter} from 'vue-router'
import { ref, onMounted, watch} from 'vue';

const conversations = ref<any[]>([]); // Initialize as an empty array
const router = useRouter()
// Fetch data from the API when the component is mounted
onMounted(async () => {
  try {
    const response = await fetch('http://localhost:8001/get_all_chat');
    if (!response.ok) throw new Error('Failed to fetch conversations');
    
    const data = await response.json();
    conversations.value = data; // Assuming data is an array of chat objects
  } catch (error) {
    console.error('Error fetching conversations:', error);
  }
});

const new_chat = async () => {
  try {
    const response = await fetch('http://localhost:8001/new_chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    const id = await response.json(); 
    // Redirect to chat page with the received ID
    router.push(`/chat/${id}`);
    if (!conversations.value.includes(id)) {
      conversations.value.push(id);
    }
  } catch (error) {
    console.error('Failed to new conversations:', error);
  }
}

const del_chat = async (id_conv: string) => {
  try {
    const response = await fetch('http://localhost:8001/del_chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body:JSON.stringify({id: id_conv})
    });

    conversations.value = conversations.value.filter((item: any) => String(item) !== String(id_conv));

  } catch (error) {
    console.error('Failed to new conversations:', error);
  }
}
const drawer = ref(true);
const rail = ref(true);
</script>

<template>
  <v-app>
    <v-main>
      <v-navigation-drawer
        v-model="drawer"
        :rail="rail"
        permanent
        @click="rail = false"
      >
        <v-list-item
          prepend-avatar="https://randomuser.me/api/portraits/men/85.jpg"
          title="Phumiphat"
        >
          <template v-slot:append>
            <v-btn
              icon="mdi-chevron-left"
              style="padding-top: 0px;"
              variant="text"
              @click.stop="rail = !rail"
            ></v-btn>
          </template>
        </v-list-item>
        
        <v-divider></v-divider>
        <v-card @click="new_chat">
            <v-card-title style="font-size: 15px;">
              <v-icon icon="mdi-chat"  class="me-2" style="font-size: 15px;"></v-icon>
                Start new chat
            </v-card-title>
        </v-card>
        <v-divider></v-divider>

        <!-- Scrollable conversation list -->
        <div class="scrollable-conversations" >
          <v-virtual-scroll :items="conversations " >
            <template v-slot:default="{ item: id, index }">
              <v-list-item
                :to="{ path: `/chat/${id}` }"
                component="RouterLink"
              >
              <v-list-item-content class="d-flex align-center justify-space-between" style="font-size: 15px;">
                <v-list-item-title>chat {{ index + 1 }}</v-list-item-title>

                
               
                <v-btn
                  style="margin: 0 0 0 0px;"
                  icon="mdi-delete"
                  size="x-small"
                  variant="text"
                  @click="del_chat(id as string)"
                ></v-btn>
                

                
              </v-list-item-content>
              </v-list-item>
            </template>
          </v-virtual-scroll>
        </div>
        
        
      </v-navigation-drawer>

      <!-- Main router view for pages -->
      <RouterView :key="$route.fullPath" />
    </v-main>
  </v-app>
</template>

            
            
<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}

html, body, #app {
  height: 100%;
  margin: 0;
  padding: 0;
}
.v-application--wrap {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
.fill-height {
  height: 100%;
}

.scrollable-conversations {
  max-height: 70vh; /* Controls the max height of the scrollable area */
  overflow-y: auto;
  padding-top: 8px;
}

</style>
