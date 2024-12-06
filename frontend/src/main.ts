import { createApp } from 'vue'
import router from './routers/index.ts'

// Vuetify
import 'vuetify/styles'
import { createVuetify, type ThemeDefinition } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css'

// Components
import App from './App.vue'
const myCustomLightTheme: ThemeDefinition = {
  dark: false,
  colors: {
    background: '#282828', // Your desired background color
    surface: '#181818',
    primary: '#6200EE',
    'primary-darken-1': '#000000',
    secondary: '#03DAC6',
    'secondary-darken-1': '#000000',
    error: '#B00020',
    info: '#2196F3',
    success: '#4CAF50',
    warning: '#FB8C00',
  },
};

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'myCustomLightTheme',
    themes: {
      myCustomLightTheme,
    },
  },
  icons: {
    defaultSet: 'mdi', // This is already the default value - only for display purposes
  },
  
})
 

// Create the Vue app
createApp(App)
  .use(router)
  .use(vuetify) // Use Vuetify
  .mount('#app');
