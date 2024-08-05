<template>
  <div>
    <h2 class="text-2xl font-bold mb-4">Secret Santa Draw</h2>
    <button
      class="bg-green-500 text-white px-4 py-2 rounded mb-4"
      @click="performDraw"
    >
      Perform Draw
    </button>

    <div v-if="currentDraw">
      <h3 class="text-xl font-semibold mb-2">Current Draw Results</h3>
      <ul class="divide-y divide-gray-200">
        <li v-for="result in currentDraw.results" :key="result.id" class="py-2">
          {{ result.giver }} is Secret Santa for {{ result.receiver }}
        </li>
      </ul>
    </div>

    <h3 class="text-xl font-semibold mt-6 mb-2">Previous Draws</h3>
    <ul class="divide-y divide-gray-200">
      <li v-for="draw in previousDraws" :key="draw.id" class="py-2">
        <p class="font-medium">
          Draw on {{ new Date(draw.date).toLocaleDateString() }}
        </p>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'DrawPage',
  data() {
    return {
      currentDraw: null,
      previousDraws: [],
    }
  },
  async fetch() {
    const response = await this.$axios.$get('draws/')
    this.previousDraws = response
    if (this.previousDraws.length > 0) {
      this.currentDraw = this.previousDraws[0]
    }
  },
  methods: {
    async performDraw() {
      try {
        const response = await this.$axios.$post('draws/')
        this.currentDraw = response
        this.previousDraws.unshift(response)
      } catch (error) {
        // console.error('Error performing draw:', error)
        alert('Error performing draw. Please try again.')
      }
    },
  },
}
</script>
