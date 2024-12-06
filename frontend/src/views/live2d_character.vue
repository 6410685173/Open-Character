<script setup lang="ts">
import { Application } from "pixi.js";




function onClick() {
  console.log('sprite clicked!');
}
</script>

<template>
  <Application :width="640" :height="480">
    <container>
      
    </container>
  </Application>
</template>