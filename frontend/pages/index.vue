<template>
  <div class="bg-white shadow overflow-hidden sm:rounded-lg">
    <div class="px-4 py-5 sm:px-6">
      <h3 class="text-lg leading-6 font-medium text-gray-900">
        Welcome to Secret Santa
      </h3>
      <p class="mt-1 max-w-2xl text-sm text-gray-500">
        Organize your gift exchange easily and fairly!
      </p>
    </div>
    <div class="border-t border-gray-200">
      <dl>
        <div
          class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
        >
          <dt class="text-sm font-medium text-gray-500">Total Participants</dt>
          <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
            {{ participantCount }}
          </dd>
        </div>
        <div class="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
          <dt class="text-sm font-medium text-gray-500">Last Draw Date</dt>
          <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
            {{ lastDrawDate }}
          </dd>
        </div>
      </dl>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
  data() {
    return {
      participantCount: 0,
      lastDrawDate: 'N/A',
    }
  },
  async fetch() {
    const participants = await this.$axios.$get('participants/')
    this.participantCount = participants.length

    const draws = await this.$axios.$get('draws/')
    if (draws.length > 0) {
      this.lastDrawDate = new Date(draws[0].date).toLocaleDateString()
    }
  },
}
</script>
