import { createWebHistory, createRouter } from 'vue-router'
import Chat  from "../views/chat.vue"
import Home from "../views/home.vue"
import LiveCharacter from "../views/live2d_character.vue"

const routes = [
    {
      path: '/', 
      component: Home, 
    },
    {
      path: '/chat/:id',    // Dynamic route for specific chat ID
      name: 'chat',
      component: Chat,      // Your Chat component
      props: true           // Pass route params as props
    },
    // { path: '/live2d', 
    //   name: 'live2d',
    //   component: LiveCharacter 
    // }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
  })


export default router