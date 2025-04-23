<template>
  <main>
    <div class="app-container">
      <div class="map-container">
        <ClassmatesMap />
      </div>
      <div class="data-container">
        <ClassmatesData />
      </div>
    </div>
  </main>
</template>

<script>
import ClassmatesMap from '../components/ClassmatesMap.vue'
import ClassmatesData from '../components/ClassmatesData.vue'

export default {
  name: 'HomeView',
  components: {
    ClassmatesMap,
    ClassmatesData
  }
}
</script>